from tkinter import *
import random, time

root = Tk()
root.title("Minesweeper")
root.geometry("500x500")

# Minesweeper Dimensions
width = 9
height = 9
bomb_number = 3

solution_grid = []
user_grid = []

class minesGUI:
    def __init__(self):
        self.myFrame = Frame(root)
        self.myFrame.grid()

        # Enter name & Start
        self.label0 = Label(self.myFrame, text="MINESWEEPER", fg="#7393EA", font=("Beirut", 20))
        self.label0.grid(row=1, column=1)
        self.userName = Label(self.myFrame, text="Enter your name: ", fg="#7393EA", font=("Beirut", 20))
        self.userName.grid(row=2, column=1)
        self.textfield = Entry(self.myFrame)
        self.textfield.grid(row=3, column=1)
        self.startButton = Button(self.myFrame, text="Start Game", fg="#7393EA", command=self.startButtonClicked)
        self.startButton.grid(row=4, column=1)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def startButtonClicked(self):
        # Button click count
        self.count = 0

        # Clear screen
        self.label0.destroy()
        self.userName.destroy()
        self.textfield.destroy()
        self.startButton.destroy()

        # Create time, mines, and flags labels
        self.time = Label(self.myFrame, text="00:00", fg="#7393EA")
        self.time.grid(row=0, column=0, columnspan=9)
        self.mines = Label(self.myFrame, text="Mines: 0", fg="#7393EA")
        self.mines.grid(row=12, column=0, columnspan=4)
        self.flags = Label(self.myFrame, text="Flags: 0", fg="#7393EA")
        self.flags.grid(row=12, column=5, columnspan=4)
        self.tryAgain = Label(self.myFrame, text="", fg="#7393EA")
        self.tryAgain.grid(row=15, column=0, columnspan=9)

        # Create tiles
        for x in range(width):
            user_grid.append([])
            for y in range(height):
                self.gridButton = Button(self.myFrame, text="?", fg="#7393EA", width=2, disabledforeground = "black", command=lambda x=x+1, y=y+1: self.reveal(x, y))
                # <Button-2> is right click -- may not work on all computers
                self.gridButton.bind("<Button-2>", lambda e, x=x+1, y=y+1: self.flag(x, y))
                self.gridButton.grid(row=x+1, column=y)
                user_grid[x].append(self.gridButton)

        # Create solution grid
        for row in range(height + 2):
            solution_grid.append([])
            for col in range(width + 2):
                solution_grid[row].append(0)

        # Create gutters on edges of grid
        for row in range(0, height + 2):
            solution_grid[row][0] = 5
            solution_grid[row][width + 1] = 5
        for column in range(0, width + 2):
            solution_grid[0][column] = 5
            solution_grid[height + 1][column] = 5

    def placeBomb(self, x, y):
        for bomb in range(bomb_number):
            bomb_x = random.randint(1, width)
            bomb_y = random.randint(1, height)
            if (solution_grid[bomb_y][bomb_x] != '*') and ((bomb_x != x) or (bomb_y != y)):
                solution_grid[bomb_y][bomb_x] = '*'
                # Fill grid
                for y in range(bomb_y - 1, bomb_y + 2):
                    for x in range(bomb_x - 1, bomb_x + 2):
                        if solution_grid[y][x] != '*':
                            solution_grid[y][x] += 1

    # Reveal cell
    def reveal(self, x, y): # x, y = grid coordinates
        # Button clicked
        self.count += 1
        if self.count == 1:
            self.placeBomb(x, y)

        # Reveal value of cell
        self.tryAgain["text"] = "                                          "
        if user_grid[x-1][y-1]["text"] != solution_grid[y][x]:
            user_grid[x-1][y-1]["text"] = solution_grid[y][x]
            user_grid[x-1][y-1]["width"] = 2
            user_grid[x-1][y-1]["fg"] = "black"
        else:
            self.tryAgain["text"] = "please choose another cell"
        self.checkWin()

        if user_grid[x-1][y-1]["text"] == 0:
            self.openZero(x, y)

        if user_grid[x-1][y-1]["text"] == "*":
            self.endGame()
            # Print reveal bomb labels
            self.revealBomb = Label(self.myFrame, text="You have revealed a bomb!", fg="#7393EA")
            self.revealBomb.grid(row=12, column=0, columnspan=9)
            # Pring game over labels
            self.gameOver = Label(self.myFrame, text="GAME OVER", font=("Beirut", 20), fg="#7393EA")
            self.gameOver.grid(row=0, column=0, columnspan=9)

    def openZero(self, x, y):
        user_grid[x-1][y-1]["text"] = solution_grid[y][x]
        user_grid[x-1][y-1]["width"] = 2
        user_grid[x-1][y-1]["fg"] = "black"
        if user_grid[x-1][y-1]["text"] == 0:
            if x != 1 and y != 1:
                self.openZero(x-1, y-1)  # Not top left
            if x != 1:
                self.openZero(x-1, y) # Not left side
            if x != 1 and y != height:
                self.openZero(x-1, y+1) # Not bottom left
            if y != 1:
                self.openZero(x, y-1) # Not top row
            if y != width:
                self.openZero(x, y+1) # Not bottom row
            if x != width and y != 1:
                self.openZero(x+1, y-1) # Not top right
            if x != width:
                self.openZero(x+1, y)
            if x != width and y != height:
                self.openZero(x+1, y+1) # Not bottom right
        if user_grid[x-1][y-1]["text"] == solution_grid[y][x]:
            return

    def flag(self, x, y):
        if user_grid[x-1][y-1]["text"] != "⚑":
            user_grid[x-1][y-1]["text"] = "⚑"
            user_grid[x-1][y-1]["width"] = 2
            user_grid[x-1][y-1]["fg"] = "green"
        else:
            user_grid[x-1][y-1]["text"] = "?"
            user_grid[x-1][y-1]["width"] = 2
            user_grid[x-1][y-1]["fg"] = "#7393EA"
        self.checkWin()

    def checkWin(self):
        hidden = 0
        for y in range(1, height+1):
            for x in range(1, width+1):
                if ((user_grid[x-1][y-1]["text"]) == "?") or (user_grid[x-1][y-1]["text"] == "⚑"):
                    hidden += 1
        if (hidden == bomb_number):
            self.endGame()
            # Print win game labels
            self.revealBomb = Label(self.myFrame, text="You have discovered all mines!", fg="#7393EA")
            self.revealBomb.grid(row=12, column=0, columnspan=9)
            # Pring game over labels
            self.gameOver = Label(self.myFrame, text="YOU WIN", font=("Beirut", 20), fg="#7393EA")
            self.gameOver.grid(row=0, column=0, columnspan=9)

    # End game screen
    def endGame(self):
        self.time.destroy()
        self.mines.destroy()
        self.flags.destroy()
        self.tryAgain.destroy()

        # Print Mines
        for y in range(width+1):
            for x in range(height+1):
                user_grid[x-1][y-1]["text"] = solution_grid[y][x]
                user_grid[x-1][y-1]["width"] = 2
                user_grid[x-1][y-1]["state"] = DISABLED

        self.endButton = Button(self.myFrame, text="View Leaderboard", fg="#7393EA", command=self.leaderboard)
        self.endButton.grid(row=13, column=1, columnspan=7)

    # Print leaderboard
    def leaderboard(self):
        # Delete existing labels
        self.endButton.destroy()
        self.revealBomb.destroy()
        self.gameOver.destroy()
        for x in range(width):
            for y in range(height):
                user_grid[x][y].destroy()
        user_grid.clear()

        # Create leaderboard labels
        self.lbTitle = Label(self.myFrame, text="LEADERBOARD", font=("Beirut", 20), fg="#7393EA")
        self.lbTitle.grid(row=0, column=0)

        # Create restart button
        self.restart = Button(self.myFrame, text="Restart Game", fg="#7393EA", command=self.restartGame)
        self.restart.grid(row=1, column=0)

    def restartGame(self):
        self.lbTitle.destroy()
        self.restart.destroy()
        self.startButtonClicked()


def start():
    ms = minesGUI()
    ms.myFrame.mainloop()

start()