"""
Canvas fast grading script from csv file of grades
by makersmelx <makersmelx@gmail.com>
"""
import canvasapi
import utils
import os
import csv
from canvasapi import Canvas, exceptions
import sys
import settings


def joj_score_to_canvas_score(_student, _canvas_full_score, _csv_full_score):
    cli_weight = float(_canvas_full_score) / float(_csv_full_score)
    print('==============================')
    print("{}\t{}".format(
        _student[settings.csv_name_column], _student[settings.csv_sjtu_id_column]))
    _score = 0
    if len(settings.csv_score_column) != len(settings.weight):
        print("Make sure that you can add a weight to all the columns you would like to include")
        exit(1)
    settings.weight = [cli_weight]
    for i in range(len(settings.csv_score_column)):
        _column_grade = _student[settings.csv_score_column[i]]
        try:
            _column_grade = float(_column_grade)
        except ValueError:
            _column_grade = 0
        _score += float(_column_grade) * settings.weight[i]

    # adjustment
    if _student[settings.csv_sjtu_id_column] in settings.extra_adjust:
        _adjust = settings.extra_adjust[_student[settings.csv_sjtu_id_column]]
        _score += _adjust
        print("Extra adjust: {}".format(_adjust))

    print('Now score: {}'.format(_score))

    if _student[settings.csv_sjtu_id_column] in settings.direct_reassign:
        _reassign = settings.direct_reassign[_student[settings.csv_sjtu_id_column]]
        _score = _reassign
        print('Score is directly re-assigned to: {}'.format(_reassign))
    print('==============================')
    return _score


def main(_csv_file, _course_id, _assignment_id, _canvas_full_score, _csv_full_score):
    utils.import_env()
    canvas_base_url = os.environ['CANVAS_BASE_URL']
    canvas_token = os.environ['CANVAS_TOKEN']
    umji_canvas = Canvas(canvas_base_url, canvas_token)
    course = None
    assignment = None
    try:
        course = umji_canvas.get_course(_course_id)
    except canvasapi.exceptions.ResourceDoesNotExist:
        print("Course does not exist. Exit.", file=sys.stderr)
        exit(1)
    try:
        assignment = course.get_assignment(_assignment_id)
    except canvasapi.exceptions.ResourceDoesNotExist:
        print("Assignment does not exist. Exit.", file=sys.stderr)
        exit(1)

    students = {}

    for _student in course.get_users(enrollment_type=['student']):
        students[_student.id] = _student.sis_login_id

    joj_scores = {}

    with open(_csv_file) as joj_csv:
        joj_score = csv.reader(joj_csv)
        skip_line = 0
        for student_row in joj_score:
            if skip_line < settings.content_row:
                skip_line += 1
                continue
            score = joj_score_to_canvas_score(student_row, _canvas_full_score, _csv_full_score)
            student_id = student_row[settings.csv_sjtu_id_column].strip()
            joj_scores[student_id] = score

    all_submissions = assignment.get_submissions()

    for _submission in all_submissions:
        if _submission.user_id in students:
            this_student_sjtu_id = students[_submission.user_id]
            this_joj_score = joj_scores.get(this_student_sjtu_id, 0)
            print('SJTU ID:{}, Score:{}'.format(
                this_student_sjtu_id, this_joj_score))
            _submission.edit(submission={'posted_grade': this_joj_score})


try:
    csv_file = sys.argv[1] if sys.argv[1] else settings.csv_path
    course_id = sys.argv[2]
    assignment_id = sys.argv[3]
    canvas_full_score = float(sys.argv[4])
    csv_full_score = float(sys.argv[5]) if len(sys.argv) > 5 else canvas_full_score
    main(csv_file, course_id, assignment_id, canvas_full_score, csv_full_score)
except ValueError as e:
    print(e, file=sys.stderr)
    print('The scores are invalid.', file=sys.stderr)
    exit(1)
