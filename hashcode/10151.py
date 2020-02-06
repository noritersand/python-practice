
class Student():

    def __init__(self, name, hakbun, major, kor, eng, math, score, avg, grade):
        self.name = name
        self.hakbun = hakbun
        self.kor = kor
        self.eng = eng
        self.math = math
        self.score = score
        self.avg = avg
        self.grade = grade

    def print_info(self):
        print("이름 : ", self.name)
        print("학번 : ", self.hakbun)
        print("국어 : ", self.kor)
        print("영어 : ", self.eng)
        print("수학 : ", self.math)
        print("총점 : ", self.score)
        print("평균 : ", self.avg)
        print("학점 : ", self.grade)

def Insert_student(name, hakbun, major, kor, eng, math):
    # name = input('이름을 입력하세요 : ')
    # hakbun = input('학번을 입력하세요 : ')
    # major = input('학과를 입력하세요 : ')
    # kor = int(input('국어 성적을 입력하세요 : '))
    # eng = int(input('영어 성적을 입력하세요 : '))
    # math = int(input('수학 성적을 입력하세요 : '))
    print("학생이 입력되었습니다.\n")

    score = kor + eng + math
    avg = round(score / 3, 3)
    if avg >= 95:
        grade = "A+"
    elif avg >= 90:
        grade = "A0"
    elif avg >= 85:
        grade = "B+"
    elif avg >= 80:
        grade = "B0"
    elif avg >= 75:
        grade = "C+"
    elif avg >= 70:
        grade = "C0"
    elif avg >= 65:
        grade = "D+"
    elif avg >= 60:
        grade = "D0"
    else:
        grade = "F"
    student = Student(name,hakbun, major, kor, eng, math, score, avg, grade)
    return student

def Search_student(student_list, name):
    for i, student in enumerate(student_list):
        if student.name == name:
            print("======================================================================")
            student.print_info()
            print("======================================================================")

        else:
            print('해당 이름이 없습니다.')

    return student

def delete_contact(student_list, name):
    for i, student in enumerate(student_list):
        if student.name == name:
            del student_list[i]

def print_student(student_list):
    for student in student_list:
        student.print_info()

def print_menu():
    print("1. 데이터 추가")
    print("2. 데이터 검색")
    print("3. 데이터 삭제")
    print("4. 데이터 정렬")
    print("0. 종료\n")
    menu = input("메뉴선택: ")
    return int(menu)

def main():

    student_list = []
    print()
    print("                      학생 관리 프로그램      \n")
    print("메뉴 생성\n")
    while 1:
        menu = print_menu()

        # ----- 데이터 추가 -----
        if menu == 1:
            student = Insert_student('야', '90198', '왜', 100, 80, 90)
            student_list.append(student)
            student_list.append(Insert_student('야2', '70101', '왜2', 100, 80, 90))
            student_list.append(Insert_student('야3', '13146', '왜3', 100, 80, 90))
            student_list.append(Insert_student('야4', '40001', '왜4', 100, 80, 90))

        # ----- 데이터 검색 -----
        elif menu == 2:
            name = input('검색할 학생의 이름을 입력해주세요 : ')
            Search_student(student_list, name)

        # ----- 데이터 삭제 -----
        elif menu == 3:
            name = input('삭제할 학생의 이름을 입력해주세요 : ')
            delete_contact(student_list, name)

        # ----- 데이터 정렬 -----
        elif menu == 4:
            sorted_list = sorted(student_list, key=lambda student: student.hakbun) # 이 부분을 이용해 정렬을 하려는데 오류가 납니다.
            print_student(sorted_list)

        else:
            print("종료되었습니다.")
            break

if __name__ == "__main__":
    main()
