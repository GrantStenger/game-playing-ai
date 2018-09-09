import os

BLANK = "_"

class Game:

	def __init__(self):
		self.board = self.makeBoard()
		self.gameOver = False

	def makeBoard(self):
		board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
		return board

	def printBoard(self):
		for i in range(len(self.board)):
			for j in range(len(self.board)):
				print(self.board[i][j], end=" ")
			print()

	def play(self, player1, player2):
		turn = player1
		while not self.gameOver:
			os.system('clear')
			self.printBoard()

			hasMoved = False
			while not hasMoved:
				decision = turn.move(self.board)
				if self.move(decision, turn.color):
					hasMoved = True

			if self.hasWon():
				self.gameOver = True

			# It's now the next player's turn
			if turn == player1:
				turn = player2
			else:
				turn = player1

		os.system('clear')
		self.printBoard()
		print(str(turn.color), "has won!")

	def move(self, decision, color):
		if self.board[(decision-1)//3][(decision-1)%3] == str(decision):
			if color == "white":
				self.board[(decision-1)//3][(decision-1)%3] = "X"
			else:
				self.board[(decision-1)//3][(decision-1)%3] = "O"
			return True
		else:
			print("Spot has already been played")
			return False

	def hasWon(self):
		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2] or self.board[0][i] == self.board[1][i] == self.board[2][i] or self.board[0][0] == self.board[1][1] == self.board[2][2] or self.board[2][0] == self.board[1][1] == self.board[0][2]:
				return True
			else:
				return False
		self.gameOver == True

class HumanPlayer:

	def __init__(self, color):
		self.color = color

	def move(self, board):
		decision = input("What move would you like to play? \n")
		return int(decision)

class ComputerPlayer:

	def __init__(self):
		self.name = "computer"

def main():
	game = Game()
	player1 = HumanPlayer("white")
	player2 = HumanPlayer("black")
	game.play(player1, player2)
	# game.printBoard()


if __name__ == "__main__":
	main()