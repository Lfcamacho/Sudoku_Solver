import pygame
import queue
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
TITLE_FONT = pygame.font.SysFont("comicsans", 50)
BUTTON_FONT = pygame.font.SysFont("comicsans", 20)



class Sudoku():

    def __init__(self):
        self.x_space = 0
        self.y_space = 60
        self.cube_size = int((WIDTH - 2 * self.x_space) / 9)
        self.board = [[0 for i in range(9)] for j in range(9)]
        self.cubes = []
        self.q = queue.Queue()
        self.create_cubes()

        
    def create_cubes(self):
        x = self.x_space
        y = self.y_space
        row = []

        for i in range(9):
            for j in range(9):
                cube = Cube(0, x, y, self.cube_size)
                row.append(cube)
                x += self.cube_size      
            self.cubes.append(row)
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

        for i in range(9):
            for j in range(9):
                if self.cubes != BLACK: 
                    self.cubes[i][j].draw_contour()      

    def draw_cubes(self):
        
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].draw_cube()
                if self.cubes[i][j].selected:
                    self.cubes[i][j].draw_selection()
                if not self.cubes[i][j].valid:
                    self.cubes[i][j].draw_invalid()
                self.cubes[i][j].draw_number()

    def update_cube(self, row, col, num):
        if num != None:
            self.cubes[row][col].value = num
            self.board[row][col] = num

        for i in range(9):
            for j in range(9):
                if i == row and j == col:
                    self.cubes[i][j].selected = True
                else:
                    self.cubes[i][j].selected = False
                if solver.is_valid(self.board, i, j) or self.board[i][j] == 0:
                    self.cubes[i][j].valid = True
                else:
                    self.cubes[i][j].valid = False
                if self.q.empty():
                    self.cubes[i][j].contour = BLACK
                else:
                    self.cubes[i][j].selected = False

    def valid_position(self, pos):
        if pos[0] > self.x_space and pos[0] < self.x_space + 9 * self.cube_size and pos[1] > self.y_space and pos[1] < self.y_space + 9 * self.cube_size:
            return True
        return False

    def get_boardposition(self, pos):
        col = (pos[0] - self.x_space) // self.cube_size
        row = (pos[1] - self.y_space) // self.cube_size
        return row, col

    def validate(self):
        for i in range(9):
            for j in range(9):
                if self.cubes[i][j].valid == False:
                    return False
        return True

    def solve(self, visualize):
        if self.validate():
            if visualize:
                self.visual_solve(self.board)
            else:    
                solver.solver(self.board)
                for i in range(9):
                    for j in range(9):
                        self.cubes[i][j].value = self.board[i][j]

    def update_visual(self, change):
        cube = change[0]
        cube.contour = change[2]
        cube.draw_cube()
        cube.value = change[1]
        cube.draw_number()
        pygame.display.update()
        pygame.time.delay(50)

    
    def visual_solve(self, board):
        
        pos = solver.find_empty(board)
        if pos:
            row,col = pos
            for num in range(1,10):       
                board[row][col] = num

                if solver.is_valid(board,row,col):
                    self.q.put((self.cubes[row][col], num, GREEN))
                    board = self.visual_solve(board)
                    if not solver.find_empty(board):
                        break
                    self.q.put((self.cubes[row][col], 0, RED))
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
        self.contour = BLACK
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

    def draw_contour(self):
        if self.contour != BLACK:
            pygame.draw.rect(WIN, self.contour, (self.x, self.y, self.size, self.size), 4)


class button():
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.draw_button()

    def draw_button(self):
        pygame.draw.rect(WIN, (0,0,0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.height))
        self.draw_text()
    
    def draw_text(self):
        label = BUTTON_FONT.render(self.text, 1, (0,0,0))
        WIN.blit(label, (round(self.x + (self.width - label.get_width()) / 2), round(self.y + (self.height - label.get_height()) / 2 )))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True



def main():
    run = True
    clock = pygame.time.Clock()
    sudoku = Sudoku()
    row = 4
    col = 4
    num = None

    WIN.fill(WHITE)
    fastsolve = button(0, HEIGHT - 30, WIDTH // 3, 30, WHITE, "Fast solve")
    visualsolve = button(WIDTH // 3, HEIGHT - 30, WIDTH // 3, 30, WHITE, "Visual solve")

    def redraw_window():
        WIN.fill(WHITE)
        title = NUMBER_FONT.render("SUDOKU SOLVER", 1, BLACK)
        WIN.blit(title, ((WIDTH - title.get_width()) / 2,20))
        fastsolve.draw_button()
        visualsolve.draw_button()
        sudoku.draw_board()

    while run:

        redraw_window()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:    # when clicked with mouse
                if sudoku.valid_position(event.pos):
                    row,col = sudoku.get_boardposition(event.pos)
                if fastsolve.isOver(event.pos):
                    sudoku.solve(False)
                if visualsolve.isOver(event.pos):
                    sudoku.solve(True)

            if event.type == pygame.MOUSEMOTION:
                if fastsolve.isOver(event.pos):
                    fastsolve.color = GRAY
                else:
                    fastsolve.color = WHITE
                if visualsolve.isOver(event.pos):
                    visualsolve.color = GRAY
                else:
                    visualsolve.color = WHITE

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
                    sudoku.q.queue.clear()
                if event.key == pygame.K_a:
                    sudoku.solve(True)

            sudoku.update_cube(row,col,num)
            num = None
            
        if not sudoku.q.empty(): 
            sudoku.update_visual(sudoku.q.get())
            


main()
