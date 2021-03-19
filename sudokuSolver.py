

a = list('309000400200709000087000000750060230600904008028050041000000590000106007006000104')


def genBoard(numbers): # creates 3 coordinate identifires for each square
    square = list(''.join([ j*3 for j in ''.join([ i*3 for i in ['ABC', 'DEF', 'GHI']])]))
    return { square.pop(0)+i+str(j): numbers.pop(0) for i in 'abcdefghi' for j in range(1, 10) }


def printBoard(board): # accepts dictionary
	board = ' '.join([ board[key] for key in board.keys() ] )
	for k in range(3):
		for i in range(3):
			print(str(board[0 : 6])+'| '+str(board[6 : 12]+'| '+str(board[12 : 18])))
			board = board[18 : ]
		if k != 2:
			print('------+-------+------')


def checkLegal(board):
    pass


print(genBoard(a))