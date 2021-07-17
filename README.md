# canvas-csv-autograder
Grade Canvas assignment based on scores stored in the csv file. It can work with the exported csv grades from Joint Online Judge.

1. Set `CANVAS_TOKEN` at .env in the root directory
2. <del>Modify the settings in `settings.py` if you need</del>
3. You must set a default grade for this assignment for each student before running this script

You can also use this script to upload scores on Canvas based on your own csv file (you should include students' sjtu id. OR if your csv have the same first three columns as JOJ 1.0 csv format)

**Usage**
~~~shell script
PYTHONPATH=. python grade_from_joj.py [csv_path] [course_id] [assignment_id] [canvas_full_score] [csv_full_score]
~~~

csv_path is the path of the JOJ exported grade csv file

course_id: It can be obtained from Canvas course page url. It is the id of the course

course_id: It can be obtained from Canvas assignment page url. It is the id of the assignment

canvas_full_score: the full score of this assignment on canvas

csv_full_score: the full score of this assignment/homework on joj (or the full score that leads to the score in your csv)

### How to prepare your own csv file
By default, the third column of your csv should be the SJTU id of a student. The fourth column should be his total score.

Prepare you csv following the rule above.

### Example
Assignment p2 of VE280 Summer 2021 Section (Paul) is located at
~~~
https://umjicanvas.com/courses/2036/assignments/19399
~~~

The course id is `2036`. The assignment id is `19399`.
If our exported csv from joj p2 judge is located at `/tmp/Project2Bot.csv`, and we have 120 cases with each 10 points,and the full score on Canvas for p2 joj part is 85, we can run as
~~~
PYTHONPATH=. python3 grade_from_joj.py /tmp/Project2Bot.csv 2036 19399 85 1200
~~~

### Further
You can check `settings.py` to modify the script as you need.

### Issues
You are welcomed to post an issue or pull request if you encounter any problems regarding this repo.