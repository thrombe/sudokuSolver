
import copy

class Square:
    def __init__(self, neighbours, values):
        self.neighbours = neighbours # shove in only empty squares
        self.values = values
    
    def setValue(self, value, blanks, board, used): # sets the value and discards stuff from neighbours attributes and discards itself from blanks
        for neighbour in self.neighbours:
            neighbour.values.discard(value)
            if neighbour.values == set():
                for neighbour in self.neighbours:
                    neighbour.values.add(value)
                    neighbour.neighbours.add(self)
                return False # if no value is suitable for a cell, something went wrong
            neighbour.neighbours.discard(self)
        self.values = value
        used[value] += 1
        blanks.discard(self)
        return True # if nothing went wrong

def genBoard(numbers): # creates 3 coordinate identifires for each square and setup square attributes
    # each coor has 3 parts, 1st is what box is it in, 2nd is x coor, 3rd is y coor. origin in top left
    box = list(''.join([ j*3 for j in ''.join([ i*3 for i in ['ABC', 'DEF', 'GHI']])])) # coor eg: Ac4 - box 1, x coor is 3, y coor is 4
    board =  { box.pop(0) + x + str(y): Square(set(), int(numbers.pop(0))) for y in range(1, 10) for x in 'abcdefghi' } # returns a dict
    blanks = set()
    used = {i : 0 for i in range(1, 10)} # to track the least used number and choose that instead of random ones
    for coord, square in board.items():
        if square.values == 0:
            square.values = set(i for i in range(1, 10))
            for cord, sq in board.items():
                if sq == square: continue
                if coord[0] in cord or coord[1] in cord or coord[2] in cord:
                    if sq.values != 0 and type(sq.values) == type(0): square.values.discard(sq.values) # only leave values that are not in its neighbours
                    if sq.values == 0 or type(sq.values) == type(set()):
                        square.neighbours.add(sq) # shove neighbours into the list
            blanks.add(square)
        else: used[square.values] += 1
    return board, blanks, used

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

def EZsquares(blanks, board, used): # eliminates easy squares with only 1 possible value
    blanksC = blanks.copy() # copy so that it dosent change while loop
    # num, least, maxNei = 10, None, 25 # returns square with least possible values. so that we dont have to try many   - EG
    num, least = 10, None # returns square with least possible values. so that we dont have to try many
    for square in blanksC:
        length = len(square.values)
        if length == 1: # if only 1 possible value for square, then set it
            valueResult = square.setValue(list(square.values)[0], blanks, board, used)
            if valueResult == False: return False
        # elif length < num and len(square.neighbours) < maxNei: least, num, maxNei = square, length, len(square.neighbours) #  - EG
        elif length < num: least, num = square, length
    return least

def EZloop(board, blanks, used): # loops eliminating easy squares till no ez squares left
    length = 0
    while length != len(blanks):
        length = len(blanks)
        valueResult = EZsquares(blanks, board, used)
        if valueResult == False: return False
    if len(blanks) == 0: return board
    return valueResult # passing this for square with least possible values
    
def solve(board, blanks, used): # solves and returns board (a bit randomness is involved. only single solves)
    valueResult = EZloop(board, blanks, used)
    if valueResult == False: return False
    elif type(valueResult) == type({'key': 'val'}): return board
    least = valueResult

    # logic for when every element in blanks has multiple possible values
    leastVal = least.values.copy()
    leastUsed = []
    for i in leastVal:
        pos = used[i]
        if pos > len(leastUsed): leastUsed.append(i)
        else: leastUsed.insert(pos, i)
    for _ in leastVal: # we only have to check if this square has any possible value or not. if this dosent, the board is janked
        val = leastUsed.pop(0)
        neiVal = [nei for nei in least.neighbours if val in nei.values] # record what neighbours used to contain val before guess
        valueResult = least.setValue(val, blanks, board, used) # take a guess at what the value might be
        if valueResult == False: continue # if setValue fails
        
        board['blanks'] = blanks #create a copy of board and blanks for recursion
        boardNew = copy.deepcopy(board)
        board.pop('blanks') # shoved blanks in board just to be able to deepcopy it properly
        blanksNew = boardNew.pop('blanks')
        usedNew = used.copy()
        
        valueResult = solve(boardNew, blanksNew, usedNew)
        if type(valueResult) == type({'key' : 'val'}): return valueResult
        for nei in neiVal: nei.values.add(val) # undo the effects of guessing for backtracking
        used[val] += -1
    return False

def startSolve(numbers):
        board, blanks, used = genBoard(numbers)
        board = solve(board, blanks, used)
        if board != False: return board
        else: print('board is janked')


if __name__ == '__main__':
    
    if True: # for collapsing. numbers defined here
        #a = list('309000400200709000087000000750060230600904008028050041000000590000106007006000104')

        #a = list('517600034289004000346205090602000010038006047000000000090000078703400560000000000')

        # this is arguably the hardest sudoku puzzle (takes a long time if searching for multiple solutions)
        a = list('800000000003600000070090200050007000000045700000100030001000068008500010090000400')

        # literally unsolvable puzzle
        #a = list('000005080000601043000000000010500000000106000300000005530000061000000004000000000')

        #perposely janked example(for multi solution testing)
        #a = list('309000000200709000087000000750060230600904008028050041000000590000106007006000104')

        # for no solution testing
        #a = list('339000400200709000087000000750060230600904008028050041000000590000106007006000104')

        #this one takes 50 some seconds. bring it down to 11 secs to be better than the other guy
        #a = list('....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...'.replace('.', '0'))
    
    import time
    start = time.time()
    board = startSolve(a)
    if board: printBoard(board)
    print(time.time() - start)