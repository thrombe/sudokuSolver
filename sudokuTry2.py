
'''
TODO
    sudoku generator - very hard. basically try to solve after removing stuff for single sol puzzles
    more human like method of solving
        store a list of possible values of each square and put the value in if only 1 available. then remove this value from the corresponding lists of squares
        integrate both methods for faster search
    if not previous method, randomise what/ numbers and squares to try

text
    create square objects
    square.hori, square.vert, square.box, square.values, 
    if a value is confirmed, remove that value from all objects from square.hori,vert,box
    how to try values that we cant confirm? (no square.values has just 1 value left):
        copy.copy() objects in a recursive function
    while removing values from square.values, check if only 1 value remaining. and maybe also 2 and 3 for priority
    maintain list of empty squares for loop (was already doing this)

    how this helps?:
        dont have to loop through all squares just to check the if it lies in same box etc
        square.values would all for checking only useful values and not check if its valid
'''
import copy

def legal(board, square, val):
    for coor, sq in board.items():
        if sq == square: break
    for coor2, sq in board.items():
        if coor[0] in coor2 or coor[1] in coor2 or coor[2] in coor2:
            if type(sq.values) == type(0):
                if val == sq.values: return False
    return True


class Square:
    def __init__(self, neighbours, values):
        self.neighbours = neighbours # shove in only empty squares
        self.values = values
    
    def setValue(self, value, blanks, board): # sets the value and discards it from neghbour's values
        #print(self.values)#
        if not legal(board, self, value): return False
        self.values = value
        blanks.remove(self)
        for neighbour in self.neighbours:
            neighbour.values.discard(value)
            if neighbour.values == set():
                #print('fal1')####
                return False # if no value is suitable for a cell, something went wrong
            neighbour.neighbours.discard(self)
        return True # if nothing went wrong

def genBoard(numbers): # creates 3 coordinate identifires for each square and setup square attributes
    # each coor has 3 parts, 1st is what box is it in, 2nd is x coor, 3rd is y coor. origin in top left
    box = list(''.join([ j*3 for j in ''.join([ i*3 for i in ['ABC', 'DEF', 'GHI']])])) # coor eg: Ac4 - box 1, x coor is 3, y coor is 4
    board =  { box.pop(0) + x + str(y): Square(set(), int(numbers.pop(0))) for y in range(1, 10) for x in 'abcdefghi' } # returns a dict
    blanks = set()
    for coord, square in board.items():
        if square.values == 0:
            square.values = set(i for i in range(1, 10))
            for cord, sq in board.items():
                if sq == square: continue
                if coord[0] in cord or coord[1] in cord or coord[2] in cord:
                    if sq.values != 0 and type(sq.values) != type(set()): square.values.discard(sq.values) # only leave values that are not in its neighbours
                    if sq.values == 0 or type(sq.values) == type(set()):
                        square.neighbours.add(sq) # shove neighbours into the list
            blanks.add(square)
    return board, blanks

def printBoard(board, playing = 'no'): # prints the board
    # accepts dictionary, playing set to yes if its not an autosolve. ie player is playing
    board = ' '.join([ str(square.values) for square in board.values() ] ) # making a string(with space in between) out of values from dict
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

def EZsquares(blanks, board): # eliminates easy squares with only 1 possible value
    blanksC = blanks.copy() # so that it dosent change while loop
    for square in blanksC:
        length = len(square.values)
        if length == 1:
            valueResult = square.setValue(list(square.values)[0], blanks, board)
            if valueResult == False:
                #print('fal2')###
                return False
    return True

def EZloop(board, blanks): # loops eliminating easy squares till no ez squares left
    length = 0
    while length != len(blanks):
        length = len(blanks)
        valueResult = EZsquares(blanks, board)
        if valueResult == False:
            #print('fal3')###
            return False
    if len(blanks) == 0:
        #print('bor3')
        return board

def solve(board, blanks, mainSolve = 0):
    #######
    #print(len(blanks))###
    if len(blanks) == 0:
        printBoard(board)###
        #return board
    ########

    valueResult = EZloop(board, blanks)
    if valueResult == False: 
        #print('fal4')###
        return False
    elif type(valueResult) == type({'key': 'val'}):
        #print('bor4')###
        return board

    #return board##
    # logic for when every element in blanks has multiple possible values
    num = 10
    for square in blanks: # shift this inside EZsquares
        if len(square.values) < num:
            least = square
            num = len(square.values)
    #print(least.values)##

    leastVal = least.values.copy()
    for val in leastVal:
        valueResult = least.setValue(val, blanks, board) # take a guess at what the value might be
        if valueResult == False: continue
        boardNew = copy.deepcopy(board)
        blanksNew = set()
        num = 10
        for square in boardNew.values(): #create a copy of board and blanks
            if type(square.values) == type(set()): blanksNew.add(square)
        valueResult = solve(boardNew, blanksNew)
        #if valueResult == False: return False
        if type(valueResult) == type({'key' : 'val'}):
            print('bor5', len(valueResult))###
            printBoard(valueResult)###
            return valueResult
        for neighbour in least.neighbours: # undo the guess we took
            neighbour.values.add(val)
        blanks.add(least)
        least.values = leastVal
    #print('fal6')###
    return False

    

if __name__ == '__main__':
    
    if True: # for collapsing. numbers defined here
        a = list('309000400200709000087000000750060230600904008028050041000000590000106007006000104')

        #a = list('517600034289004000346205090602000010038006047000000000090000078703400560000000000')

        # this is arguably the hardest sudoku puzzle (takes a long time if searching for multiple solutions)
        a = list('800000000003600000070090200050007000000045700000100030001000068008500010090000400')

        # literally unsolvable puzzle
        #a = list('000005080000601043000000000010500000000106000300000005530000061000000004000000000')

        #perposely janked example(for multi solution testing)
        #a = list('309000000200709000087000000750060230600904008028050041000000590000106007006000104')

        # for no solution testing
        #a = list('339000400200709000087000000750060230600904008028050041000000590000106007006000104')
    
    import time
    start = time.time()

    def sob():
        board, blanks = genBoard(a)
        board = solve(board, blanks, 1)
    
    board = sob()
    #printBoard(board)
    #for s in board.values(): print(s.values)####
    #printBoard(board)
    print(time.time() - start)