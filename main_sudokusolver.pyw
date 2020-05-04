import pygame
import time, random, textwrap, copy
import solver
pygame.font.init()


# Initializing all variables that are not changing in the game, like size, color and caption
WIDTH, HEIGHT = 398, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Colors
WHITE = (255,255,255)
BLUE = (0,0,100)
BLACK = (0,0,0)
GRAY = (200,200,200)
RED = (255,0,0)
GREEN = (0,255,0)

# Fonts
NUMBER_FONT = pygame.font.SysFont("comicsans", 35)



class Sudoku():

    def __init__(self):
        self.x_space = 0
        self.y_space = 50
        self.cube_size = int((WIDTH - 2 * self.x_space) / 9)
        self.board = [[0 for i in range(0,9)] for j in range(0,9)]
        self.cubeboard = []
        self.create_cubes()
        self.draw_board()
        
    def create_cubes(self):
        x = self.x_space
        y = self.y_space
        row = []

        for i in range(0,9):
            for j in range(0,9):
                cube = Cube(0, x, y, self.cube_size)
                row.append(cube)
                x += self.cube_size      
            self.cubeboard.append(row)
            row = []
            x = self.x_space
            y += self.cube_size                
    
    def draw_board(self):
        x = self.x_space
        y = self.y_space

        self.draw_cubes()

        for i in range(0,10):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(WIN, BLACK, (self.x_space, y), ((self.x_space + self.cube_size * 9), y), thick)
            pygame.draw.line(WIN, BLACK, (x, self.y_space), (x, (self.y_space + self.cube_size * 9)), thick)
            x += self.cube_size
            y += self.cube_size


    def draw_cubes(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.cubeboard[i][j].selected == True:
                    self.cubeboard[i][j].draw_selection()
                if not solver.is_valid(self.board, i, j) and self.board[i][j] != 0:
                    self.cubeboard[i][j].draw_invalid()
                    self.cubeboard[i][j].valid = False
                else:
                    self.cubeboard[i][j].valid = True
                self.cubeboard[i][j].draw_number()        

    def update(self, row, col, num):
        for i in range(0,9):
            for j in range(0,9):
                if i == row and j == col:
                    self.cubeboard[i][j].selected = True
                else:
                    self.cubeboard[i][j].selected = False

        if num != None:
            self.cubeboard[row][col].value = num
            self.board[row][col] = num

    def get_boardposition(self, pos):
        col = (pos[0] - self.x_space) // self.cube_size
        row = (pos[1] - self.y_space) // self.cube_size
        return row, col

    def validate(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.cubeboard[i][j].valid == False:
                    return False
        return True

    def solve(self, visualize):
        if self.validate():
            if visualize:
                self.setupboard()
                self.visual_solve(self.board)
            else:    
                solver.solver(self.board)
                for i in range(0,9):
                    for j in range(0,9):
                        self.cubeboard[i][j].value = self.board[i][j]

    def setupboard(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.cubeboard[i][j].value != 0:
                    self.cubeboard[i][j].draw_contour(GREEN)

    def update_visual(self, cube, color):
        cube.draw_cube()
        if color == RED:
            cube.value = 0
        cube.draw_number()
        cube.draw_contour(color)
        pygame.display.update()
        pygame.time.delay(50)

    
    def visual_solve(self, board):
        
        pos = solver.find_empty(board)
        if pos:
            row,col = pos
            for num in range(1,10):       
                board[row][col] = num
                self.cubeboard[row][col].value = num

                if solver.is_valid(board,row,col):
                    self.update_visual(self.cubeboard[row][col], GREEN)
                    board = self.visual_solve(board)
                    if not solver.find_empty(board):
                        break
                    self.update_visual(self.cubeboard[row][col], RED)
                board[row][col] = 0
            return board
            
        else:
            return board


class Cube():

    def __init__(self, value, x, y, size): 
        self.x = x
        self.y = y
        self.size = size
        self.value = value
        self.selected = False
        self.valid = True

    def draw_cube(self):
        pygame.draw.rect(WIN, WHITE, (self.x, self.y, self.size, self.size))
    
    def draw_selection(self):
        s = pygame.Surface((self.size,self.size)) 
        s.set_alpha(70)               
        s.fill((BLACK))          
        WIN.blit(s, (self.x, self.y))

    def draw_number(self):
        if self.value != 0:
            number = NUMBER_FONT.render(str(self.value), 1, BLACK)
            WIN.blit(number, (round(self.x + (self.size - number.get_width()) / 2), round(self.y + (self.size - number.get_height()) / 2 )))

    def draw_invalid(self):
        s = pygame.Surface((self.size,self.size)) 
        s.set_alpha(100)               
        s.fill((RED))          
        WIN.blit(s, (self.x, self.y))

    def draw_contour(self, color):
        pygame.draw.rect(WIN, color, (self.x, self.y, self.size, self.size), 4)



def main():
    WIN.fill((WHITE))
    run = True
    clock = pygame.time.Clock()
    sudoku = Sudoku()
    row = None
    col = None
    num = None

    def redraw_window():
        WIN.fill(WHITE)
        sudoku.draw_board()

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:    # when clicked with mouse
                row,col = sudoku.get_boardposition(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if col > 0:
                        col -= 1
                if event.key == pygame.K_RIGHT:
                    if col < 8:
                        col += 1
                if event.key == pygame.K_UP:
                    if row > 0:
                        row -= 1
                if event.key == pygame.K_DOWN:
                    if row < 8:
                        row += 1
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    num = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    num = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    num = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    num = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    num = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    num = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    num = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    num = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    num = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    num = 0
                if event.key == pygame.K_SPACE:
                    sudoku.solve(False)
                if event.key == pygame.K_a:
                    sudoku.solve(True)

            sudoku.update(row,col,num)
            num = None
                
        redraw_window()
        pygame.display.update()
main()
