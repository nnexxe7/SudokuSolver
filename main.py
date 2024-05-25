import pygame
import sys

pygame.init()

screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size + 100))
pygame.display.set_caption('Sudoku Solver')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

board = [[0 for _ in range(9)] for _ in range(9)]

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False

    for x in range(9):
        if board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            thickness = 4
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (i * screen_size / 9, 0), (i * screen_size / 9, screen_size), thickness)
        pygame.draw.line(screen, BLACK, (0, i * screen_size / 9), (screen_size, i * screen_size / 9), thickness)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()