import heapq
from rules import inside, edge_blocked

def heuristic(cell, player):
    goal_row = 0 if player == 0 else 8
    return abs(cell[0]-goal_row)

def astar_path(state, player):
    start = state.positions[player]
    heap = [(heuristic(start,player),0,start)]
    cost = {start:0}
    parent = {start:None}
    seen = set()

    while heap:
        _,g,current = heapq.heappop(heap)
        if current in seen:
            continue
        seen.add(current)

        if current[0] == (0 if player == 0 else 8):
            path=[]
            node=current
            while node is not None:
                path.append(node)
                node=parent[node]
            return path[::-1]

        r,c=current
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nxt=(r+dr,c+dc)
            if not inside(*nxt) or edge_blocked(state,current,nxt):
                continue
            ng=g+1
            if nxt not in cost or ng<cost[nxt]:
                cost[nxt]=ng
                parent[nxt]=current
                heapq.heappush(heap,(ng+heuristic(nxt,player),ng,nxt))

    return None
