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

	def __init__(self, board, turn):
		self.board = board
		self.turn = turn

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


board  = [[None, None, None], [None, None, None], [None, None, None]]
turn = 'x'
start_node = Node(board, turn)
nodes_to_process = [start_node]
x_wins = 0
o_wins = 0
draws = 0

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
	else:

		# Make new nodes for all possible moves based on 
		# blank squares for current state
		for blank in node.blank_squares():

			#clone board from current state
			board = [x[:] for x in node.board]

			# Make new state and make move to empty square
			new_node = Node(board, node.turn)
			new_node.make_move(blank)

			# Add new state to the queue to process
			nodes_to_process.append(new_node)

print 'x', x_wins
print 'o', o_wins
print 'd', draws




