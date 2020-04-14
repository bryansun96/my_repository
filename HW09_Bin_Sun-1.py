from typing import Dict, DefaultDict, Any, Tuple, List, Iterator
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Bin_Sun import file_reader
import os




class Student:
    """ create a student"""
    pt_header = ["CWID", "Name", "Major", "Courses"]

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """ store the init value"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def store_course_grade(self, course: str, grade: str) -> None:
        """ note that students take course and earned grade"""
        self._courses[course] = grade

    def pt_row(self) -> Tuple[str, str, List[str]]:
        """return a list of the information about me/self need for the pretty table"""
        return [self._cwid, self._major, self._name, sorted(self._courses.keys())]




class Instructor:
    """ create an instructor """
    def __init__(self, cwid: str, name: str, dept: str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int) #course[course name] = #of studentrs who take

    def store_course_students(self, course: str, students: str) -> None:
        """ note that inst taught course to one more students"""
        self._courses[course] += 1

    def pt_rows(self) -> Iterator[Tuple[str, str, str, str, int]]:

        for course, count in self._courses.items():
            yield self._cwid, self._name, self._dept, course, count

class Repository:
    """ store all information about students and instructors"""

    def __init__(self, path: str, students: str, Instructor: str, ptables: bool=True) -> None:
        self._path: str = path
        self._students: Dict[str, Student] = dict() #_students[cwid] = student()
        self._instructors: Dict[str, Instructor] = dict()

        try:
            self._read_students(os.path.join(wdir, 'students.txt'))
            self._read_instructors(os.path.join(wdir, 'instructors.txt'))
            self._read_grades(os.path.join(wdir, 'grades.txt'))
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)
        
        if ptables:
            print("\nStudent Summary")
            self.student_prettytable()

            print("\nInstructor Summary")
            self.instructor_prettytable()
    
    def _read_students(self, path: str, ptables: bool=True) -> None:
        """read rach line from path/students.txt and create 
         an instance of class students for each line"""
        for cwid, name, major in file_reader(path, 3, sep = '\t', header = False):
            self._students[cwid]= Student(cwid, name, major)

    
    def _read_instructors(self, path: str, course: str, student: str, Student_cwid: int, ptables: bool=True) -> None:
        """read rach line from path/instructors.txt and create 
         an instance of class instructors for each line"""
        for cwid, name, dept in file_reader(path, 3, sep = '\t', header = False):
            self._students[cwid]= Instructor(cwid, name, dept)


    def _read_grades(self, path: str, Student: str, instructor: str, course: str, grade: int, Student_cwid: int, Instructor_cwid: int) -> None:
        """read rach line from path/students.txt and create 
         an instance of class students for each line"""
        for Student_cwid, course, grade, Instructor_cwid in file_reader(os.path.join(self._path, 'grades.txt'),4, sep = '\t', header = False):
            if Student_cwid in self._students:
                self._students[Student_cwid].store_course_grade(course, grade)
            else:
                print(f"The unknown student grade was found '{Student_cwid}'")

            if Instructor_cwid in self._instructors:
                self._instructors[Instructor_cwid].store_course_students(course)
            else:
                print(f"The unknown instructor was found '{Instructor_cwid}'")
    

    def student_prettytable(self) -> None:
        """ create the petty table of student"""
        pt: PrettyTable() = PrettyTable(field_names = Student.pt_header)
        pt.field_names = ["CWID", "Name", "Major", "Courses"]
        for student in self._students.values():
            pt.add_row(student.pt_row())

        return pt


    def instructor_prettytable(self) -> None:
        """create the pretty table of instrutor"""
        pt = PrettyTable()
        pt.field_names = ["CWID", "Name", "Dept", "Course", "Students"]
        # generator 
        for instructor in self._instructors.values():
            for row in instructor.prettytable_row():
                pt.add_row(row)

        return pt
        

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