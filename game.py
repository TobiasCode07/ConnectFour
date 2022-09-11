from constants import *
from circle import Circle
import pygame

class Game:
    def __init__(self, win):
        self.win = win
        self.colors = [RED, YELLOW]
        self.turn = 0
        self.starting_pos = (0, 6)
        self.mouse_pos = None
        self.over = False
        self.tie = False
        self.move_count = 0
        self.create_board()
        self.draw_start_screen()
        self.starting_circle()

    def starting_circle(self):
        circle = Circle(self.win, self.colors[self.turn], self.starting_pos[0], self.starting_pos[1])
        self.board[self.starting_pos[0]][self.starting_pos[1]] = circle
        circle.draw()

    def change_turn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def get_circle(self, row, col):
        return self.board[row][col]

    def clear(self, row, col):
        pygame.draw.circle(self.win, WHITE, (col * SQUARE_SIZE + RADIUS, row * SQUARE_SIZE + RADIUS), RADIUS)

    def move(self, circle, row, col):
        self.clear(circle.row, circle.col)
        self.board[circle.row][circle.col], self.board[row][col] = self.board[row][col], self.board[circle.row][
            circle.col]
        circle.move(row, col)

    def get_valid_row(self, col):
        for row in range(ROWS):
            circle = self.get_circle(ROWS - row, col)
            if not circle:
                return ROWS - row

    def check_if_won(self):
        # Check vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if self.board[r + 1][c] and self.board[r + 2][c] and self.board[r + 3][c] and self.board[r + 4][c]:
                    if self.board[r + 1][c].color == self.board[r + 2][c].color == self.board[r + 3][c].color == \
                            self.board[r + 4][c].color:
                        return True

        # Check horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if self.board[r + 1][c] and self.board[r + 1][c + 1] and self.board[r + 1][c + 2] and self.board[r + 1][
                    c + 3]:
                    if self.board[r + 1][c].color == self.board[r + 1][c + 1].color == self.board[r + 1][c + 2].color == \
                            self.board[r + 1][c + 3].color:
                        return True

        # Check positively sloped diagonales
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if self.board[r + 1][c] and self.board[r + 2][c + 1] and self.board[r + 3][c + 2] and self.board[r + 4][
                    c + 3]:
                    if self.board[r + 1][c].color == self.board[r + 2][c + 1].color == self.board[r + 3][c + 2].color == \
                            self.board[r + 4][c + 3].color:
                        return True

        # Check negatively sloped diagonales
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if self.board[r + 1][c] and self.board[r][c + 1] and self.board[r - 1][c + 2] and self.board[r - 2][
                    c + 3]:
                    if self.board[r + 1][c].color == self.board[r][c + 1].color == self.board[r - 1][c + 2].color == \
                            self.board[r - 2][c + 3].color:
                        return True

    def game_over(self):
        font = pygame.font.SysFont("Arial", 40)
        if self.tie:
            text = font.render(f"It's a tie!!!", True, BLACK)
        else:
            text = font.render(f"{'RED' if self.colors[self.turn] == (255, 0, 0) else 'YELLOW'} won!!!", True, BLACK)
        self.win.blit(text, (WIDTH / 2 - (text.get_width() / 2), PADDING / 2 - (text.get_height() / 2)))

    def draw_frame(self, circle):
        pygame.draw.circle(self.win, BLACK, (circle.col * SQUARE_SIZE + RADIUS, circle.row * SQUARE_SIZE + RADIUS),
                           RADIUS, 2)

    def remove_frame(self, circle):
        self.clear(circle.row, circle.col)
        circle.draw()

    def clicked(self):
        for col in range(COLS):
            if self.get_circle(self.starting_pos[0], col):
                circle = self.get_circle(self.starting_pos[0], col)

        if self.mouse_pos[0] == 0:
            if self.mouse_pos == circle.pos and not circle.selected:
                circle.selected = True
                self.draw_frame(circle)
            elif self.mouse_pos == circle.pos and circle.selected:
                row = self.get_valid_row(circle.col)
                if row:
                    self.move(circle, row, circle.col)
                    if self.check_if_won():
                        self.over = True
                        self.game_over()
                    else:
                        self.move_count += 1
                        if self.move_count == ROWS * COLS:
                            self.tie = True
                            self.over = True
                            self.game_over()
                        else:
                            self.change_turn()
                            self.starting_circle()
            elif self.mouse_pos != circle.pos and circle.selected:
                self.move(circle, self.mouse_pos[0], self.mouse_pos[1])
                self.draw_frame(circle)
            else:
                circle.selected = False
                self.remove_frame(circle)
        else:
            circle.selected = False
            self.remove_frame(circle)

    def create_board(self):
        self.board = []
        for row in range(ROWS + 1):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)

    def draw_start_screen(self):
        self.win.fill(WHITE)

        pygame.draw.rect(self.win, BLUE, pygame.Rect(0, PADDING, WIDTH, HEIGHT - PADDING))

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.circle(self.win, WHITE, (col * SQUARE_SIZE + RADIUS, row * SQUARE_SIZE + RADIUS + PADDING),
                                   RADIUS)