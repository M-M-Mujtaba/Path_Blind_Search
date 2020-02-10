import numpy as np
from dataclasses import dataclass
import operator
from draw import *


@dataclass
class State:  # used in state grid for to store cost , depth and parent information
    Parent: []  # coordinates of the parent state
    Current: []
    cost: int  # the cost to reach this state
    depth: int  # to store the level of the node

    def __eq__(self, other):  # modifying '==' operator because a state is defined by its current coordinates
        return self.Current == other.Current


# Global variables
dimensions = []  # the dimensions of grid : size = 2. First element # rows and second element # cols
grid = None  # 2d array of all the information about the map
state_grid = None  # grid of all the states that holds the intermediate information during searching
right = [0, 1]  # constant : adding this to current coordinates would shift it one unit right
up = [1, 0]  # constant : adding this to current coordinates would shift it one unit right
di = [1, 1]  # constant : adding this to current coordinates would shift it one unit right
min_cost = 10000000  # minimum cost initialized with a large number


# stores all the states in the state grid
# position of the state is its current value
# all other positions are initialized to 0 or base value : to be modified by searching algorithm
def initialize_state_grid():
    global state_grid
    global dimensions
    state_grid = [[State([], [i, j], 0, 0) for j in range(dimensions[1])] for i in range(dimensions[0])]


# this function reads information form file and initialize the basic state of our program
def file_input(file_name):
    global dimensions
    global grid
    global state_grid
    with open(file_name, 'r') as f:
        file_data = f.read()

    file_lines = file_data.split("\n")  # all the rows of files are now stored in this list

    dimensions = [int(i) for i in file_lines[0].split(" ")]  # first thing is the dimension of the grid
    initialize_state_grid()  # with dimensions available we can initialize the grid
    start_cord = [int(i) for i in file_lines[1].split(" ")]  # second is the starting coords
    start_state = State(start_cord, start_cord, 0, 0)  # setting the start state with start coord as parent
    # current

    goal_cord = [int(i) for i in file_lines[2].split(" ")]
    goal_state = State([], goal_cord, 0, 0)

    rows = dimensions[0]
    cols = dimensions[1]
    grid = np.zeros((rows, cols), int)
    # initializing the grid
    # starting from 3 because previous rows had other information
    for i in range(3, len(file_lines) - 2):
        grid[i - 3] = [int(j) for j in file_lines[i].split(" ")]

    return start_state, goal_state


# Returns: all possible successor to the input state as list of states
def successors(state):
    States = []
    global right
    global up
    global di
    end = False  # True when we reach the upper right corner (no where to go now )
    coord = state.Current

    # check is not in edge condition
    if coord[0] < dimensions[0] - 1 and coord[1] < dimensions[1] - 1:
        right_state = State(state.Current, list(map(operator.add, right, state.Current)), state.cost + 2,
                            state.depth + 1)
        up_state = State(state.Current, list(map(operator.add, up, state.Current)), state.cost + 2, state.depth + 1)
        di_state = State(state.Current, list(map(operator.add, di, state.Current)), state.cost + 3, state.depth + 1)

        States.append(right_state)
        States.append(up_state)
        States.append(di_state)
    elif coord[0] == dimensions[0] - 1 and coord[1] == dimensions[1] - 1:  # the end point top right corner
        end = True
    elif coord[0] == dimensions[0] - 1:  # if we have reached the top
        States.append(
            State(state.Current, list(map(operator.add, right, state.Current)), state.cost + 2, state.depth + 1))
    elif coord[1] == dimensions[1] - 1:  # if we have reached the right boundary
        States.append(State(state.Current, list(map(operator.add, up, state.Current)), state.cost + 2, state.depth + 1))

    return States


# Returns the path taken by the algo
# once we have all the information we will start from Goal state and iterate to it's parents until we reach the
# start state , generating the path in the way
def generate_path(start_state, goal_state):
    path = []
    global state_grid
    cur_state = state_grid[goal_state.Parent[0]][goal_state.Parent[1]]
    while not (cur_state == start_state):
        path.append(cur_state)
        cur_state = state_grid[cur_state.Parent[0]][cur_state.Parent[1]]

    return path

