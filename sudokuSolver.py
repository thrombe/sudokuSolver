

a = list('309000400200709000087000000750060230600904008028050041000000590000106007006000104')


def genBoard(numbers):
    return { str(i)+str(j): numbers.pop(0) for i in range(1, 10) for j in range(1, 10) }

def checkLegal(board):
    # 3 coordinate system
    #2 coor system

print(genBoard(a))