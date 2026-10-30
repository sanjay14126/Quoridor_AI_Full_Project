def inside(r, c):
    return 0 <= r < 9 and 0 <= c < 9

def edge_blocked(state, a, b):
    r1,c1 = a
    r2,c2 = b

    if r2 == r1+1:
        return (r1,c1) in state.h_walls
    if r2 == r1-1:
        return (r2,c1) in state.h_walls
    if c2 == c1+1:
        return (r1,c1) in state.v_walls
    if c2 == c1-1:
        return (r1,c2) in state.v_walls
    return True

def pawn_moves(state, player):
    start = state.positions[player]
    enemy = state.positions[1-player]
    r,c = start
    er,ec = enemy
    result = set()

    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr,nc = r+dr,c+dc
        if not inside(nr,nc):
            continue

        nxt = (nr,nc)
        if edge_blocked(state,start,nxt):
            continue

        if nxt != enemy:
            result.add(nxt)
            continue

        # Jump over opponent
        jr,jc = er+dr,ec+dc
        if inside(jr,jc) and not edge_blocked(state,enemy,(jr,jc)):
            result.add((jr,jc))
        else:
            # Diagonal movement around opponent
            sides = [(0,-1),(0,1)] if dr else [(-1,0),(1,0)]
            for sr,sc in sides:
                x,y = er+sr,ec+sc
                if inside(x,y) and not edge_blocked(state,enemy,(x,y)):
                    result.add((x,y))

    return list(result)

def valid_wall(state, orientation, r, c):
    if not (0 <= r < 8 and 0 <= c < 8):
        return False

    # Basic overlap/crossing protection
    if orientation == "H":
        if (r,c) in state.h_walls or (r,c) in state.v_walls:
            return False
    else:
        if (r,c) in state.v_walls or (r,c) in state.h_walls:
            return False

    test = state.clone()
    if orientation == "H":
        test.h_walls.add((r,c))
    else:
        test.v_walls.add((r,c))

    # A wall cannot eliminate every route for either player.
    from search import astar_path
    return astar_path(test,0) is not None and astar_path(test,1) is not None