# print the path on console
def print_path(start_state, goal_state):
    global grid
    global state_grid
    global min_cost
    min_cost = goal_state.cost if goal_state.cost < min_cost else min_cost
    path_grid = []
    path_row = ""


    path = generate_path(start_state, goal_state)
    print(state_grid[goal_state.Current[0]][goal_state.Current[1]])
    print("The cost of this path is {}".format(goal_state.cost))
    for i in range(dimensions[0] - 1, -1, -1):
        path_row = ""
        for j in range(dimensions[1]):
            if State([], [i, j], 0, 0) == start_state:
                print('S', end=" ")
                path_row += 'S'
            elif State([], [i, j], 0, 0) == goal_state:
                print('G', end=" ")
                path_row += 'G'
            elif State([], [i, j], 0, 0) in path:
                print('*', end=" ")
                path_row += '*'
            else:
                print(grid[i][j], end=" ")
                path_row += str(grid[i][j])
        path_grid.append(path_row)
        print(" ")

    print("", end="\n \n \n")
    draw_path(path_grid)
    a = 2





# Breadth first Blind search
def bfs(start_state, goal_state):
    global grid
    global state_grid
    found = False
    path = []
    visited = grid.copy() # don't want to modify the ordinal grid because it will be used in printing
    path.append(start_state)
    while path:
        check_state = path.pop(0)   # get the first element in list : using list as Queue

        # to make sure we do not
        # overwrite current path
        if not state_grid[check_state.Current[0]][check_state.Current[1]].Parent:
            state_grid[check_state.Current[0]][check_state.Current[1]] = check_state

        if check_state == goal_state:
            found = True
            print_path(start_state, check_state)
        visited[check_state.Current[0]][check_state.Current[1]] += 2 # adding 2 to view visiting structure
        for state in successors(check_state):   # for all of its successors
            if visited[state.Current[0]][state.Current[1]] < 1: # if not visited and not a obstacle
                path.append(state)

    return found


# simple dfs that traverses the entire grid
# if a path is found to the goal state then it returns True otherwise False
def dfs(start_state, goal_state):
    global grid
    global state_grid
    found = False
    path = []
    visited = grid.copy()
    path.append(start_state)
    while len(path) > 0:
        check_state = path.pop()  # using list as a stack
        state_grid[check_state.Current[0]][check_state.Current[1]] = check_state
        if check_state == goal_state:
            found = True
            print(state_grid)
            print_path(start_state, check_state)
            visited[check_state.Current[0]][check_state.Current[1]] -= 2
        visited[check_state.Current[0]][check_state.Current[1]] += 2
        for state in successors(check_state):
            if visited[state.Current[0]][state.Current[1]] < 1:
                path.append(state)
    return found


# max_level stores the maximum depth of the node, total_levels is the number of levels it will traverse
# returns True if path found otherwise False
def dfs_level(start_state, goal_state, total_levels, max_level):
    global grid
    global state_grid
    found = False
    path = []
    visited = grid.copy()
    path.append(start_state)
    while len(path) > 0:
        check_state = path.pop()  # using list as a stack
        state_grid[check_state.Current[0]][check_state.Current[1]] = check_state
        if check_state == goal_state:
            found = True
            print(state_grid)
            print_path(start_state, check_state)
        visited[check_state.Current[0]][check_state.Current[1]] = 2
        for state in successors(check_state):
            if visited[state.Current[0]][state.Current[1]] < 1 and state.depth <= total_levels:  # if depth is in range
                if state.depth > max_level[0]:  # storing the maximum depth in max_level
                    max_level[0] = state.depth
                path.append(state)
    return found


# returns True if path found otherwise False
def iterativedeepening(start_state, goal_state):
    max_level = [0]
    flag = True
    total_level = 0
    while flag:
        found = dfs_level(start_state, goal_state, total_level, max_level)
        if found:
            return True
        if max_level[0] < total_level:  # number of levels traversed are less than the total assigned levels
            return False
        total_level = total_level + 1
        print("total level", total_level)  # just for the sake of showing that all levels are traversed
    return False


def main():
    global dimensions
    global grid

    start_state, goal_state = file_input('grid.txt')
    print(start_state)
    print(goal_state)

    # to run a specific search uncomment it and fun the file


    # if not bfs(start_state, goal_state):
    #     print("No path found")
    initialize_state_grid()
    # if not dfs(start_state, goal_state):
    #    print("No path found")
    # print(grid)
    if not iterativedeepening(start_state, goal_state):
        print("No path found")


if __name__ == "__main__":
    main()
