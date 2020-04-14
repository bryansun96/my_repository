import unittest
from HW09_Bin_Sun import Student, Instructor, Repository
from typing import Dict
from HW08_Bin_Sun import file_reader
import os

def test_Student(self, Student: str) -> None:
    """ test students function"""
    directory: str = '/Users/germysun/Desktop/python/810/assignment/HW09_Test_Bin_Sun/'
    expect: Dict[str, Dict[str, int]] = {
                        '10103': ('10103', 'Baldwin, C', ['CS 501', 'SSW564', 'SSW 687']),
                        '10115': ('10115', 'Wyatt, X', ['CS 545', 'SSW 567', 'SSW 687']),   
                        '10172': ('10172', 'Forbes, I', ['SSW 564', 'SSW 567']), 
                        '10175': ('10175', 'Erickson, D', ['SSW 564', 'SSW 567' , 'SSW 687']), 
                        '10183': ('10183', 'Chapman, O', ['SSW 689']), 
                        '11399': ('11399', 'Cordova, I', ['SSW 540']), 
                        '11461': ('11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS800']),  
                        '11658': ('11658', 'Kelly, P', ['SSW 540']),   
                        '11714': ('11714', 'Morton, A', ['SYS 611', 'SYS645']),  
                        '11788': ('11788', 'Fuller, E', ['SSW 540'])}
    fact = {cwid: student.pt_row() for cwid, student in self.Repository._students.item()}
    self.assertEqual(expect, fact)

def test_Instructor(self, Instructor: str) -> None:
    """test instructor function"""
    directory: str = '/Users/germysun/Desktop/python/810/assignment/HW09_Test_Bin_Sun/'
    expect: Dict[str, Dict[str, int]] = {
                            ('98765', 'Einstein, A', 'SFEN', 'SSW 555', 4),
                            ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 3),
                            ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                            ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                            ('98763', 'Newton, I', 'SFEN', 'CS 510', 1),
                            ('98763', 'Newton, I', 'SFEN', 'CS 545', 1),
                            ('98762', 'Hawking, S', 'SYEN', 'SYS 800', 1),
                            ('98762', 'Hawking, S', 'SYEN', 'SYS 800', 1),}
    fact = {tuple(item) for instructor in self.Repository._instructors.values() for item in instructor.pt_rows()}

    self.assertEqual(expect, fact)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)