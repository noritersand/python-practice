class Stack:
    def __init__(self):
        self.items = []

    def push(self, val):
        self.items.append(val)

    def pop(self):
        try:
            return self.items.pop()
        except IndexError:
            print("Stack is empty")
    def top(self):
        try:
            return self.items[-1]
        except IndexError:
            print("Stack is empty")

    def __len__(self):
        return len(self.items)

    def isEmpty(self):
        return self.__len__() == 0  

def get_token_list(expr):
    opstack = Stack()
    outstack = []
    token_list = expr

    for token in token_list:
        print(token)
        if token == '(':
            opstack.push(token)
        elif token == ')':
            opstack.push(token)
        elif token in '+-/*^': #opstack에 자기 자신보다 우선순위 높은 연산자 pop하기
            #while (not opstack.isEmpty()) and \
            #(prec[opstack.top()] >= prec[token]):
            #outstack.append(opstack.pop())
                #print(outstack)
                # print(opstack)
            opstack.push(token)
        elif token in '.':
            outstack.append(opstack.top()+token)
            opstack.push(token)
        elif opstack.pop() == '.':  # . 일때
            outstack.append(opstack.pop()+opstack.top()+token)
        opstack.push(token)

        #outstack.append(opstack.top())
        #if outstack in '.':
        #    outstack.append(str(opstack.pop()+'.'+opstack.pop()))
    outstack.append(opstack.pop())
    return print(outstack)

##expr = input()
expr = '1+2+3'
value = get_token_list(expr)

