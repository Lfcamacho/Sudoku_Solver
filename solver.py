# Function to see if cell is free
def free(board,row,col):

    return True if board[row][col] == 0 else False

# Function to check if the number is valid according to sudoku rules
def verify(board,row,col):

    # Loop that will allow to check if there is a number repeated in row or column
    for num in range(0,9):

        if board[row][num] == board[row][col] and num != col:
            return False
        if board[num][col] == board[row][col] and num != row:
            return False

    # Check if the number is valid in each of the 9 subgrids, by defining the limits of its subgrid and asking if there is any repeated numbers in it
    startrow = row//3*3
    startcol = col//3*3

    for i in range (0,3):
        for j in range (0,3):
            if board[row][col] == board[startrow+i][startcol+j] and row != startrow+i and col != startcol+j:
                return False
    return True

# Function to print the sudoku board
def printboard(board):

    for x in board:
        print(x)
    print('\n')

# Main function that is called himself to solve sudoku recursively using backtracking
def solver(board,row,col):

    global finish # used to finish the program once it finds a solution
    finish = False

    if free(board,row,col):

        # Loop that chooses which number should it try next
        for num in range(1,10):

            board[row][col] = num

            if verify(board,row,col):

                # This if's wil tell which is the next cell in the process
                if col == 8 and row < 8:
                    solver(board,row+1,0)

                if col < 8:
                    solver(board,row,col+1)

                if row == 8 and col == 8:
                    finish = True
                    printboard(board)

            if finish: break

            board[row][col] = 0

    else:

        if col == 8 and row < 8:
            solver(board, row + 1, 0)

        if col < 8:
            solver(board, row, col + 1)

        if row == 8 and col == 8:
            finish = True
            printboard(board)

"""
board = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]
"""

board = [
    [0,3,0,0,0,0,0,0,0],
    [6,0,0,1,0,5,0,0,0],
    [0,0,0,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,0,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,0,0,0,0,5],
    [0,0,0,0,8,0,0,7,0]
]
"""
row = 0
col = 0

printboard(board)
solver(board,row,col)