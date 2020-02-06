class Student():
    def __init__(self, name, hakbun, major, kor, eng, math):
        self.name = name
        self.hakbun = hakbun
        self.kor = kor
        self.eng = eng
        self.math = math

def Insert_student(name, hakbun, major, kor, eng, math):
    student = Student(name,hakbun, major, kor, eng, math)
    return student

student_list = []
student = Insert_student('야', '90198', '왜', 100, 80, 90)
student_list.append(student)
student_list.append(Insert_student('야2', '70101', '왜2', 100, 80, 90))
student_list.append(Insert_student('야3', '13146', '왜3', 100, 80, 90))
student_list.append(Insert_student('야4', '40001', '왜4', 100, 80, 90))

sorted_list = sorted(student_list, key=lambda student: student.hakbun)
unsorted_list = sorted(student_list, key=lambda hakbun: student.hakbun)

print('\n정렬 전 원본:')

for ele in student_list:
    print(ele.hakbun)

print('\n정렬 후:')

for ele in sorted_list:
    print(ele.hakbun)

print('\n잘못된 정렬:')

for ele in unsorted_list:
    print(ele.hakbun)

