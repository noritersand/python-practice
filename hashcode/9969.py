money = 0
while True:
    num = int(input("메뉴를 선택하세요 :"))
    if num == 1:
        money2 = int(input("예금액 :"))
        money = money + money2
    elif num == 2:
        money3 = int(input("출금액 :"))
        while money3 > money:
            money3 =int(intput)
            money3 =int(input("출금액 :"))
            money = money - money3
    elif num ==3:
        print("잔고 :",money)
    elif num == 4:
        print("프로그램종료")
        break