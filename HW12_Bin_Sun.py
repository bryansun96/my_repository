from flask import Flask, render_template
from typing import Dict
import sqlite3


DB_FILE: str = '/Users/germysun/Desktop/python/810/assignment/HW11.db'

app: Flask = Flask(__name__)

@app.route('/students')
def students_summary() -> str:
    query: str = """select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as InstructorName
                    from students s join grades g on s.CWID = g.StudentCWID
                    join instructors i on g.InstructorCWID = i.CWID
                    order by s.Name"""

    db: sqlite3.Connection = sqlite3.connect(DB_FILE)
    print(db)

    data: Dict[str, str] = \
        [{ 'Name': Name, 'CWID': CWID, 'COurse': Course, 'Grade': Grade, 'Instructorname': Instructorname}
            for Name, CWID, Course, Grade, Instructorname in db.execute(query) ]
    db.close()
    return render_template('Stevens.html',
                            title = 'Stevens Repository',
                            table_title = 'Students data',
                            students = data)

app.run(debug=True)



