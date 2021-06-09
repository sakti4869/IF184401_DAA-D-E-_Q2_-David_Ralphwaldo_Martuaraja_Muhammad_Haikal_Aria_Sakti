# Minesweeper game

import sys
import random
import pygame

# Cell class

class Cell:
	def __init__(self):
		self.isMine = False
		self.numMines = 0
		self.open = False
		self.flagged = False

# Grid class

class Grid:
	def __init__(self, width, height):
		self.grid = None # The cells array
		self.size = None # Width and height of the grid
		self.created = False # Has the grid been filled with mines?
		self.cellsLeft = 0 # Number of cells left to be opened to win the game
		self.time = 0 # Game time in seconds
		self.timeTimer = 0 # Timer for counting game time
		self.state = 0 # 0 - Playing, 1 - Game won, 2 - Game lost
		self.minesCount = 0 # Maximum number of mines
		self.minesLeft = 0 # Number of mines left unflagged

		self.generate(width, height)

	# Function to create the grid array

	def generate(self, width, height):
		self.grid = []
		self.size = (width, height)

		for i in range(height):
			temp = []

			for j in range(width):
				temp.append(Cell())

			self.grid.append(temp)

	# Function to set the maximum number of mines for the grid

	def setMinesCount(self, minesCount):
		self.minesCount = minesCount

	# Function to reset the grid

	def reset(self):
		for i in range(self.size[1]):
			for j in range(self.size[0]):
				self.grid[i][j].isMine = False
				self.grid[i][j].numMines = 0
				self.grid[i][j].open = False
				self.grid[i][j].flagged = False

		self.created = False
		self.state = 0
		self.time = 0

	# Function to create mines on the grid at random locations

	def fillMines(self, clickPos):
		if self.grid == None:
			print('Grid has not been generated!')

		addedMines = 0

		while addedMines < self.minesCount:
			cellX = random.randint(0, self.size[0] - 1)
			cellY = random.randint(0, self.size[1] - 1)

			if self.grid[cellY][cellX].isMine == False:
				if (cellX, cellY) != clickPos:
					self.grid[cellY][cellX].isMine = True
					addedMines += 1

		# Update adjacent mine cells count for each cell

		for i in range(self.size[1]):
			for j in range(self.size[0]):
				if self.isMine(j, i) == 0:
					self.grid[i][j].numMines  = self.isMine(j - 1, i - 1)
					self.grid[i][j].numMines += self.isMine(j    , i - 1)
					self.grid[i][j].numMines += self.isMine(j + 1, i - 1)

					self.grid[i][j].numMines += self.isMine(j - 1,     i)
					self.grid[i][j].numMines += self.isMine(j + 1,     i)

					self.grid[i][j].numMines += self.isMine(j - 1, i + 1)
					self.grid[i][j].numMines += self.isMine(j    , i + 1)
					self.grid[i][j].numMines += self.isMine(j + 1, i + 1)

		# Reset number of cells left to win the game

		self.cellsLeft = self.size[0] * self.size[1] - self.minesCount
		self.state = 0
		self.minesLeft = self.minesCount

	# Function to check if a cell is valid

	def cellValid(self, x, y):
		if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return False
		return True

	# Function to check if a cell is open or not

	def isOpen(self, x, y):
		if not self.cellValid(x, y): return False
		return self.grid[y][x].open

	# Function to check if a cell is a mine cell

	def isMine(self, x, y):
		if not self.cellValid(x, y): return 0
		if self.grid[y][x].isMine == True: return 1
		return 0

	# Function to check if a cell is flagged

	def isFlagged(self, x, y):
		if not self.cellValid(x, y): return 0
		if self.grid[y][x].flagged == True: return 1
		return 0

	# Function to check if a cell is satisfied

	def isSatisfied(self, x, y):
		if not self.cellValid(x, y): return False

		countFlags  = self.isFlagged(x - 1, y - 1)
		countFlags += self.isFlagged(x    , y - 1)
		countFlags += self.isFlagged(x + 1, y - 1)

		countFlags += self.isFlagged(x - 1, y)
		countFlags += self.isFlagged(x    , y)
		countFlags += self.isFlagged(x + 1, y)

		countFlags += self.isFlagged(x - 1, y + 1)
		countFlags += self.isFlagged(x    , y + 1)
		countFlags += self.isFlagged(x + 1, y + 1)

		if countFlags == self.grid[y][x].numMines:
			return True

		return False

	# Function to open cell

	def openCell(self, x, y, click = False, chord = False):
		if self.created == False:
			self.fillMines((x, y))
			self.created = True
			self.time = 0
			self.timeTimer = pygame.time.get_ticks() + 1000

		if self.state != 0: return # Not playing
		if not self.cellValid(x, y): return
		if self.isFlagged(x, y) == 1: return

		if self.isOpen(x, y) == True:
			if click == True: # Chording cells
				if self.isSatisfied(x, y):
					self.openCell(x - 1, y - 1, chord = True)
					self.openCell(x    , y - 1, chord = True)
					self.openCell(x + 1, y - 1, chord = True)
					self.openCell(x - 1, y    , chord = True)
					self.openCell(x + 1, y    , chord = True)
					self.openCell(x - 1, y + 1, chord = True)
					self.openCell(x    , y + 1, chord = True)
					self.openCell(x + 1, y + 1, chord = True)

			return

		if self.isMine(x, y) == 1:
			if click == True or chord == True: # If the player clicks on a mine cell
				# Open all the cells

				for i in range(self.size[1]):
					for j in range(self.size[0]):
						self.grid[i][j].open = True

			self.state = 2 # Game lost

			print('You lose!')

			return

		self.grid[y][x].open = True
		self.cellsLeft -= 1

		if self.cellsLeft <= 0:
			print('You win!')
			self.state = 1

		if self.grid[y][x].numMines > 0:
			return

		self.openCell(x - 1, y - 1, click = False)
		self.openCell(x    , y - 1, click = False)
		self.openCell(x + 1, y - 1, click = False)
		self.openCell(x - 1, y    , click = False)
		self.openCell(x + 1, y    , click = False)
		self.openCell(x - 1, y + 1, click = False)
		self.openCell(x    , y + 1, click = False)
		self.openCell(x + 1, y + 1, click = False)

	# Function to flag a cell

	def flagCell(self, x, y):
		if self.state != 0: return # Not playing
		if not self.cellValid(x, y): return
		if self.isOpen(x, y): return

		if self.grid[y][x].flagged == False:
			self.grid[y][x].flagged = True
			self.minesLeft -= 1
		else:
			self.grid[y][x].flagged = False
			self.minesLeft += 1

