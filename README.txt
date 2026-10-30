# Quoridor AI - Full Project

## Requirements
Python 3.10+ recommended.
For Python 3.14 use Pygame Community Edition:

    python -m pip install pygame-ce

## Run
Open this folder in IDLE or VS Code and run:

    main.py

## Controls
- Click a legal square to move your pawn.
- H = select horizontal wall.
- V = select vertical wall.
- After selecting H/V, click near an internal board boundary to place a wall.
- R = restart.

## AI concepts
1. A* Search finds the shortest available path.
2. Manhattan-style heuristic estimates distance to the goal row.
3. Minimax evaluates AI and opponent responses.
4. Alpha-Beta pruning skips branches that cannot affect the decision.
5. Wall validation uses A* to ensure both players retain a route.

## Files
main.py   - graphical interface
game.py   - game state and high-level game operations
rules.py  - movement and wall rules
search.py - A* Search
ai.py     - Minimax and Alpha-Beta
README.txt
