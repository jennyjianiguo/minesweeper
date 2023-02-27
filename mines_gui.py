from tkinter import *
import random, time

root = Tk()
root.title("Minesweeper")
root.geometry("500x500")

# Minesweeper Dimensions
width = 9
height = 9
bomb_number = 10

solution_grid = []
user_grid = []
names = []
times = []

class minesGUI:
    def __init__(self):
        self.myFrame = Frame(root)
        self.myFrame.grid()

        self.startGame()

    def startGame(self):
        # Reset lists
        solution_grid.clear()
        user_grid.clear()

        # Enter name & Start
        self.label0 = Label(self.myFrame, text="MINESWEEPER", fg="#7393EA", font=("Beirut", 20))
        self.label0.grid(row=1, column=1)
        self.askName = Label(self.myFrame, text="Enter your name: ", fg="#7393EA", font=("Beirut", 20))
        self.askName.grid(row=2, column=1)
        self.userName = Entry(self.myFrame)
        self.userName.grid(row=3, column=1)
        self.startButton = Button(self.myFrame, text="Start Game", fg="#7393EA", command=self.startButtonClicked)
        self.startButton.grid(row=4, column=1)

        # Instruction button
        self.line = Label(self.myFrame, text="")
        self.line.grid(row=5, column=1)
        self.infoButton = Button(self.myFrame, text="Instructions", fg="#7393EA", command=self.instructionPage)
        self.infoButton.grid(row=6, column=1)

        # Center widgets
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def instructionPage(self):
        # Clear page
        self.label0.destroy()
        self.askName.destroy()
        self.userName.destroy()
        self.startButton.destroy()
        self.line.destroy()
        self.infoButton.destroy()

        # Instructions
        self.emptyLine = Label(self.myFrame, text=" ")
        self.emptyLine.grid(row=1, column=1)
        self.instruct = Label(self.myFrame, text="Instructions", fg="#7393EA", font=("Beirut", 15))
        self.instruct.grid(row=2, column=1)
        instructionsText = "1. left click to reveal cells\n2. right click to flag cells\n3. avoid the bombs!"
        self.instructions = Label(self.myFrame, text=instructionsText, fg="#7393EA", font=(12))
        self.instructions.grid(row=3, column=1)

        # Back button
        self.emptyLine2 = Label(self.myFrame, text="")
        self.emptyLine2.grid(row=4, column=1)
        self.back = Button(self.myFrame, text="Back", fg="#7393EA", command=self.startGame1)
        self.back.grid(row=5, column=1)

    def startGame1(self):
        # Clear page
        self.emptyLine.destroy()
        self.instruct.destroy()
        self.instructions.destroy()
        self.emptyLine2.destroy()
        self.back.destroy()
        self.startGame()

    # Start time
    # Code adapted from Delft Stack
    # https://www.delftstack.com/howto/python-tkinter/how-to-use-a-timer-in-tkinter/
    def timeStart(self):
        self.clock.configure(text=self.now)
        self.now -= 1
        self.clock.after(1000, self.timeStart)
        # If time runs out
        if self.now == 0:
            self.endGame()
            # Print time labels
            self.revealBomb = Label(self.myFrame, text="You have run out of time!", fg="#7393EA")
            self.revealBomb.grid(row=12, column=0, columnspan=9)
            # Pring time's up labels
            self.gameOver = Label(self.myFrame, text="TIME IS UP", font=("Beirut", 20), fg="#7393EA")
            self.gameOver.grid(row=0, column=0, columnspan=9)
            # Store user time
            times.append("NULL")
            return


    def startButtonClicked(self):
        # Store user name
        # Code adapted from Tutorials Point
        # https://www.tutorialspoint.com/how-to-get-the-value-of-an-entry-widget-in-tkinter
        entry = self.userName.get()
        if entry.strip() != "":
            names.append(entry)
        else:
            names.append("anonymous")

        # Button click count
        self.count = 0

        # Clear screen
        self.label0.destroy()
        self.askName.destroy()
        self.userName.destroy()
        self.startButton.destroy()
        self.line.destroy()
        self.infoButton.destroy()

        # Create time, mines, flags, and tryAgain labels
        self.clock = Label(self.myFrame, text="00:00", fg="#7393EA")
        self.clock.grid(row=0, column=0, columnspan=9)
        self.mines = Label(self.myFrame, text="Mines: 0", fg="#7393EA")
        self.mines.grid(row=12, column=0, columnspan=4)
        self.flags = Label(self.myFrame, text="Flags: 0", fg="#7393EA")
        self.flags.grid(row=12, column=5, columnspan=4)
        self.tryAgain = Label(self.myFrame, text="", fg="#7393EA")
        self.tryAgain.grid(row=15, column=0, columnspan=9)

        # Timer starts
        self.now = 60
        self.timeStart()

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

    # Place bomb and fill grid
    def placeBomb(self, x, y):
        for bomb in range(bomb_number):
            bomb_x = random.randint(1, width)
            bomb_y = random.randint(1, height)
            # No repeat bombs & bombs do not start the game
            if (solution_grid[bomb_y][bomb_x] != '*') and ((bomb_x != y) or (bomb_y != x)):
                solution_grid[bomb_y][bomb_x] = '*'
                self.fillGrid(bomb_x, bomb_y)

    def fillGrid(self, bomb_x, bomb_y):
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
            self.placeBomb(y, x)

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
            # Store time
            times.append("NULL")

    # Reveal surrounding zeros
    def openZero(self, x, y):
        # Open grid if closed
        if user_grid[x-1][y-1]["text"] == "?":
            user_grid[x-1][y-1]["text"] = solution_grid[y][x]
            user_grid[x-1][y-1]["width"] = 2
            user_grid[x-1][y-1]["fg"] = "black"
        # Check surrounding zeros
        if user_grid[x-1][y-1]["text"] == 0:
            if x != 1 and y != 1:
                if user_grid[x-2][y-2]["text"] == "?":
                    self.openZero(x-1, y-1)  # Not top left
            if x != 1 and y != height:
                if user_grid[x-2][y]["text"] == "?":
                    self.openZero(x-1, y+1) # Not bottom left
            if x != width and y != 1:
                if user_grid[x][y-2]["text"] == "?":
                    self.openZero(x+1, y-1) # Not top right
            if x != width and y != height:
                if user_grid[x][y]["text"] == "?":
                    self.openZero(x+1, y+1) # Not bottom right
            if x != 1:
                if user_grid[x-2][y-1]["text"] == "?":
                    self.openZero(x-1, y) # Not left side
            if x != width:
                if user_grid[x][y-1]["text"] == "?":
                    self.openZero(x+1, y) # Not right side
            if y != 1:
                if user_grid[x-1][y-2]["text"] == "?":
                    self.openZero(x, y-1) # Not top row
            if y != width:
                if user_grid[x-1][y]["text"] == "?":
                    self.openZero(x, y+1) # Not bottom row
        # Stop recursion if value is not 0
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
            # Store time
            times.append(str(60-self.now) + " secs")

    # End game screen
    def endGame(self):
        self.clock.destroy()
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
        self.lbTitle.grid(row=0, column=0, columnspan=2)

        # Create name and time labels
        # Format names to print
        joinedNames = '\n'.join(names)
        joinedTimes = '\n'.join(times)

        self.printNames = Label(self.myFrame, text=joinedNames)
        self.printNames.grid(row=1, column=0)
        self.printTimes = Label(self.myFrame, text=joinedTimes)
        self.printTimes.grid(row=1, column=1)

        # Create restart button
        self.empty = Label(self.myFrame, text="")
        self.empty.grid(row=10, column=0, columnspan=2)
        self.restart = Button(self.myFrame, text="Restart Game", fg="#7393EA", command=self.restartGame)
        self.restart.grid(row=11, column=0, columnspan=2)

    def restartGame(self):
        self.lbTitle.destroy()
        self.printNames.destroy()
        self.printTimes.destroy()
        self.empty.destroy()
        self.restart.destroy()
        self.startGame()


def start():
    ms = minesGUI()
    ms.myFrame.mainloop()

start()