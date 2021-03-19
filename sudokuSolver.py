

a = list('309000400200709000087000000750060230600904008028050041000000590000106007006000104')

#a = list('800000000003600000070090200050007000000045700000100030001000068008500010090000400')

#a = list('517600034289004000346205090602000010038006047000000000090000078703400560000000000')

#perposely janked example(for multi solution testing)
a = list('309000000200709000087000000750060230600904008028050041000000590000106007006000104')

# creates 3 coordinate identifires for each square
def genBoard(numbers): # each coor has 3 parts, 1st is what box is it in, 2nd is x coor, 3rd is y coor. origin in top left
    box = list(''.join([ j*3 for j in ''.join([ i*3 for i in ['ABC', 'DEF', 'GHI']])])) # coor eg: Ac4 - box 1, x coor is 3, y coor is 4
    return { box.pop(0) + x + str(y): numbers.pop(0) for y in range(1, 10) for x in 'abcdefghi' } # returns a dict

# prints the board
def printBoard(board): # accepts dictionary
    if board == False: # if board dosent have a solution
        print('board is janked m8, try another')
        return
    board = ' '.join([ board[key] for key in board.keys() ] ) # making a string(with space in between) out of values from dict
    for k in range(3):
        for i in range(3):
            print(str(board[0 : 6])+'| '+str(board[6 : 12]+'| '+str(board[12 : 18])))
            board = board[18 : ]
        if k != 2:
            print('------+-------+------')


def checkLegal(board, coor, number):
    for id in coor: # next line returns true or false to the var after checking for vertical, horizontal, in box legallity of the move
        legal = number not in [ board[key] for key in board.keys() if id in key]
        if not legal: return False # returning false if its not legal in any single way
    return legal

# gives a list of coords without a true value
def giveBlanks(board):
    return [coor for coor in board if board[coor] == '0']

# solves sudoku
def solve(board, blanks, solves):
    for coor in blanks:
        for number in range(1, 10):
            if checkLegal(board, coor, str(number)) == True:
                boardNew = board.copy()
                boardNew[coor] = str(number) # if move is legal, copy board and blanks to edit them and then pass to next in recursion
                blanksNew = blanks.copy()
                blanksNew.remove(coor)
                if blanksNew == []: return boardNew # if blanksNew has no values, the board is solved
                result = solve(boardNew, blanksNew, solves)
                if result != False: solves.append(result)
        if board[coor] == '0': return False # if the value remains 0, then the pervious steps were wrong
    return solves
            
        
def actuallySolve(numbers):
    solves = []  # couldnt figure out how to return all solutions from main func. so had to make a blank list to which i append sols to
    board = genBoard(a)
    printBoard(board)
    print('\n')
    blanks = giveBlanks(board)
    solve(board, blanks, solves)
    print('solutions:'+'\n')
    for board in solves: # printing all sols
        printBoard(board)
        print('\n')
    print(f'total {len(solves)} solutions')
    return solves #returns a list of dict of all solutions


actuallySolve(a)