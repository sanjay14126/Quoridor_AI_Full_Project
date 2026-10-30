import pygame
from game import Game
from ai import choose_ai_move

pygame.init()

CELL = 64
MARGIN = 55
TOP = 105
BOARD = 9 * CELL
WIDTH = BOARD + 2 * MARGIN
HEIGHT = TOP + BOARD + 95

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor AI - A* + Minimax")
clock = pygame.time.Clock()

TITLE = pygame.font.SysFont("Arial", 28, bold=True)
FONT = pygame.font.SysFont("Arial", 19)
SMALL = pygame.font.SysFont("Arial", 15)

def center(r, c):
    return (MARGIN + c*CELL + CELL//2, TOP + r*CELL + CELL//2)

def mouse_cell(pos):
    x, y = pos
    if not (MARGIN <= x < MARGIN+BOARD and TOP <= y < TOP+BOARD):
        return None
    return int((y-TOP)//CELL), int((x-MARGIN)//CELL)

def wall_at_mouse(pos, orientation):
    x, y = pos
    bx, by = x-MARGIN, y-TOP
    if not (0 <= bx < BOARD and 0 <= by < BOARD):
        return None
    c, r = int(bx//CELL), int(by//CELL)
    lx, ly = bx-c*CELL, by-r*CELL
    if orientation == "H":
        wr = r-1 if ly < CELL/2 else r
        wc = c
    else:
        wr = r
        wc = c-1 if lx < CELL/2 else c
    return (wr, wc) if 0 <= wr < 8 and 0 <= wc < 8 else None

def draw(game, message, orientation):
    screen.fill((245,245,245))
    screen.blit(TITLE.render("QUORIDOR AI", True, (25,25,25)), (MARGIN,20))
    screen.blit(FONT.render(
        f"Your walls: {game.state.walls[0]}   AI walls: {game.state.walls[1]}",
        True, (30,30,30)), (315,25))

    # Goal rows
    pygame.draw.rect(screen, (205,230,255), (MARGIN,TOP,BOARD,CELL))
    pygame.draw.rect(screen, (255,225,205), (MARGIN,TOP+8*CELL,BOARD,CELL))

    # Grid
    for r in range(9):
        for c in range(9):
            pygame.draw.rect(
                screen, (185,185,185),
                (MARGIN+c*CELL, TOP+r*CELL, CELL, CELL), 1
            )

    # A* shortest paths
    for player in (0,1):
        path = game.path(player)
        if path:
            for r,c in path[1:-1]:
                pygame.draw.circle(screen, (165,165,165), center(r,c), 4)

    # Walls
    for r,c in game.state.h_walls:
        x, y = MARGIN+c*CELL, TOP+(r+1)*CELL
        pygame.draw.line(screen, (85,45,20),
                         (x+4,y),(x+2*CELL-4,y),9)

    for r,c in game.state.v_walls:
        x, y = MARGIN+(c+1)*CELL, TOP+r*CELL
        pygame.draw.line(screen, (85,45,20),
                         (x,y+4),(x,y+2*CELL-4),9)

    # Pawns
    hx,hy = center(*game.state.positions[0])
    ax,ay = center(*game.state.positions[1])
    pygame.draw.circle(screen, (45,105,220), (hx,hy), 22)
    pygame.draw.circle(screen, (220,70,70), (ax,ay), 22)

    you = SMALL.render("YOU", True, (255,255,255))
    ai = SMALL.render("AI", True, (255,255,255))
    screen.blit(you, you.get_rect(center=(hx,hy)))
    screen.blit(ai, ai.get_rect(center=(ax,ay)))

    screen.blit(SMALL.render(
        f"A* distance: You {game.distance(0)}   AI {game.distance(1)}",
        True, (35,35,35)), (MARGIN, TOP+BOARD+7))

    screen.blit(SMALL.render(
        f"{message} | H=horizontal | V=vertical | Selected={orientation} | R=restart",
        True, (35,35,35)), (MARGIN, TOP+BOARD+30))

def main():
    game = Game()
    orientation = "H"
    message = "Your turn."

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Game()
                    message = "Game restarted. Your turn."
                elif event.key == pygame.K_h:
                    orientation = "H"
                    message = "Horizontal wall selected."
                elif event.key == pygame.K_v:
                    orientation = "V"
                    message = "Vertical wall selected."

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.state.turn == 0:
                    pos = pygame.mouse.get_pos()
                    cell = mouse_cell(pos)

                    if cell is not None and game.move_pawn(0, cell):
                        message = "AI is thinking..."
                    else:
                        wall = wall_at_mouse(pos, orientation)
                        if wall and game.place_wall(0, orientation, *wall):
                            message = "AI is thinking..."
                        else:
                            message = "Invalid move or wall."

        if game.state.turn == 1 and not game.over:
            draw(game, "AI is thinking...", orientation)
            pygame.display.update()

            move = choose_ai_move(game.state)
            if move:
                game.apply_move(1, move)

            message = "Your turn."

        if game.winner == 0:
            message = "YOU WIN! Press R to restart."
        elif game.winner == 1:
            message = "AI WINS! Press R to restart."

        draw(game, message, orientation)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
