from Maze import maze, agent, COLOR, textLabel
from queue import PriorityQueue

def UCS(m, start=None):
    if start is None:
        start = (m.rows, m.cols)

    open = PriorityQueue()
    open.put((0, start))
    ucsPath = {}
    cost = {row: float("inf") for row in m.grid}
    cost[start] = 0

    searchPath = [start]

    while not open.empty():
        currCost, currCell = open.get()
        searchPath.append(currCell)

        if currCell == m._goal:
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                temp_cost = cost[currCell] + 1

                if temp_cost < cost[childCell]:
                    ucsPath[childCell] = currCell
                    cost[childCell] = temp_cost
                    open.put((temp_cost, childCell))

    fwdPath = {}
    cell = m._goal
    while cell != start:
        fwdPath[ucsPath[cell]] = cell
        cell = ucsPath[cell]

    return searchPath, ucsPath, fwdPath