# Function to resize window

def resizeWindow(size):
	window = pygame.display.set_mode(size)
	windowSurface = pygame.display.get_surface()

	return window, windowSurface

# Mine number colors

numColor = (
		(  0,   0, 255), # 1
		(  0, 128,   0), # 2
		(255,   0,   0), # 3
		(  0,   0, 128), # 4
		(128,   0,   0), # 5
		(  0, 128, 128), # 6
		(  0,   0,   0), # 7
		(128, 128, 128)  # 8
	)

# Initialize pygame

pygame.init()

# Main grid

grid = Grid(9, 9) # Start from beginner difficulty
grid.setMinesCount(10)

# Create the game window

print('Initializing window...')

cellSize = 32 # Width and height of a single cell
screenSize = (cellSize * grid.size[0], cellSize * (grid.size[1] + 1))
window, windowSurface = resizeWindow(screenSize)

pygame.display.set_caption('Simple Minesweeper')

# Font for rendering text

fontSize = 24
smallFontSize = 18

font = pygame.font.SysFont(None, fontSize)
smallFont = pygame.font.SysFont(None, smallFontSize)

# Game loop

gameDifficulty = 0 # Start with beginner difficulty
gameRunning = True

print('Entering game loop...')
while gameRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameRunning = False

		if event.type == pygame.MOUSEBUTTONDOWN: # Opening a cell
			cellX = event.pos[0] // cellSize
			cellY = event.pos[1] // cellSize

			if event.button == pygame.BUTTON_LEFT:
				grid.openCell(cellX, cellY, click = True)

			if event.button == pygame.BUTTON_RIGHT:
				grid.flagCell(cellX, cellY)

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: # Resetting th egrid
				grid.reset()

			if event.key == pygame.K_ESCAPE: # Exitting the game
				gameRunning = False

			if event.key == pygame.K_1: # Set difficulty to beginner
				if gameDifficulty != 0:
					grid = Grid(9, 9)
					grid.setMinesCount(10)

					screenSize = (cellSize * grid.size[0], cellSize * (grid.size[1] + 1))
					window, windowSurface = resizeWindow(screenSize)

					gameDifficulty = 0

			if event.key == pygame.K_2: # Set difficulty to intermediate
				if gameDifficulty != 1:
					grid = Grid(16, 16)
					grid.setMinesCount(40)

					screenSize = (cellSize * grid.size[0], cellSize * (grid.size[1] + 1))
					window, windowSurface = resizeWindow(screenSize)

					gameDifficulty = 1

			if event.key == pygame.K_3: # Set difficulty to expert
				if gameDifficulty != 2:
					grid = Grid(30, 16)
					grid.setMinesCount(99)

					screenSize = (cellSize * grid.size[0], cellSize * (grid.size[1] + 1))
					window, windowSurface = resizeWindow(screenSize)

					gameDifficulty = 2

	# Draw the grid

	window.fill((0, 0, 0)) # Clear screen with black

	for i in range(grid.size[1]):
		for j in range(grid.size[0]):
			cell = grid.grid[i][j]
			cellX = j * cellSize
			cellY = i * cellSize
			cellRect = pygame.Rect(cellX + 1, cellY + 1, cellSize - 2, cellSize - 2)

			if cell.open == False:
				cellColor = (192, 192, 192)
			else:
				cellColor = (96, 96, 96)

			pygame.draw.rect(windowSurface, cellColor, cellRect)

			if cell.open == True:
				if cell.isMine == False:
					if cell.numMines > 0:
						textSize = font.size(str(cell.numMines))

						numSurf = font.render(str(cell.numMines), True, numColor[cell.numMines - 1])
						numRect = numSurf.get_rect()
						numRect.x = cellX + (cellSize // 2) - textSize[0] // 2
						numRect.y = cellY + (cellSize // 2) - textSize[1] // 2

						window.blit(numSurf, numRect)
				else:
					mineRect = pygame.Rect(cellX + 4, cellY + 4, cellSize - 8, cellSize - 8)
					pygame.draw.rect(windowSurface, (0, 0, 0), mineRect)
			else:
				if cell.flagged == True:
					mineRect = pygame.Rect(cellX + 4, cellY + 4, cellSize - 8, cellSize - 8)
					pygame.draw.rect(windowSurface, (255, 128, 0), mineRect)

	# Show timer

	if grid.state == 0:
		timerColor = (255, 255, 255)
	elif grid.state == 1:
		timerColor = (0, 255, 0)
	else:
		timerColor = (255, 0, 0)

	timerSurface = smallFont.render('Time: ' + str(grid.time), True, timerColor)
	timerRect = timerSurface.get_rect()
	timerRect.y = grid.size[1] * cellSize

	window.blit(timerSurface, timerRect)

	# Show number of mines left unflagged

	textSurface = smallFont.render('Mines left: ' + str(grid.minesLeft), True, (255, 255, 255))
	textRect = textSurface.get_rect()
	textRect.y = grid.size[1] * cellSize + smallFontSize

	window.blit(textSurface, textRect)

	# Show controls

	textSurface = smallFont.render('Space - Reset', True, (255, 255, 255))
	textRect = textSurface.get_rect()
	textRect.x = 80
	textRect.y = grid.size[1] * cellSize

	window.blit(textSurface, textRect)

	textSurface = smallFont.render('1 - Beginner', True, (255, 255, 255))
	textRect = textSurface.get_rect()
	textRect.x = 80
	textRect.y = grid.size[1] * cellSize + smallFontSize

	window.blit(textSurface, textRect)

	textSurface = smallFont.render('2 - Intermediate', True, (255, 255, 255))
	textRect = textSurface.get_rect()
	textRect.x = 180
	textRect.y = grid.size[1] * cellSize

	window.blit(textSurface, textRect)

	textSurface = smallFont.render('3 - Expert', True, (255, 255, 255))
	textRect = textSurface.get_rect()
	textRect.x = 180
	textRect.y = grid.size[1] * cellSize + smallFontSize

	window.blit(textSurface, textRect)

	# Update timer

	if grid.created == True and grid.state == 0:
		if grid.timeTimer < pygame.time.get_ticks():
			grid.timeTimer = pygame.time.get_ticks() + 1000
			grid.time += 1

	pygame.display.flip()
	pygame.time.delay(16)

# Clean things up

print('Quitting...')
pygame.quit()
sys.exit()
