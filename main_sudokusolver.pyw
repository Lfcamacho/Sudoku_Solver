import pygame
import time, random, textwrap, copy
#import solver
pygame.font.init()


# Initializing all variables that are not changing in the game, like size, color and caption
WIDTH, HEIGHT = 405, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
WHITE = (255,255,255)
BLUE = (0,0,70)
BLACK = (0,0,0)
GRAY = (220,220,220)
WIN.fill(WHITE)


class Sudoku():

    def __init__(self):

        self.x_space = 0
        self.y_space = 50
        self.cube_size = round((WIDTH - 2 * self.x_space) / 9)
        self.board = []
        self.create_board()
        
    def create_board(self):
        row = []
        x = self.x_space
        y = self.y_space
        color = BLUE

        for i in range(0,9):
            for j in range (0,9):

                cube = Cube(0, x, y, self.cube_size)
                row.append(cube)
                thick = 3

                if j % 3 == 0 and j != 0 and i == 8:
                    pygame.draw.line(WIN, color, (x, self.y_space), (x, (self.y_space + self.cube_size * 9) - 1), thick)
                
                x += self.cube_size

            if i % 3 == 0 and i != 0:
                pygame.draw.line(WIN, color, (self.x_space, y), ((self.x_space + self.cube_size * 9) - 1, y), thick)

            x= self.x_space
            y += self.cube_size
            self.board.append(row)
            row = []

        pygame.draw.rect(WIN, color, (self.x_space, self.y_space, self.cube_size * 9, self.cube_size * 9), thick)





class Cube():

    def __init__(self, x, y, size):
        
        self.x = x
        self.y = y
        self.size = size
        pygame.draw.rect(WIN, GRAY, (self.x, self.y, self.size, self.size), 1)




def main():

    WIN.fill((255,255,255))
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    sudoku = Sudoku()

    while run:
        clock.tick(FPS)
        pygame.display.update()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

main()