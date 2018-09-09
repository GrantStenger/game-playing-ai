import os
import random

BLANK = "_"

class Game:

	def __init__(self):
		self.board = self.makeBoard()
		self.gameOver = False

	def makeBoard(self):
		board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
		return board

	def printBoard(self):
		for row in range(3):
			for column in range(3):
				print(self.board[row][column], end=" ")
			print()

	def play(self, player1, player2):
		turn = player1
		move_num = 0
		while not self.gameOver and move_num != 9:
			os.system('clear')
			self.printBoard()

			hasMoved = False
			while not hasMoved:
				decision = turn.move(self.board)
				if self.move(decision, turn.letter):
					hasMoved = True

			if self.hasWon():
				self.gameOver = True
				break

			# It's now the next player's turn
			if turn == player1:
				turn = player2
			else:
				turn = player1

			# Increment move number
			move_num += 1

		os.system('clear')
		self.printBoard()
		if move_num == 9:
			print("It's a tie!")
		else:
			print(str(turn.letter), "has won!")

	def move(self, decision, letter):
		if self.board[(decision-1)//3][(decision-1)%3] == str(decision):
			self.board[(decision-1)//3][(decision-1)%3] = letter
			return True
		else:
			print("Spot has already been played")
			return False

	def hasWon(self):
		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2]:
				return True
			elif self.board[0][i] == self.board[1][i] == self.board[2][i]:
				return True
			elif self.board[0][0] == self.board[1][1] == self.board[2][2]:
				return True
			elif self.board[2][0] == self.board[1][1] == self.board[0][2]:
				return True
		else:
			return False


class Player:

	def __init__(self, letter):
		self.letter = letter

class HumanPlayer(Player):

	def __init__(self, letter):
		Player.__init__(self, letter)

	def move(self, board):
		decision = input("What move would you like to play? \n")
		return int(decision)

class ComputerPlayer(Player):

	def __init__(self, letter):
		Player.__init__(self, letter)

# This AI plays legal moves randomly
class ComputerPlayerLevel0(ComputerPlayer):

	def __init__(self, letter):
		ComputerPlayer.__init__(self, letter)

	def move(self, board):

		# Find and store all open cells
		open_cells = []
		for row in range(3):
			for col in range(3):
				if board[row][col] == str((row)*3 + (col+1)):
					open_cells.append((row)*3 + (col+1))

		# Play a random legal move
		return open_cells[random.randrange(len(open_cells))]


# This AI can play immeditaly winning moves, but otherwise plays randomly
class ComputerPlayerLevel1(ComputerPlayer):

	def __init__(self, letter):
		ComputerPlayer.__init__(self, letter)

	def move(self, board):

		# Find and store the cells of all legal moves
		open_cells = []
		for row in range(3):
			for col in range(3):
				if board[row][col] == str((row)*3 + (col+1)):
					open_cells.append((row)*3 + (col+1))

		# If any of these moves result in an immediate win, do this. 
		for cell_num in open_cells:

			# Make a copy of the board (do not want to pass by reference)
			new_board = [row[:] for row in board]

			# Check if executing this move will result in a win
			new_board = updateBoard(new_board, cell_num, self.letter)
			if isWinning(new_board, self.letter):
				# If so, execute this move
				return cell_num

		# Play a random legal move
		return open_cells[random.randrange(len(open_cells))]

# This AI blocks the opponent from playing immediately winning moves
# It will also play immediately winning moves for itself, otherwise it plays randomly
class ComputerPlayerLevel2(ComputerPlayer):

	def __init__(self, letter):
		ComputerPlayer.__init__(self, letter)

	def move(self, board):

		# Find and store all open cells
		open_cells = []
		for row in range(3):
			for col in range(3):
				if board[row][col] == str((row)*3 + (col+1)):
					open_cells.append((row)*3 + (col+1))

		# If any of these moves result in an immediate win, do this. 
		for cell_num in open_cells:

			# Make a copy of the board (do not want to pass by reference)
			new_board = [row[:] for row in board]

			# Check if executing this move will result in a win
			new_board = updateBoard(new_board, cell_num, self.letter)
			if isWinning(new_board, self.letter):
				# If so, execute this move
				return cell_num

		# Check if this move creates any immediately winning moves for the opponent
		for cell_num in open_cells:

			# Create the new board that would result in making this legal move
			new_board = [row[:] for row in board]
			new_board = updateBoard(new_board, cell_num, self.letter)

			# Iterate through each of the opponents move, an if they could win, block them.
			opponent_open_cells = []
			for row in range(3):
				for col in range(3):
					if new_board[row][col] == str((row)*3 + (col+1)):
						opponent_open_cells.append((row)*3 + (col+1))
			for opponent_cell_num in opponent_open_cells:
				opponent_new_board = [row[:] for row in new_board]
				opponent_new_board = updateBoard(opponent_new_board, opponent_cell_num, otherLetter(self.letter))
				if isWinning(opponent_new_board, otherLetter(self.letter)):
					return opponent_cell_num

		# Play a random legal move
		return open_cells[random.randrange(len(open_cells))]

# Checks if any board is winning (general function, will fix code structure soon)
def isWinning(board, letter):
	for i in range(3):
		if board[i][0] == board[i][1] == board[i][2] == letter:
			return True
		elif board[0][i] == board[1][i] == board[2][i] == letter:
			return True
		elif board[0][0] == board[1][1] == board[2][2] == letter:
			return True
		elif board[2][0] == board[1][1] == board[0][2] == letter:
			return True
	else:
		return False

def updateBoard(board, cell_num, letter):
	board[(cell_num-1)//3][(cell_num-1)%3] = letter
	return board

def PrintBBoard(board):
	for row in range(3):
		for column in range(3):
			print(board[row][column], end=" ")
		print()

def otherLetter(letter):
	if letter == "X":
		return "O"
	else:
		return "X"

def main():
	game = Game()
	player1 = HumanPlayer("X")
	player2 = ComputerPlayerLevel2("O")
	game.play(player1, player2)

if __name__ == "__main__":
	main()