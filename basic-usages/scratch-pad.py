foo = 'foo'

def fn():
    return 'bar'

print(fn())

# 클래스 정의
class MyClass:
    # 초기화 메서드
    def __init__(self, name):
        self.name = name  # 속성 정의

# 클래스의 인스턴스 생성
myInst = MyClass("John")
print(myInst.name) # John

from module.my_module import MyClass


def fn(a, b):
    print(a, b)

dic = {'a': 1, 'b': 2}

# 딕셔너리를 언패킹하여 함수 인자로 전달
fn(**dic)
