
from typing import Dict, DefaultDict, Any, Tuple, List, Iterator, Set
from collections import defaultdict
from prettytable import PrettyTable
from HM08_Bin_Sun import file_reader
import sqlite3
from statistics import mean
import os


class Major:
    pt_header: Tuple[str, str, str] = ("Major", "Required Courses", "Electives")

    # JRR def __init__(self, required: str, electives: str, dept: str) -> None:
    # JRR2 def __init__(self, dept: str, required: str, electives: str) -> None:  # JRR: you don't know the required or electives until after the Major is created
    def __init__(self, dept: str, required: str, electives: str) -> None:
        self._dept: str = dept
        # JRR: self._required: List[str] = required   # or use set()
        # JRR: self._electives: List[str] = electives
        # JRR2: self._required: Set[str] = required
        # JRR2: self._electives: Set[str] = electives
        # JRR2: you could use either a set or a list.   your store_course_majors() uses a list so I made these lists
        self._required: Set[str] = required  # JRR2: the required will be filled in later
        self._electives: Set[str] = electives # JRR2: the required will be filled in later
        # JRR: not needed - self._courses: Dict[str, str] = dict()

    # JRR: def store_course_majors(self, major: str, required: str, elective: str, course: str):
    def store_course_majors(self, type: str, course: str):
        """ store majors data"""
        if type == 'R':
            #JRR self._required.add(course)
            self._required.append(course)
        elif type == 'E':
            # JRR self._required.add(course)
            self._electives.append(course)
        else:
            raise ValueError(f"Major.store_coourse_majors: expected 'R' or 'E' but found '{type}' ")

    def get_required(self) -> List[str]:
        # JRR
        return list(self._required)

    def get_electives(self) -> List[str]:
        # JRR
        return list(self._electives)

    def pt_row(self) -> Tuple[str, List[str], List[str]]:
        """return a list for prettytable"""
        # JRR return [self._dept, sorted(self._required), sorted(self._electives)]
        return (self._dept, sorted(self._required), sorted(self._electives))


class Student:
    """ create a student"""
    # JRR pt_header = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Required", "Remaining Electives", "GPA"]
    pt_header = ["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives", "GPA"]

    _passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C-'}

    _grade_map: Dict[str, float] = {
                'A': 4.0, 'A-': 3.75,
                'B+': 3.25, 'B': 3.0, 'B-': 2.75,
                'C+': 2.25, 'C': 2.0, 'C-': 0,
                'D+': 0, 'D': 0, 'D-': 0,
                'F': 0    }

    def __init__(self, cwid: str, name: str, major: str, required: List[str], electives: List[str]) -> None:
        """ store the init value"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()
        self._rem_required: List[str] = required
        self._rem_electives: List[str] = electives

    # JRR def store_course_grade(self, course: str, grade: str, major: str, required: str) -> None:
    # JRR2: def store_course_grade(self, course: str, grade: str, major: str, required: str) -> None:
    def store_course_grade(self, course: str, grade: str, major: str, required: str) -> None:
        """ note that students take course and earned grade"""
        if grade not in Student._grade_map:
            raise ValueError(f"'{grade}'is an invalid grade for course '{course}' for student {self._name} ")
        else:
            self._courses[course] = grade

            if grade in Student._passing_grades:
                if course in self._rem_required:
                    self._rem_required.remove(course)

                if course in self._rem_electives:
                    # JRR self._rem_electives = set()
                    # JRR2: you're using lists in some places and lists in other.  Must be consistent
                    # JRR2: self._rem_electives = set()
                    self._rem_electives = set()

    def _GPA(self) -> float:
        """ calculate and return the student's gpa based on the course"""
        points = [Student._grade_map[grade] for grade in self._courses.values()]
        if len(points) > 0:
            return round(mean(points), 2)
        else:
            return 0.0


    # JRR def pt_row(self) -> Tuple[str, str, List[str]]:
    # JRR2 you're returning 7 elements so the type hint must match
    # JRR2: def pt_row(self) -> Tuple[str, str, List[str]]:
    def pt_row(self) -> Tuple[str, str, List[str]]:
        """return a list of the information about me/self need for the pretty table"""
        return (self._cwid, self._major, self._name, sorted(self._courses.keys()), \
                sorted(self._rem_required), sorted(self._rem_electives), self._GPA())




