import numpy as np
from dataclasses import dataclass
import operator


@dataclass
class State:
    Parent: []
    Current: []

    def __eq__(self, other):
        return self.Current == other.Current


# Global variables
dimensions = []
grid = None
right = [0, 1]
up = [1, 0]
di = [1, 1]


def file_input(file_name):
    global dimensions
    global grid
    with open(file_name, 'r') as f:
        file_data = f.read()

    file_lines = file_data.split("\n")
    dimensions = [int(i) for i in file_lines[0].split(" ")]
    start_cord = [int(i) for i in file_lines[1].split(" ")]

    start_state = State(start_cord, start_cord)

    goal_cord = [int(i) for i in file_lines[2].split(" ")]
    goal_state = State([], goal_cord)
    rows = dimensions[0]
    cols = dimensions[1]
    grid = np.zeros((rows, cols), int)
    for i in range(3, len(file_lines) - 2):
        grid[i - 3] = [int(j) for j in file_lines[i].split(" ")]

    return start_state, goal_state




def successors(state):
    States = []
    global right
    global up
    global di
    end = False
    coord = state.Current

    if coord[0] < dimensions[0] - 1 and coord[1] < dimensions[1] - 1:
        right_state = State(state.Current, list(map(operator.add, right, state.Current)))
        up_state = State(state.Current, list(map(operator.add, up, state.Current)))
        di_state = State(state.Current, list(map(operator.add, di, state.Current)))

        States.append(right_state)
        States.append(up_state)
        States.append(di_state)
    elif coord[0] == dimensions[0] - 1 and coord[1] == dimensions[1] - 1:
        end = True
    elif coord[0] == dimensions[0] - 1:
        States.append(State(state.Current, list(map(operator.add, right, state.Current))))
    else:
        States.append(State(state.Current, list(map(operator.add, up, state.Current))))

    return States, end

def main():
    global dimensions
    global grid

    start_state, goal_cord = file_input('grid.txt')
    print(grid)


if __name__ == "__main__":
    main()
