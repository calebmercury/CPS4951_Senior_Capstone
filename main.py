import pygame
from game import Game
from board import Board, load_piece_images

DIFFICULTY_LEVELS = {
    "EASY":   1,
    "MEDIUM": 5,
    "HARD":   20,
}

def draw_menu(screen, windowSize, selected_difficulty):
    screen.fill((30, 30, 30))

    title_font = pygame.font.SysFont("Arial", 60, bold=True)
    title_text = title_font.render("CHESS PY", True, (255, 255, 255))
    screen.blit(title_text, (windowSize // 2 - title_text.get_width() // 2, 150))

    label_font = pygame.font.SysFont("Arial", 26)
    label = label_font.render("Select Difficulty:", True, (180, 180, 180))
    screen.blit(label, (windowSize // 2 - label.get_width() // 2, 290))

    btn_font = pygame.font.SysFont("Arial", 28, bold=True)
    mouse_pos = pygame.mouse.get_pos()

    labels = ["EASY", "MEDIUM", "HARD"]
    btn_w, btn_h = 160, 50
    spacing = 20
    total_w = len(labels) * btn_w + (len(labels) - 1) * spacing
    start_x = windowSize // 2 - total_w // 2
    y = 340

    diff_rects = {}
    for label in labels:
        rect = pygame.Rect(start_x, y, btn_w, btn_h)
        diff_rects[label] = rect

        is_selected = selected_difficulty == label
        is_hovered = rect.collidepoint(mouse_pos)

        if is_selected:
            fill = (0, 180, 60)
        elif is_hovered:
            fill = (70, 70, 70)
        else:
            fill = (50, 50, 50)

        pygame.draw.rect(screen, fill, rect, border_radius=8)

        text_color = (255, 255, 255)
        text_surf = btn_font.render(label, True, text_color)
        screen.blit(text_surf, (rect.centerx - text_surf.get_width() // 2,
                                rect.centery - text_surf.get_height() // 2))

        start_x += btn_w + spacing

    start_rect = pygame.Rect(windowSize // 2 - 110, 440, 220, 60)
    if start_rect.collidepoint(mouse_pos):
        btn_color = (80, 130, 80)
    else:
        btn_color = (50, 90, 50)
    pygame.draw.rect(screen, btn_color, start_rect, border_radius=10)
    start_font = pygame.font.SysFont("Arial", 30, bold=True)
    start_text = start_font.render("START GAME", True, (255, 255, 255))
    screen.blit(start_text, (start_rect.centerx - start_text.get_width() // 2,
                             start_rect.centery - start_text.get_height() // 2))

    return diff_rects, start_rect


def main():
    pygame.init()
    windowSize = 800
    screen = pygame.display.set_mode((windowSize, windowSize))
    pygame.display.set_caption("Chess")

    squareSize = 80
    load_piece_images(squareSize)

    clock = pygame.time.Clock()
    in_menu = True
    running = True
    selected_difficulty = "MEDIUM"
    game = None
    diff_rects = {}
    start_rect = pygame.Rect(0, 0, 0, 0)

    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if in_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for label, rect in diff_rects.items():
                        if rect.collidepoint(event.pos):
                            selected_difficulty = label
                    if start_rect.collidepoint(event.pos):
                        skill = DIFFICULTY_LEVELS[selected_difficulty]
                        game = Game(windowSize, skill_level=skill)
                        in_menu = False
            else:
                game.handleEvent(event)

        if in_menu:
            diff_rects, start_rect = draw_menu(screen, windowSize, selected_difficulty)
        else:
            game.update(dt)
            game.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
