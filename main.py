import pygame
import sys

pygame.init()

screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size + 150))
pygame.display.set_caption('Sudoku Solver')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)

board = [[0 for _ in range(9)] for _ in range(9)]

selected = None

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

def draw_solve_button():
    solve_button = pygame.Rect((screen_size / 2 - 50, screen_size + 20, 100, 50))
    pygame.draw.rect(screen, LIGHT_GRAY, solve_button)
    text = font.render('Solve', True, BLACK)
    screen.blit(text, (solve_button.x + (solve_button.width - text.get_width()) / 2,
                       solve_button.y + (solve_button.height - text.get_height()) / 2))
    return solve_button


def draw_selection():
    if selected:
        if 0 <= selected[0] < 9 and 0 <= selected[1] < 9:
            pygame.draw.rect(screen, BLUE, (
                selected[1] * screen_size / 9, selected[0] * screen_size / 9, screen_size / 9, screen_size / 9), 3)

def draw_numbers():
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num_text = font.render(str(board[i][j]), True, BLACK)
                num_text_rect = num_text.get_rect(
                    center=(j * screen_size / 9 + screen_size / 18, i * screen_size / 9 + screen_size / 18))
                screen.blit(num_text, num_text_rect)

def reset_board(board):
    for i in range(9):
        for j in range(9):
            board[i][j] = 0

def draw_reset_button():
    reset_button = pygame.Rect((screen_size / 2 - 50, screen_size + 90, 100, 50))
    pygame.draw.rect(screen, LIGHT_GRAY, reset_button)
    text = font.render('Reset', True, BLACK)
    screen.blit(text, (reset_button.x + (reset_button.width - text.get_width()) / 2,
                       reset_button.y + (reset_button.height - text.get_height()) / 2))
    return reset_button

def main():
    global selected
    running = True
    solve_button = draw_solve_button()
    reset_button = draw_reset_button()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if solve_button.collidepoint(x, y):
                    solve_sudoku(board)
                elif reset_button.collidepoint(x, y):
                    reset_board(board)
                else:
                    selected = (int(y // (screen_size / 9)), int(x // (screen_size / 9)))
            elif event.type == pygame.KEYDOWN:
                if selected:
                    if event.key == pygame.K_BACKSPACE:
                        board[selected[0]][selected[1]] = 0
                    elif selected and event.unicode.isnumeric():
                        num = int(event.unicode)
                        if is_valid(board, selected[0], selected[1], num):
                            board[selected[0]][selected[1]] = num
                            draw_numbers()
                    elif event.key == pygame.K_UP:
                        if selected[0] > 0:
                            selected = (selected[0] - 1, selected[1])
                    elif event.key == pygame.K_DOWN:
                        if selected[0] < 8:
                            selected = (selected[0] + 1, selected[1])
                    elif event.key == pygame.K_LEFT:
                        if selected[1] > 0:
                            selected = (selected[0], selected[1] - 1)
                    elif event.key == pygame.K_RIGHT:
                        if selected[1] < 8:
                            selected = (selected[0], selected[1] + 1)
        screen.fill(WHITE)
        draw_grid()
        draw_numbers()
        draw_selection()
        draw_solve_button()
        draw_reset_button()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()