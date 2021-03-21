
'''
TODO
    sudoku generator - very hard. basically try to solve after removing stuff for single sol puzzles
    more human like method of solving
        store a list of possible values of each square and put the value in if only 1 available. then remove this value from the corresponding lists of squares
        integrate both methods for faster search
    if not previous method, randomise what/ numbers and squares to try
'''

# creates 3 coordinate identifires for each square
def genBoard(numbers): # each coor has 3 parts, 1st is what box is it in, 2nd is x coor, 3rd is y coor. origin in top left
    box = list(''.join([ j*3 for j in ''.join([ i*3 for i in ['ABC', 'DEF', 'GHI']])])) # coor eg: Ac4 - box 1, x coor is 3, y coor is 4
    return { box.pop(0) + x + str(y): numbers.pop(0) for y in range(1, 10) for x in 'abcdefghi' } # returns a dict

# prints the board
def printBoard(board, playing = 'no'): # accepts dictionary, playing set to yes if its not an autosolve. ie player is playing
    board = ' '.join([ board[key] for key in board.keys() ] ) # making a string(with space in between) out of values from dict
    if playing == 'yes': print('   a b c   d e f   g h i\n')
    num = 0
    for k in range(3):
        for i in range(3):
            if playing != 'yes': num = ' '
            else: num += 1
            print(str(num) + '  ' + str(board[0 : 6])+'| '+str(board[6 : 12]+'| '+str(board[12 : 18])))
            board = board[18 : ]
        if k != 2:
            print('   ------+-------+------')


def checkLegal(board, coor, number):
    for id in coor: # next line returns true or false to the var after checking for vertical, horizontal, in box legallity of the move
        legal = number not in [ board[key] for key in board.keys() if id in key]
        if not legal: return False # returning false if its not legal in any single way
    return legal

# gives a list of coords without a true value
def giveBlanks(board):
    return [coor for coor in board if board[coor] == '0']

# solves sudoku
def solve(board, blanks, solves, multiple = 'single'):
    for coor in blanks:
        for number in range(1, 10):
            if checkLegal(board, coor, str(number)) == True:
                boardNew = board.copy()
                boardNew[coor] = str(number) # if move is legal, copy board and blanks to edit them and then pass to next in recursion
                blanksNew = blanks.copy()
                blanksNew.remove(coor)
                if blanksNew == []: return boardNew # if blanksNew has no values, the board is solved
                result = solve(boardNew, blanksNew, solves, multiple)
                if result != False:
                    if multiple != 'single': solves.append(result) # appending all solutions if multisolve is on
                    else: return result # if multi solve is off
        if board[coor] == '0': return False # if the value remains 0, then the pervious steps were wrong
    return solves # this line dosent really get executed, it always returns earlier
            
# numbers should be a list of 81 str(numbers) and multiple == 'single'(or leave blank) for only 1 output, multiple != 'single' for all possible outputs (this may take quite a bit of time(depending on how many squares have 0 value))
def actuallySolve(numbers, multiple = 'single'):
    solves = []  # couldnt figure out how to return all solutions from main func. so had to make a blank list to which i append sols to
    board = genBoard(numbers)
    printBoard(board)
    print('\n')
    blanks = giveBlanks(board)
    board = solve(board, blanks, solves, multiple)
    errmsg = 'board is janked m8, try another'
    if multiple != 'single':
        if solves == [] : # if board has no solution
            print(errmsg)
            return
        print('solutions:'+'\n')
        for board in solves: # printing all sols
            printBoard(board)
            print('\n')
        print(f'total {len(solves)} solutions')
    else:
        if board == False:
            print(errmsg)
            return
        printBoard(board)
    return solves #returns a list of dict of all solutions


def play(numbers):
    print('''
welcome to sudoku.play, 
you can only edit values of squares which are originally 0
to edit your previous misplays, first set the required coord to 0
''')
    board = genBoard(numbers)
    printBoard(board, 'yes')
    print('\n')
    blanks = giveBlanks(board)
    illegalError = 'illegal move. fbi is on the way'
    while True:
        while True:
            coor = input('input coordinate: ')
            for key in board.keys():
                if coor in key: coor = key
            if coor in blanks:
                number = input('input value: ')
                if number != '0': legal = checkLegal(board, coor, number)
                else: legal = True
                if not legal: print(illegalError)
                else: break
            else: print('\n coords should be like c4 for x = 3 and y = 4 \n and should also not be one of the originally filled coords \n (origin top left)(first element = a1) \n')
        board[coor] = number
        print('\n')
        printBoard(board, 'yes')
        print('\n')
        if giveBlanks(board) == []: break
    print('you solved it!!')


if __name__ == '__main__':
    
    #a = list('309000400200709000087000000750060230600904008028050041000000590000106007006000104')

    a = list('517600034289004000346205090602000010038006047000000000090000078703400560000000000')

    # this is arguably the hardest sudoku puzzle (takes a long time if searching for multiple solutions)
    #a = list('800000000003600000070090200050007000000045700000100030001000068008500010090000400')

    # literally unsolvable puzzle
    #a = list('000005080000601043000000000010500000000106000300000005530000061000000004000000000')

    #perposely janked example(for multi solution testing)
    #a = list('309000000200709000087000000750060230600904008028050041000000590000106007006000104')

    # for no solution testing
    #a = list('339000400200709000087000000750060230600904008028050041000000590000106007006000104')
    
    #import time
    #start = time.time()
    actuallySolve(a, 'single') # to auto-solve
    #play(a) # to play
    #print(str(time.time()-start))