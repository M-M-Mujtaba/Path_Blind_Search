import numpy as np
from dataclasses import dataclass
import operator
import watson_text_talker


@dataclass
class State:
    Parent: []
    Current: []

    def __eq__(self, other):
        return self.Current == other.Current


# Global variables
dimensions = []
grid = None  # 2d array of all the information about the map
right = [0, 1]
up = [1, 0]
di = [1, 1]


def file_input(file_name):
    global dimensions
    global grid
    with open(file_name, 'r') as f:
        file_data = f.read()

    file_lines = file_data.split("\n")

    dimensions = [int(i) for i in file_lines[0].split(" ")]  # first thing is the dimension of the grid

    start_cord = [int(i) for i in file_lines[1].split(" ")]  # second is the starting coords
    start_state = State(start_cord, start_cord)  # setting the start state with start cood as parent and
    # current

    goal_cord = [int(i) for i in file_lines[2].split(" ")]
    goal_state = State([], goal_cord)

    rows = dimensions[0]
    cols = dimensions[1]
    grid = np.zeros((rows, cols), int)  # initializing the grid
    for i in range(3, len(file_lines) - 2):
        grid[i - 3] = [int(j) for j in file_lines[i].split(" ")]

    return start_state, goal_state


def successors(state):
    States = []
    global right
    global up
    global di
    # end = False  # True when we reach the upper right corner (no where to go now )
    coord = state.Current

    if coord[0] < dimensions[0] - 1 and coord[1] < dimensions[1] - 1:
        right_state = State(state.Current, list(map(operator.add, right, state.Current)))
        up_state = State(state.Current, list(map(operator.add, up, state.Current)))
        di_state = State(state.Current, list(map(operator.add, di, state.Current)))

        States.append(right_state)
        States.append(up_state)
        States.append(di_state)
    # elif coord[0] == dimensions[0] - 1 and coord[1] == dimensions[1] - 1:
    # end = True
    elif coord[0] == dimensions[0] - 2:
        States.append(State(state.Current, list(map(operator.add, right, state.Current))))
    elif coord[1] == dimensions[1] - 2:
        States.append(State(state.Current, list(map(operator.add, up, state.Current))))

    return States


def print_path(path, start_state, goal_state):
    global grid

    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            if State([], [i, j]) == start_state:
                print('S', end=" ")
            elif State([], [i, j]) == goal_state:
                print('G', end=" ")
            elif State([], [i, j]) in path:
                print('*', end=" ")
            else:
                print(grid[i][j], end=" ")
        print(" ")

    print("", end="\n \n \n")


def bfs(start_state, goal_state):
    global grid
    found = False
    path = []
    visited = grid.copy()
    path.append(start_state)
    while len(path) > 0:
        check_state = path.pop(0)
        if check_state == goal_state:
            found = True
            print_path(path, start_state, goal_state)
        visited[check_state.Current[0]][check_state.Current[1]] = 2
        for state in successors(check_state):
            if visited[state.Current[0]][state.Current[1]] < 1:
                path.append(state)

    return found


def main():
    global dimensions
    global grid

    start_state, goal_state = file_input('grid.txt')
    print(start_state)
    print(goal_state)
    if not bfs(start_state, goal_state):
        print("No path found")

    print(grid)


if __name__ == "__main__":
    main()
