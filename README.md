# minesweeper

## Overview
Minesweeper is a single-player video game with the objective of discovering all the mines in a grid field.
In this program, users can utilize numbers on the grid to flag points they believe contain mines. To win, they must mark all the mines within a 60 seconds.

## Program Features
- The user will be prompted to enter their name.
- The user will click “start” on a starting page to begin the game.
- A 60-second timer will count down.
- The user will click on squares to reveal spaces.
- If the square has no bombs next to it (value 0), it will reveal squares next to it until the value is not 0.
- Mines are placed at random.
- The first square the user opens will not be a mine.
- If the space the user opens does not contain a mine, it will show the number of mines around that space.
- If the space the user opens does contain a mine, they lose the game.
- If the user chooses to open an already opened square, they will be prompted to choose another space.
- The user can flag spaces.
- If the user flags all the bombs before 60 seconds, they win.
- If the user does not flag all the bombs before 60 seconds, or opens a bomb space, they lose.
- After the game ends, “You Win!” or “You Lose!” will show up on the screen.
- After the game ends, a leaderboard will display player names and times.
- The program will ask if the user would like to play again.

## Sample Output
