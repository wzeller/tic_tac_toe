import random
from random import randrange

def transpose(board):
	new_board = [[None, None, None], [None, None, None], [None, None, None]]
	for x in xrange(0,3):
		for y in xrange(0,3):
			new_board[y][x] = board[x][y]
	return new_board


def eval_board(board):
	"""
	Takes a board (format [['x','x', None], ['o', 'o', 'x'], [None, None, None]]) 
	and returns None if no result, 'x' if 'x' won, 'o' if 'o'
	won, and 'd' if drawn
	"""

	# Test for fewer than 5 moves, as cannot win until 6th move
	total_str = ''
	for row in board:
 		for el in row:
 			if el:
				total_str += el
	if len(total_str) < 5:
		return None

	x_win = ['x', 'x', 'x']
	o_win = ['o', 'o', 'o']

	# Test rows
	for row in board:
		if row == x_win: return 'x' 
		if row == o_win: return 'o' 
			
	# Test columns
	for row in transpose(board):
		if row == x_win: return 'x' 
		if row == o_win: return 'o' 

	# Test diagonals
	if ([board[0][0], board[1][1], board[2][2]] == x_win or 
		[board[0][2], board[1][1], board[2][0]] == x_win):
		return 'x'
	if ([board[0][0], board[1][1], board[2][2]] == o_win or 
		[board[0][2], board[1][1], board[2][0]] == o_win):
		return 'o'

	# No win and full board is a draw
	if len(total_str) == 9:
		return 'd'

def get_blanks(board):
	"""
	Returns a list of coordinates for all open squares on a board
	"""
	blanks = []
	for x in xrange(0,3):
		for y in xrange(0, 3):
			if board[x][y] == None:
				blanks.append([x, y])
	return blanks

class Node(object):
	"""
	A Node captures all the state of any given tic-tac-toe
	position, including the moves thus far, the current board
	and whose turn it is.  There are some methods for printing
	as well as getting the blank squares of the position.
	"""

	def __init__(self, board, turn):
		self.board = board
		self.turn = turn
		self.history = []

	def copy_history(self, history):
		self.history = history

	def add_to_history(self, node):
		self.history.append(node)

	def print_board(self, board=None):
		if board:
			print_board = board
		else:
			print_board = self.board
		for row in print_board:
			first, second, third = row[0], row[1], row[2]
			if not first: first = "_"
			if not second: second = "_"
			if not third: third = "_"
			print "%s %s %s" % (first, second, third)
		print "\n"

	def print_history(self):
		for b in self.history:
			self.print_board(b)

	def evaluate(self):
		return eval_board(self.board)

	def blank_squares(self):
		return get_blanks(self.board)

	def make_move(self, move):
		self.board[move[0]][move[1]] = self.turn
		if self.turn == 'x':
			self.turn = 'o'
		else:
			self.turn = 'x'

	def make_random_move(self):
		squares = self.blank_squares()
		idx = randrange(0,len(squares))
		move = squares[idx]
		self.make_move(move)

	def stringify_board(self):
		string = ""
		for row in self.board:
			for el in row:
				if el:
					string += el
				else:
					string += "_"
		return string 

	def num_moves(self):
		return 9 - len(self.blank_squares())

new_board  = [[None, None, None], [None, None, None], [None, None, None]]
new_board_clone = [x[:] for x in new_board]
turn = 'x'
start_node = Node(new_board_clone, turn)
nodes_to_process = [start_node]
x_wins = 0
o_wins = 0
draws = 0
total_length = 0
finished_games = []
distinct_outcomes = {}

# Perform depth-first search through all possible moves, tabulating
# a result if the game concludes, otherwise adding nodes representing
# all possible next moves and adding them to the processing queue
while len(nodes_to_process):
	node = nodes_to_process.pop()
	result = node.evaluate()
	if result:
		if result == 'x':
			x_wins += 1
		elif result == 'o':
			o_wins += 1
		elif result == 'd':
			draws += 1
		else:
			raise Error

		# Keep the finished game positions to view how they
		# unfolded
		finished_games.append(node)
		total_length += node.num_moves()

		# Get a hashable representation of the final board, add
		# it to the dict if it doesn't already exist
		board_string = node.stringify_board()
		outcome_exists = distinct_outcomes.get(board_string, None)
		if not outcome_exists:
			distinct_outcomes[board_string] = 1
		else:
			distinct_outcomes[board_string] += 1
	else:

		# Make new nodes for all possible moves based on 
		# blank squares for current position
		for blank in node.blank_squares():

			#clone board and history from current state
			board = [x[:] for x in node.board]
			board_clone = [x[:] for x in board]
			history = [x[:] for x in node.history]

			# Make new state and make move to empty square
			new_node = Node(board, node.turn)
			
			# Track history of position to be able to see 
			# progression of moves after game is over
			new_node.copy_history(history)
			new_node.add_to_history(board_clone)

			new_node.make_move(blank)

			# Add new position to the queue to process
			nodes_to_process.append(new_node)

print 'average num moves in total', float(total_length)/len(finished_games)
print 'total x wins:', x_wins, float(x_wins)/len(finished_games)
print 'total o wins:', o_wins, float(o_wins)/len(finished_games)
print 'total draws:', draws, float(draws)/len(finished_games)

total_possible_games = x_wins + o_wins + draws

# Start with a blank board and 'x' going first, move randomly till game over
new_board  = [[None, None, None], [None, None, None], [None, None, None]]
new_board_clone = [x[:] for x in new_board]
turn = 'x'
start_node = Node(new_board_clone, turn)
nodes_to_process = [start_node]
x_wins = 0
o_wins = 0
draws = 0
finished_simul_games = []
total_length = 0

# Simulate as many games as run above to completion and look at percentage of x wins, 
#o wins and draws
while len(finished_simul_games) <= total_possible_games:
	result = start_node.evaluate()
	if result:
		if result == 'x':
			x_wins += 1
		elif result == 'o':
			o_wins += 1
		elif result == 'd':
			draws += 1
		else:
			raise Error
		finished_simul_games.append(start_node)
		total_length += start_node.num_moves()
		new_board_clone = [x[:] for x in new_board]
		start_node = Node(new_board_clone, turn)
	else:
		start_node.make_random_move()

total = len(finished_simul_games)

print 'average num moves in simul', float(total_length)/total
print 'simulated x wins:', x_wins, float(x_wins)/total
print 'simulated o wins:', o_wins, float(o_wins)/total
print 'simulated draws:', draws, float(draws)/total



