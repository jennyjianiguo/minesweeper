import random

width = 6
height = 6
bomb_number = 6

# Color Legend
# Code adapted from Stack Overflow
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
class color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# Create color variables for question marks and flags
question = color.RED + "?" + color.ENDC
flag_sign = color.BLUE + '⚑' + color.ENDC

# Create blank solution grid with gutters
def create_solution_grid():
	global solution_grid
	solution_grid = []
	for row in range(height+2):
		solution_grid.append([])
		for col in range(width+2):
			solution_grid[row].append(0)
	change_gutters()

# Create gutters on edges of grid
def change_gutters():
	for row in range(0, height+2):
		solution_grid[row][0] = 5
		solution_grid[row][width+1] = 5
	for column in range(0, width+2):
		solution_grid[0][column] = 5
		solution_grid[height+1][column] = 5

# Print solution grid without gutters
def print_solution_grid():
	print()
	for row in solution_grid[1: height+1]:
		for column in row[1: width+1]:
			print(column, end = ' ')
		print('')

# Create the game grid the user will use
def create_user_grid():
	global user_grid, revealed, first_input
	revealed = 0
	first_input = 0
	user_grid = []
	for row in range(height+2):
		user_grid.append([])
		for col in range(width+2):
			user_grid[row].append(question)
	print_user_grid()
	play_grid()

# Print the grid the user will see (without gutters)
def print_user_grid():
	print('')
	for across in user_grid[1: height+1]:
		for spot in across[1: width+1]:
			print(spot, end = ' ')
		print('')

# User reveals cells in grid
def play_grid():
	count = 0
	user_input = input('''\nEnter the coordinates for the cell you wish to reveal,
and include an 'f' or 'u' for flag/unflag (x y u/f): ''')
	global user_answer, x, y
	user_answer = user_input.split()
	# Ensure input is an integer
	while count == 0:
		try:
			count = +1
			x = int(user_answer[0])
			y = int(user_answer[1])
		except:
			print("\nPlease enter a valid response.")
			play_grid()
	if (len(user_answer) != 2) and (len(user_answer) != 3):
		print("\nPlease enter a valid response.")
		play_grid()
	# User chooses to reveal cell
	if len(user_answer) == 2:
		if (y in range(1, height+1)) and (x in range(1, width+1)):
			global first_input, first_x, first_y
			# Check if it is the user's first input
			if first_input == 0:
				first_x = x
				first_y = y
				first_input += 1
				place_bomb()
				reveal(x,y)
				print_user_grid()
				play_grid()
			else:
				reveal(x,y)
				print_user_grid()
				play_grid()
		else:
			print("\nPlease ensure your coordinates are correct.")
			play_grid()
	# User chooses to flag or unflag
	if len(user_answer) == 3:
		if (y in range(1, height+1)) and (x in range(1, width+1)):
			# User wishes to flag a cell
			if user_answer[2].lower() == "f":
				if user_grid[y][x] != question:
					print("\nYou can only flag unopened cells. Please try again.")
					play_grid()
				else:
					flag(x,y)
			# User wishes to unflag a cell
			if (user_answer[2].lower() == "u"):
				if user_grid[y][x] != flag_sign:
					print("\nYou can only unflag flagged cells. Please try again.")
					play_grid()
				else:
					unflag(x,y)
			else:
				print("\nPlease enter a valid response.")
				play_grid()
		else:
			print("\nPlease ensure your coordinates are correct.")
			play_grid()

# Set up bombs on solution grid
def place_bomb():
	for bomb in range(bomb_number):
		bomb_x = random.randint(1, width)
		bomb_y = random.randint(1, height)
		# Ensure no repeat bombs
		if (solution_grid[bomb_y][bomb_x] != '*') and ((bomb_y != first_y) or (bomb_x != first_x)):
			solution_grid[bomb_y][bomb_x] = '*'
			fill_grid(bomb_y, bomb_x)

# Print numbers surrounding bombs
def fill_grid(bomb_y, bomb_x):
	for y in range(bomb_y-1, bomb_y+2):
		for x in range(bomb_x-1, bomb_x+2):
			if solution_grid[y][x] != '*':
				solution_grid[y][x] +=1

# Reveal user location
def reveal(x,y):
	if user_grid[y][x] != solution_grid[y][x]:
		user_grid[y][x] = solution_grid[y][x]
		check_finish()
		# Reveal surrounding zeros
		if solution_grid[y][x] == 0:
			for y2 in range(-1,2):
				for x2 in range(-1,2):
					if user_grid[y + y2][x + x2] == question:
						reveal(x + x2, y + y2)
		# User reveals bomb
		if user_grid[y][x] == "*":
			end_bomb()
	else:
		print("\nThis cell has already been opened.")

# Flag user location
def flag(x, y):
	user_grid[y][x] = flag_sign
	print_user_grid()
	play_grid()

# Unflag user location
def unflag(x, y):
	user_grid[y][x] = question
	print_user_grid()
	play_grid()

# User reveals a bomb
def end_bomb():
	print("\nOh no! You have revealed a bomb!\nGame over!")
	print_solution_grid()
	play_again()

# User wins game
def check_finish():
	# Checking that the unrevealed cells are all bombs
	hidden = 0
	for y in range(1, height+1):
		for x in range(1, width+1):
			if ((user_grid[y][x]) == question) or (user_grid[y][x] == flag_sign):
				hidden += 1
	if (hidden == bomb_number):
		print("\nCongratulations! You have solved the grid!")
		print_solution_grid()
		play_again()

# Ask user if they would like to restart the game
def play_again():
	once_more = input("\nWould you like to play again (Y/N): ")
	if once_more.lower() == "y":
		main()
	if once_more.lower() == "n":
		print("\nThank you for playing!\n")
		quit()
	else:
		print("\nPlease enter a valid response.")
		play_again()

def main():
	create_solution_grid()
	create_user_grid()

main()