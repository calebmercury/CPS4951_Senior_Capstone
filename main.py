import pygame
from game import Game
from board import Board, load_piece_images


def draw_menu(screen, windowSize):
    screen.fill((30, 30, 30))
    font = pygame.font.SysFont("Arial", 60, bold=True)

    title_text = font.render("CHESS PY", True, (255, 255, 255))
    screen.blit(title_text, (windowSize//2 - title_text.get_width()//2, 200))

    button_rect = pygame.Rect(windowSize//2 - 100, 400, 200, 60)

    mouse_pos = pygame.mouse.get_pos()
    color = (100, 100, 100) if button_rect.collidepoint(mouse_pos) else (60, 60, 60)

    pygame.draw.rect(screen, color, button_rect, border_radius=10)

    btn_font = pygame.font.SysFont("Arial", 30)
    btn_text = btn_font.render("START GAME", True, (255, 255, 255))
    screen.blit(btn_text, (button_rect.centerx - btn_text.get_width()//2, button_rect.centery - btn_text.get_height()//2))

    return button_rect

def draw_menu2(screen, windowSize):
    screen.fill((30, 30, 30))
    font = pygame.font.SysFont("Arial", 60, bold=True)

    title_text = font.render("CHESS PY", True, (255, 255, 255))
    screen.blit(title_text, (windowSize//2 - title_text.get_width()//2, 200))

    button_rect = pygame.Rect(windowSize//2 - 100, 400, 200, 60)

    mouse_pos = pygame.mouse.get_pos()
    color = (100, 100, 100) if button_rect.collidepoint(mouse_pos) else (60, 60, 60)

    pygame.draw.rect(screen, color, button_rect, border_radius=10)

    btn_font = pygame.font.SysFont("Arial", 30)
    btn_text = btn_font.render("EASY", True, (255, 255, 255))
    screen.blit(btn_text, (button_rect.centerx - btn_text.get_width()//2, button_rect.centery - btn_text.get_height()//2))

    btn2_font = pygame.font.SysFont("Arial", 30)
    btn2_text = btn2_font.render("MEDIUM", True, (255, 255, 255))
    screen.blit(btn2_text, (button_rect.centerx - btn2_text.get_width()//2, button_rect.centery - btn2_text.get_height()//2))

    btn3_font = pygame.font.SysFont("Arial", 30)
    btn3_text = btn_font.render("LARGE", True, (255, 255, 255))
    screen.blit(btn3_text, (button_rect.centerx - btn3_text.get_width()//2, button_rect.centery - btn3_text.get_height()//2))

    return button_rect2


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

    in_menu = True
    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if in_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        in_menu = False
            else:
                game.handleEvent(event)

        if in_menu:
            button_rect = draw_menu(screen, windowSize)
            button_rect = draw_menu2(screen= windowSize)
        else:
            game.update(dt)
            game.draw(screen)
        pygame.display.flip()

    pygame.quit()
#test
if __name__ == "__main__":
    main()