from rules import pawn_moves, valid_wall
from search import astar_path

AI_DEPTH = 2
MAX_WALL_CANDIDATES = 24

def evaluate(state):
    if state.positions[1][0] == 8:
        return 10000
    if state.positions[0][0] == 0:
        return -10000

    p0 = astar_path(state,0)
    p1 = astar_path(state,1)

    d0 = 999 if p0 is None else len(p0)-1
    d1 = 999 if p1 is None else len(p1)-1

    return (d0-d1) + 0.1*(state.walls[1]-state.walls[0])

def all_walls(state, player, limit=False):
    if state.walls[player] <= 0:
        return []

    walls=[]
    for r in range(8):
        for c in range(8):
            if valid_wall(state,"H",r,c):
                walls.append(("W","H",r,c))
            if valid_wall(state,"V",r,c):
                walls.append(("W","V",r,c))

    if limit and len(walls) > MAX_WALL_CANDIDATES:
        path = astar_path(state,1-player) or []
        def priority(w):
            _,_,r,c=w
            return min((abs(r-pr)+abs(c-pc) for pr,pc in path), default=99)
        walls.sort(key=priority)
        walls=walls[:MAX_WALL_CANDIDATES]

    return walls

def generate_moves(state, player, limit_walls=False):
    result=[("P",p) for p in pawn_moves(state,player)]
    result += all_walls(state,player,limit_walls)
    return result

def apply(state, player, move):
    s=state.clone()
    if move[0]=="P":
        s.positions[player]=move[1]
    else:
        _,o,r,c=move
        if o=="H":
            s.h_walls.add((r,c))
        else:
            s.v_walls.add((r,c))
        s.walls[player]-=1
    s.turn=1-player
    return s

def minimax(state, depth, alpha, beta, maximizing):
    if depth==0 or state.positions[0][0]==0 or state.positions[1][0]==8:
        return evaluate(state),None

    player=1 if maximizing else 0
    moves=generate_moves(state,player,limit_walls=maximizing)

    if not moves:
        return evaluate(state),None

    best_move=None

    if maximizing:
        best=float("-inf")
        for move in moves:
            score,_=minimax(apply(state,player,move),
                            depth-1,alpha,beta,False)
            if score>best:
                best=score
                best_move=move
            alpha=max(alpha,best)
            if beta<=alpha:
                break
        return best,best_move

    best=float("inf")
    for move in moves:
        score,_=minimax(apply(state,player,move),
                        depth-1,alpha,beta,True)
        if score<best:
            best=score
            best_move=move
        beta=min(beta,best)
        if beta<=alpha:
            break
    return best,best_move

def choose_ai_move(state):
    _,move=minimax(state,AI_DEPTH,float("-inf"),float("inf"),True)
    return move
