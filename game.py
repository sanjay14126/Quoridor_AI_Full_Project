from dataclasses import dataclass, field
from search import astar_path
from rules import pawn_moves, valid_wall

@dataclass
class State:
    positions: list = field(default_factory=lambda: [(8,4),(0,4)])
    walls: list = field(default_factory=lambda: [10,10])
    h_walls: set = field(default_factory=set)
    v_walls: set = field(default_factory=set)
    turn: int = 0

    def clone(self):
        return State(
            self.positions.copy(),
            self.walls.copy(),
            self.h_walls.copy(),
            self.v_walls.copy(),
            self.turn
        )

class Game:
    def __init__(self):
        self.state = State()
        self.winner = None
        self.over = False

    def path(self, player):
        return astar_path(self.state, player)

    def distance(self, player):
        path = self.path(player)
        return 999 if path is None else len(path)-1

    def check_winner(self):
        if self.state.positions[0][0] == 0:
            self.winner = 0
            self.over = True
        elif self.state.positions[1][0] == 8:
            self.winner = 1
            self.over = True

    def move_pawn(self, player, target):
        if self.over or self.state.turn != player:
            return False
        if target not in pawn_moves(self.state, player):
            return False

        self.state.positions[player] = target
        self.state.turn = 1-player
        self.check_winner()
        return True

    def place_wall(self, player, orientation, r, c):
        if self.over or self.state.turn != player:
            return False
        if self.state.walls[player] <= 0:
            return False
        if not valid_wall(self.state, orientation, r, c):
            return False

        if orientation == "H":
            self.state.h_walls.add((r,c))
        else:
            self.state.v_walls.add((r,c))

        self.state.walls[player] -= 1
        self.state.turn = 1-player
        return True

    def apply_move(self, player, move):
        if move[0] == "P":
            self.move_pawn(player, move[1])
        else:
            _, orientation, r, c = move
            self.place_wall(player, orientation, r, c)
