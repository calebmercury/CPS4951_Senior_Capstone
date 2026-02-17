import pygame
from game import Game
from board import Board, load_piece_images


def main():
    #tetetete
    pygame.init()
    windowSize = 800
    screen = pygame.display.set_mode((windowSize, windowSize))
    pygame.display.set_caption("Chess")

    squareSize = 80
    load_piece_images(squareSize)

    game = Game(windowSize)
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handleEvent(event)

        game.update(dt)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()