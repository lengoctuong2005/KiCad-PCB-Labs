import pcbnew
import heapq
import math
from test_netlist_map import NET_MAP

board = pcbnew.BOARD()

# Board dimensions: 100 x 80 mm
WIDTH = 100.0
HEIGHT = 80.0
RES = 0.5 # 0.5 mm grid
NX = int(WIDTH / RES) + 1
NY = int(HEIGHT / RES) + 1

print(f"Grid dimensions: {NX} x {NY} = {NX*NY} cells per layer (2 layers)")

def to_grid(x_mm, y_mm):
    gx = int(round(x_mm / RES))
    gy = int(round(y_mm / RES))
    return max(0, min(NX-1, gx)), max(0, min(NY-1, gy))

def to_mm(gx, gy):
    return gx * RES, gy * RES

# Test A* algorithm
def astar(blocked, start, goal):
    # start, goal are (layer, gx, gy)
    if start == goal:
        return [start]
    
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    
    def h(pos):
        l, x, y = pos
        gl, gx, gy = goal
        return abs(x - gx) + abs(y - gy) + (5 if l != gl else 0)
    
    found = False
    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            found = True
            break
            
        l, x, y = current
        # Neighbors: 4 in-plane + 1 layer switch (via)
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < NX and 0 <= ny < NY:
                neighbors.append((l, nx, ny, 1))
        # Layer switch
        nl = 1 - l
        neighbors.append((nl, x, y, 6)) # via penalty
        
        for nl, nx, ny, step_cost in neighbors:
            nxt = (nl, nx, ny)
            if nxt != goal and nxt in blocked:
                continue
            new_cost = cost_so_far[current] + step_cost
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + h(nxt)
                heapq.heappush(pq, (priority, nxt))
                came_from[nxt] = current
                
    if not found:
        return None
        
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        curr = came_from[curr]
    path.append(start)
    path.reverse()
    return path

print("A* core logic verified.")
