import pygame
from board import Board, load_piece_images
from game import Game

DIFFICULTY_LEVELS = {
    "EASY":   1,
    "MEDIUM": 5,
    "HARD":   20,
}

GOLD       = (210, 175, 90)
OFF_WHITE  = (232, 232, 222)
MUTED_GREY = (140, 140, 148)

def _draw_button(screen, rect, label, font, is_selected, is_hovered, accent=GOLD):
    if is_selected:
        pygame.draw.rect(screen, (55, 44, 10), rect, border_radius=7)
        pygame.draw.rect(screen, accent, rect, 2, border_radius=7)
        color = accent
    elif is_hovered:
        pygame.draw.rect(screen, (42, 42, 50), rect, border_radius=7)
        pygame.draw.rect(screen, (90, 90, 100), rect, 1, border_radius=7)
        color = OFF_WHITE
    else:
        pygame.draw.rect(screen, (28, 28, 34), rect, border_radius=7)
        pygame.draw.rect(screen, (55, 55, 65), rect, 1, border_radius=7)
        color = MUTED_GREY
    surf = font.render(label, True, color)
    screen.blit(surf, (rect.centerx - surf.get_width() // 2, rect.centery - surf.get_height() // 2))


def draw_menu(screen, windowSize, selected_difficulty, selected_color, offset_x=0, offset_y=0):
    # Background
    screen.fill((14, 14, 18))

    # Subtle dark checkerboard pattern
    sq = 44
    for r in range(windowSize // sq + 1):
        for c in range(windowSize // sq + 1):
            if (r + c) % 2 == 0:
                pygame.draw.rect(screen, (20, 20, 26), (c * sq, r * sq, sq, sq))

    # Dim overlay so the board pattern stays subtle
    veil = pygame.Surface((windowSize, windowSize), pygame.SRCALPHA)
    veil.fill((14, 14, 18, 185))
    screen.blit(veil, (0, 0))

    raw = pygame.mouse.get_pos()
    mouse_pos = (raw[0] - offset_x, raw[1] - offset_y)

    # ── Title ──────────────────────────────────────────────────────────
    title_font = pygame.font.SysFont("Arial", 78, bold=True)
    title_surf = title_font.render("CHESS", True, GOLD)
    screen.blit(title_surf, (windowSize // 2 - title_surf.get_width() // 2, 90))

    sub_font = pygame.font.SysFont("Arial", 19)
    sub_surf = sub_font.render("Python Chess Engine", True, MUTED_GREY)
    screen.blit(sub_surf, (windowSize // 2 - sub_surf.get_width() // 2, 182))

    # Gold divider
    pygame.draw.line(screen, GOLD,
                     (windowSize // 2 - 130, 216),
                     (windowSize // 2 + 130, 216), 1)

    # ── Difficulty ─────────────────────────────────────────────────────
    sec_font = pygame.font.SysFont("Arial", 15, bold=True)
    btn_font  = pygame.font.SysFont("Arial", 21, bold=True)

    sec_surf = sec_font.render("DIFFICULTY", True, GOLD)
    screen.blit(sec_surf, (windowSize // 2 - sec_surf.get_width() // 2, 234))

    labels   = ["EASY", "MEDIUM", "HARD"]
    btn_w, btn_h = 138, 44
    spacing  = 14
    total_w  = len(labels) * btn_w + (len(labels) - 1) * spacing
    start_x  = windowSize // 2 - total_w // 2

    diff_rects = {}
    for lbl in labels:
        rect = pygame.Rect(start_x, 264, btn_w, btn_h)
        diff_rects[lbl] = rect
        _draw_button(screen, rect, lbl, btn_font,
                     selected_difficulty == lbl,
                     rect.collidepoint(mouse_pos))
        start_x += btn_w + spacing

    # ── Play As ────────────────────────────────────────────────────────
    as_surf = sec_font.render("PLAY AS", True, GOLD)
    screen.blit(as_surf, (windowSize // 2 - as_surf.get_width() // 2, 342))

    color_rects = {}
    white_rect = pygame.Rect(windowSize // 2 - 152, 370, 138, 50)
    black_rect = pygame.Rect(windowSize // 2 +  14, 370, 138, 50)

    for color, rect in (("w", white_rect), ("b", black_rect)):
        color_rects[color] = rect
        is_sel  = selected_color == color
        is_hov  = rect.collidepoint(mouse_pos)

        # Fill
        if is_sel:
            fill = (240, 238, 228) if color == "w" else (24, 24, 30)
            pygame.draw.rect(screen, fill, rect, border_radius=8)
            pygame.draw.rect(screen, GOLD, rect, 2, border_radius=8)
        elif is_hov:
            pygame.draw.rect(screen, (42, 42, 50), rect, border_radius=8)
            pygame.draw.rect(screen, (90, 90, 100), rect, 1, border_radius=8)
        else:
            pygame.draw.rect(screen, (28, 28, 34), rect, border_radius=8)
            pygame.draw.rect(screen, (55, 55, 65), rect, 1, border_radius=8)

        # Piece dot
        dot_col = (230, 228, 218) if color == "w" else (38, 38, 44)
        dot_border = GOLD if is_sel else (80, 80, 92)
        pygame.draw.circle(screen, dot_col, (rect.left + 22, rect.centery), 10)
        pygame.draw.circle(screen, dot_border, (rect.left + 22, rect.centery), 10, 1)

        lbl_text  = "WHITE" if color == "w" else "BLACK"
        lbl_color = (20, 20, 24) if (is_sel and color == "w") else GOLD if is_sel else OFF_WHITE if is_hov else MUTED_GREY
        lbl_surf  = btn_font.render(lbl_text, True, lbl_color)
        screen.blit(lbl_surf, (rect.left + 38, rect.centery - lbl_surf.get_height() // 2))

    # ── Start Button ───────────────────────────────────────────────────
    start_rect = pygame.Rect(windowSize // 2 - 125, 464, 250, 58)
    is_hov = start_rect.collidepoint(mouse_pos)

    if is_hov:
        pygame.draw.rect(screen, GOLD, start_rect, border_radius=10)
        st_color = (14, 14, 18)
    else:
        pygame.draw.rect(screen, (50, 40, 10), start_rect, border_radius=10)
        pygame.draw.rect(screen, GOLD, start_rect, 2, border_radius=10)
        st_color = GOLD

    st_font = pygame.font.SysFont("Arial", 26, bold=True)
    st_surf = st_font.render("START GAME", True, st_color)
    screen.blit(st_surf, (start_rect.centerx - st_surf.get_width() // 2,
                           start_rect.centery - st_surf.get_height() // 2))

    return diff_rects, color_rects, start_rect


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Chess")

    windowSize = 800
    canvas = pygame.Surface((windowSize, windowSize))
    offset_x = (screen.get_width()  - windowSize) // 2
    offset_y = (screen.get_height() - windowSize) // 2

    squareSize = windowSize // 8
    load_piece_images(squareSize)

    clock = pygame.time.Clock()
    in_menu = True
    running = True

    selected_difficulty = "MEDIUM"
    selected_color = "w"

    game = None
    diff_rects = {}
    color_rects = {}
    start_rect = pygame.Rect(0, 0, 0, 0)

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if in_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = (event.pos[0] - offset_x, event.pos[1] - offset_y)
                    for label, rect in diff_rects.items():
                        if rect.collidepoint(pos):
                            selected_difficulty = label

                    for color, rect in color_rects.items():
                        if rect.collidepoint(pos):
                            selected_color = color

                    if start_rect.collidepoint(pos):
                        skill = DIFFICULTY_LEVELS[selected_difficulty]
                        game = Game(
                            windowSize,
                            skill_level=skill,
                            player_color=selected_color
                        )
                        in_menu = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    adjusted = pygame.event.Event(event.type, {
                        **event.__dict__,
                        "pos": (event.pos[0] - offset_x, event.pos[1] - offset_y),
                    })
                    game.handleEvent(adjusted)
                else:
                    game.handleEvent(event)

        screen.fill((10, 10, 14))
        if in_menu:
            diff_rects, color_rects, start_rect = draw_menu(
                canvas,
                windowSize,
                selected_difficulty,
                selected_color,
                offset_x,
                offset_y,
            )
        else:
            game.update(dt)
            game.draw(canvas)

        screen.blit(canvas, (offset_x, offset_y))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()