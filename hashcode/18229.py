import random


def choosePlayer():
    print('대문자 영문자 X 또는 O 입력')
    while True:
        chosen = input('대문자 영문자 X 또는 O 입력')
        if chosen != 'O' and chosen != 'X':
            print('영문자 O 또는 X를 다시 입력하세요.')
            continue
        elif chosen == 'O':
            return 'O', 'X'
        elif chosen == 'X':
            return 'X', 'O'


def drawingBoard(screen):
    print()
    print('____________________________________________')
    print(' '+screen[6]+' '+'|'+' '+screen[7]+' '+'|'+' '+screen[8])
    print('____________________________________________')
    print(' '+screen[3]+' '+'|'+' '+screen[4]+' '+'|'+' '+screen[5])
    print('____________________________________________')
    print(' '+screen[0]+' '+'|'+' '+screen[1]+' '+'|'+' '+screen[2])
    print('____________________________________________')
    print()


def putPlayerStone(screen, mark):
    while True:
        print('>>돌 위치 선택: ', end='')  # end=''는 하나의 명령어이다
        position = input()
        if position not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            continue
        if screen[int(position)-1] != '':
            continue
        else:
            break
    screen[int(position)-1] = mark
    return position, screen


def putAIStone(screen, player, AI):
    AI_willPut_here = []

    Put_player = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 9):
        if player == screen[i]:
            Put_player[i] = True

    Put_AI = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 9):
        if AI == screen[i]:
            Put_AI[i] = True

    hldx = 8
    while hldx >= 2:
        if Put_AI[hldx - 1] == True:
            if Put_AI[hldx - 1-1] == True:
                AI_willPut_here.append(hldx - 1+1)
            elif Put_player[hldx-1+1] == True:
                AI_willPut_here.append(hldx - 1-1)
        elif Put_AI[hldx - 1-1] == True and Put_AI[hldx - 1+1] == True:
            AI_willPut_here.append(hldx - 1)
        hldx -= 3

        vldx = 4

    while vldx <= 6:
        if Put_AI[vldx - 1] == True:
            if Put_AI[vldx-1+3] == True:
                AI_willPut_here.append(vldx - 1-3)
            elif Put_AI[vldx - 1-3] == True:
                AI_willPut_here.append(vldx - 1+3)
        elif Put_AI[vldx - 1+3] == True and Put_AI[vldx - 1-3] == True:
            AI_willPut_here.append(vldx - 1)
        vldx += 1

        if Put_AI[5-1] == True:
            if Put_AI[7-1] == True:
                AI_willPut_here.append(3-1)
            elif Put_AI[7-1] == True:
                AI_willPut_here.append(3-1)
            elif Put_AI[7-1] == True:
                AI_willPut_here.append(3-1)
            elif Put_AI[7-1] == True:
                AI_willPut_here.append(3-1)
        if Put_AI[7-1] == True and Put_AI[3-1] == True:
            AI_willPut_here.append(5-1)
        if Put_AI[9-1] == True and Put_AI[1-1] == True:
            AI_willPut_here.append(5-1)

    for i in range(0, len(AI_willPut_here)):
        if screen[AI_willPut_here[i]] == '':
            available.append(AI_willPut_here[i])
    available = random.choice(available)
    screen[int(available)] = AI
    return screen


def checkWinner(screen, player, AI):
    playerPut = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0.9):
        if player == screen[i]:
            playerPut[i] = True
    vldx = 7
    while vldx <= 9:
        if playerPut[vldx-1] == True and playerPut[vldx-1-3] == True and playerPut[vldx-1-6] == True:
            playerWin(screen)
            return True
        vldx += 1

    hldx = 7
    while hldx >= 1:
        if playerPut[hldx-1] == True and playerPut[hldx-1+1] == True and playerPut[hldx-1+2] == True:
            playerWin(screen)
            return True
        hldx -= 3

        if playerPut[7-1] == True and playerPut[5-1] == True and playerPut[3-1] == True:
            playerWin(screen)
            return True
        elif playerPut[9-1] == True and playerPut[5-1] == True and playerPut[1-1] == True:
            playerWin(screen)
            return True

    for i in range(0, 9):
        if screen[i] == '':
            break
        elif i == 8:
            drawingGameScreen(screen)
            print('무승부')
            return True


if __name__ == "__main__":
    while True:
        gameScreen = [",", ",", ",", ",", ""]
        player, AI = choosePlayer()
        drawingBoard(gameScreen)

        if player == 'X':
            while True:
                putPlayerStone(gameScreen, player)
                checkWinner(gameScreen, player, AI)
                drawingBoard(gameScreen)
                putAIStone(gameScreen, player, AI)
                checkWinner(gameScreen, player, AI)
                drawingBoard(gameScreen)