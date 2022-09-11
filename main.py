import pygame
from constants import *
from game import Game

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
icon = pygame.image.load(ICON)
pygame.display.set_icon(icon)

def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return (int(row), int(col))

def main():
    game = Game(win)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game.over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.mouse_pos = get_mouse_pos(pygame.mouse.get_pos())
                    game.clicked()

        pygame.display.flip()

if __name__ == '__main__':
    main()