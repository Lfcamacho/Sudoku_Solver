
# Function to check if the number is valid according to sudoku rules
def is_valid(board,row,col):

    # Loop that will allow to check if there is a number repeated in row or column
    for num in range(9):

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

def find_empty(board):

    for i,val in enumerate(board):
        for j,value in enumerate(val):
            if value == 0:
                return (i,j)
    return False

# Main function that is called recursively to solve sudoku using backtracking
def solver(board):

    pos = find_empty(board)
    if pos:
        row,col = pos
        for num in range(1,10):        # Loop that chooses which number should it try next
            board[row][col] = num

            if is_valid(board,row,col):
                board = solver(board)
                if not find_empty(board):
                    break

            board[row][col] = 0
        return board
        
    else:
        return board

