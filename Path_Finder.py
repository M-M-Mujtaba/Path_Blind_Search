import numpy as np
from collections import namedtuple

State = namedtuple('parent', 'Coord')


# Global variables
dimensions = []
grid = None

def file_input(file_name):
    global dimensions
    global grid
    with open(file_name, 'r') as f:
        file_data = f.read()

    file_lines = file_data.split("\n")
    dimensions = [int(i) for i in file_lines[0].split(" ")]
    start_cord = [int(i) for i in file_lines[1].split(" ")]
    start_state = (start_cord, start_cord)
    goal_cord = [int(i) for i in file_lines[2].split(" ")]
    rows = dimensions[0]
    cols = dimensions[1]
    grid = np.zeros((rows, cols), int)
    for i in range(3, len(file_lines) - 2):
        grid[i - 3] = [int(j) for j in file_lines[i].split(" ")]

    return start_state, goal_cord


def main():
    global dimensions
    global grid

    start_state, goal_cord = file_input('grid.txt')
    print(grid)


if __name__ == "__main__":
    main()