class Instructor:
    """ create an instructor """
    def __init__(self, cwid: str, name: str, dept: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int) #course[course name] = #of studentrs who take

    # JRR def store_course_students(self, course: str, students: str) -> None:
    # JRR2: def store_course_students(self, course: str, students: str) -> None:
    def store_course_students(self, course: str, students: str) -> None:
        """ note that inst taught course to one more students"""
        self._courses[course] += 1

    def pt_rows(self) -> Iterator[Tuple[str, str, str, str, int]]:

        for course, count in self._courses.items():
            yield self._cwid, self._name, self._dept, course, count

class Repository:
    """ store all information about students and instructors"""

    def __init__(self, wdir: str, ptables: bool=True) -> None:
        # JRR2: self._students: student()   #_students[cwid] = student() 
        self._students: Dict[str, Student] = dict()   #_students[cwid] = student() 
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()
        try:
            self._read_majors(os.path.join(wdir, 'majors.txt'))
            self._read_students(os.path.join(wdir, 'students.txt'))
            self._read_instructors(os.path.join(wdir, 'instructors.txt'))
            self._read_grades(os.path.join(wdir, 'grades.txt'))
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)
        
        if ptables:
            print("\nMajor summary")
            self.majors_prettytable()

            print("\nStudent Summary")
            self.student_prettytable()

            print("\nInstructor Summary")
            self.instructor_prettytable()

            print("\nStudent Grade Summary")
            self.student_grades_prettytable()

         
    
    # Bin def _read_majors(self, path: str, ) -> None:
    # JRR2: we don't know the major yet def _read_majors(self, path: str, Major: str) -> None:
    def _read_majors(self, path: str, Major: str) -> None:
        """ read majors files and assign course to majors
        """
        # JRR2: for major, flag, course in file_reader(path, 3, sep='\t', header=False):
        for major, flag, course in file_reader(path, 3, sep='\t', header=False):
            if major not in self._majors:
                self._majors[major] = Major(major)

            self._majors[major].store_course_majors(flag, course)


    # JRR def _read_students(self, path: str, 'ptables: bool=True') -> None:
    def _read_students(self, path: str, ptables: bool=True) -> None:
        """read rach line from path/students.txt and create 
         an instance of class students for each line
         """
        # JRR2: for cwid, name, major in file_reader(path,3, sep = ';', header = False):
        for cwid, name, major in file_reader(path,3, sep = ';', header = False):
            if major not in self._majors:
                print(f"Student {cwid} '{name}' has unknown major '{major}' ")
            else:
                self._students[cwid]= Student(cwid, name, major, self._majors[major].get_required(), self._majors[major].get_electives())
    

    # jrr def _read_instructors(self, path: str,course: str, student: str, Student_cwid: int, ptables: bool=True) -> None:
    # JRR2: def _read_instructors(self, path: str, course: str, student: str, Student_cwid: int, ptables: bool=True) -> None:
    def _read_instructors(self, path: str, course: str, student: str, Student_cwid: int, ptables: bool=True) -> None:
        """read rach line from path/instructors.txt and create 
         an instance of class instructors for each line"""
        # JRR for cwid, name, dept in file_reader(path,3, sep = '\t', header = False):
        # JRR2: for cwid, name, dept in file_reader(path,3, sep = '\t', header = False):
        for cwid, name, dept in file_reader(path,3, sep = '\t', header = False):
            #JRR self._students[cwid]= Instructor(cwid, name, dept)
            self._instructors[cwid]= Instructor(cwid, name, dept)


    # JRR  def _read_grades(self, path: str, ‘Student: str, instructor: str, course: str, grade: int, Student_cwid: int, Instructor_cwid: int’) -> None:
    # JRR2: def _read_grades(self, path: str , Student: str, instructor: str, course: str, grade: int, Student_cwid: int, Instructor_cwid: int) -> None:
    def _read_grades(self, path: str) -> None:
        """read rach line from path/students.txt and create 
         an instance of class students for each line"""
        # JRR for Student_cwid, course, grade, Instructor_cwid in file_reader(path,4, sep = '\t', header = ‘False’):
        # JRR2: for Student_cwid, course, grade, Instructor_cwid in file_reader(path,4, sep = '\t', header = False):
        for Student_cwid, course, grade, Instructor_cwid in file_reader(path,4, sep = '\t', header = False):
            if Student_cwid in self._students:
                    self._students[Student_cwid].store_course_grade(course, grade)
            else:
                    print(f"The unknown student grade was found '{Student_cwid}'")

            if Instructor_cwid in self._instructors:
                    self._instructors[Instructor_cwid].store_course_students(course)
            else:
                    print(f"The unknown instructor was found '{Instructor_cwid}'")
       

    def majors_prettytable(self):
        """ print prettytable with a summary of all majors"""
        pt: PrettyTable = PrettyTable(field_names = Major.pt_header)
        for major in self._majors.values():
            pt.add_row(major.pt_row())
        print(pt)

    def student_prettytable(self) -> None:
        """ create the petty table of student"""
        #JRR pt: PrettyTable() = PrettyTable(field_names = Student.pt_header)
        pt: PrettyTable = PrettyTable(field_names = Student.pt_header)
        pt.field_names = ["CWID", "Name", "Major", "Course"]
        # 'JRR pt.field_names = ["CWID", "Name", "Major", "Courses"]'
        # JRR2: pt.field_names = ["CWID", "Name", "Major", "Course"]
        for student in self._students.values():
            pt.add_row(student.pt_row())

        # JRR return pt
        print(pt)  # JRR2
        return pt


    def instructor_prettytable(self) -> None:
        """create the pretty table of instrutor"""
        pt = PrettyTable()
        pt.field_names = ["CWID", "Name", "Dept", "Course", "Students"]
        # generator 
        for instructor in self._instructors.values():
            #for row in instructor.prettytable_row():
            #for row in instructor.prettytable_row():
            for row in instructor.pt_rows():
                pt.add_row(row)

        # JRR return pt
        print(pt)  # JRR2
        return pt
        
    def student_grades_prettytable(self) -> None:
        """ create new student_grades prettytable """
        try:
            db: sqlite3.Connection = sqlite3.connect('/Users/germysun/Desktop/python/810/assignment/HM11.sqlite')
        except sqlite3.OperationalError as e:
            print(e)
        else:
            pt: PrettyTable = PrettyTable(field_names = ['Name', 'CWID', 'Course','Grade', 'Instructor'])
            try:
                for tup in db.execute("select * from students"):
                    pt.add_row(tup)
                print(pt)
            except sqlite3.OperationalError as e:
                print(e)
            


def main():
    """ define two repositories
    """
    
    #wdir0 = '/Users/germysun/Desktop/python/810/assignment/HW09_Bin_Sun'
    wdir0 = '/Users/germysun/Desktop/python/810/assignment/HW09_Bin_Sun'
    wdir1 = '/Users/germysun/Desktop/python/810/assignment/HW09_Bin_Sun'
    _ = Repository('/Users/jrr/Documents/Stevens/810/Assignments/HW10_Repository')

    print("The good data.")
    #_ = Repository(wdir0)

    print("\nunnesessary data")
    print(" the unknown major or unknown student should be reported.")
    #_ = Repository(wdir1)

    



if __name__ == "__main__":
    main()
