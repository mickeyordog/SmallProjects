import numpy as np
import math

gameboard = np.array([['1','2','3'],
					  ['4','5','6'],
					  ['7','8','9']])


usingComputer = True #whether computer should play as opponent

isPlaying = True
stage = 0 #0 for setup, 1 for player turn, 2 for opponent turn

boardLines = "     |     |    "
def drawBoard(board):
	for i in range(np.size(board, 0)):
		print(boardLines)
		print(f'  {board[i][0]}  |  {board[i][1]}  |  {board[i][2]}')
		print(boardLines)
		if i < np.size(board, 0) - 1:
			print("-----------------")

def initGame():
	letter = ""
	while not (letter == 'X' or letter == 'O'):
		letter = input("Do you want to be x or o? ").upper()
	
	global player
	global opponent
	global usingComputer
	player = letter
	if player == "O":
		opponent = "X"
	else:
		opponent = "O"
	result = ""
	while not (result == "Y" or result == "N"):
		result = input("Do you want to play against the computer? (Y or N) ").upper()
	usingComputer = (result == "Y")
	print("Playing against " + ("computer" if usingComputer else "another person"))

#index is num 1-9, character is x or o, returns false if another move is already there
def fillSquare(index, character, board):
	row = int((index - 1)/ 3)
	col = (index - 1) % 3
	if board[row][col] == "X" or board[row][col] == "O":
		return False
	board[row][col] = character
	return True

#fills the nth empty space, returns index of filled square
def fillEmpty(index, character, board):
	count = 0
	for x in range(3):
		for y in range(3):
			if not (board[x][y] == player or board[x][y] == opponent):
				if (count == index):
					fillSquare(3 * x + y + 1, character, board)
					return 3 * x + y + 1
				count += 1

def countNumEmpty(board):
	count = 0
	for x in range(3):
		for y in range(3):
			if not (board[x][y] == player or board[x][y] == opponent):
				count += 1
	return count

def playTurn(whichPlayer, board):
	result = False
	while not result:
		num = input(f"Enter the number where you want to play an {whichPlayer}: ")
		if num not in '0 1 2 3 4 5 6 7 8 9'.split():
			continue
		result = fillSquare(int(num), whichPlayer, board)

def computerTurn(board):
	global count
	count = 0
	index = minimax(board, 0, True)
	print(f"CPU searched {count} possible end states")
	fillSquare(index, opponent, board)
	print(f"CPU played an {opponent} at ", index)

#not sure best way to get best move out of this, added startingDepth
def minimax(board, depth, isMaximizer):
	global count #number of times run in one session
	winner = checkGameIsOver(board)
	if not winner == False:
		count += 1
		if winner == player:
			return -10 + depth
		elif winner == opponent:
			return 10 - depth
		else:
			return 0
	if isMaximizer:
		maxEval = -math.inf
		for i in range(countNumEmpty(board)):
			boardCopy = np.copy(board)
			index = fillEmpty(i, opponent, boardCopy)
			eval = minimax(boardCopy, depth + 1, False)
			if (eval > maxEval):
				maxEval = eval
				bestIndex = index
		if depth == 0:
			return bestIndex
		return maxEval
	else:
		minEval = math.inf
		for i in range(countNumEmpty(board)):
			boardCopy = np.copy(board)
			fillEmpty(i, player, boardCopy)
			eval = minimax(boardCopy, depth + 1, True)
			minEval = min(eval, minEval)
		return minEval

#this is an unintuitive function, should have made one to check if game over, then 
#another to check winner
def checkGameIsOver(board):
	for i in range(3):
		#check horizontals
		if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
			return board[i][0]
		#check verticals
		if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
			return board[0][i]

	#check diagonals
	if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
		return board[0][0]
	if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
		return board[0][2]

	#check draw (board full but no winner)
	for x in range(3):
		for y in range(3):
			if not (board[x][y] == player or board[x][y] == opponent):
				return False
				#meaning that the game is still going
	return "No one" #means that it was a draw

drawBoard(gameboard)
while isPlaying:
	global winner
	if stage == 0:
		initGame()
		stage = 1

	elif stage == 1:
		playTurn(player, gameboard)
		drawBoard(gameboard) 
		winner = checkGameIsOver(gameboard)
		if not winner == False:
			isPlaying = False
		else:
			stage = 2

	elif stage == 2:
		if usingComputer:
			computerTurn(gameboard)
		else:
			playTurn(opponent, gameboard)
		drawBoard(gameboard)
		winner = checkGameIsOver(gameboard)
		if not winner == False:
			isPlaying = False
		else:
			stage = 1

print(f'{winner} wins!')