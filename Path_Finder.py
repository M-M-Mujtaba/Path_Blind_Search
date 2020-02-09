import numpy as np
from dataclasses import dataclass
import operator




@dataclass
class State:
    Parent: []
    Current: []
    cost: int

    def __eq__(self, other):
        return self.Current == other.Current


# Global variables
dimensions = []
grid = None  # 2d array of all the information about the map
state_grid = None
right = [0, 1]
up = [1, 0]
di = [1, 1]
min_cost = 100000


def file_input(file_name):
    global dimensions
    global grid
    global state_grid
    with open(file_name, 'r') as f:
        file_data = f.read()

    file_lines = file_data.split("\n")

    dimensions = [int(i) for i in file_lines[0].split(" ")]  # first thing is the dimension of the grid
    state_grid = [[State([], [i, j], 0) for j in range(dimensions[1])] for i in range(dimensions[0])]
    start_cord = [int(i) for i in file_lines[1].split(" ")]  # second is the starting coords
    start_state = State(start_cord, start_cord, 0)  # setting the start state with start cood as parent and
    # current

    goal_cord = [int(i) for i in file_lines[2].split(" ")]
    goal_state = State([], goal_cord, 0)

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
    end = False  # True when we reach the upper right corner (no where to go now )
    coord = state.Current

    if coord[0] < dimensions[0] - 1 and coord[1] < dimensions[1] - 1:
        right_state = State(state.Current, list(map(operator.add, right, state.Current)), state.cost + 2)
        up_state = State(state.Current, list(map(operator.add, up, state.Current)), state.cost + 2)
        di_state = State(state.Current, list(map(operator.add, di, state.Current)), state.cost + 3)

        States.append(right_state)
        States.append(up_state)
        States.append(di_state)
    elif coord[0] == dimensions[0] - 1 and coord[1] == dimensions[1] - 1:
         end = True
    elif coord[0] == dimensions[0] - 1:
        States.append(State(state.Current, list(map(operator.add, right, state.Current)), state.cost + 2))
    elif coord[1] == dimensions[1] - 1:
        States.append(State(state.Current, list(map(operator.add, up, state.Current)), state.cost + 2))

    return States


def generate_path(start_state, goal_state):
    path = []
    global state_grid
    cur_state = state_grid[goal_state.Parent[0]][goal_state.Parent[1]]
    while not (cur_state == start_state):
        path.append(cur_state)
        cur_state = state_grid[cur_state.Parent[0]][cur_state.Parent[1]]

    return path


def print_path(start_state, goal_state):
    global grid
    global state_grid
    global min_cost
    min_cost = goal_state.cost if goal_state.cost < min_cost else min_cost

    path = generate_path(start_state, goal_state)
    print(state_grid[goal_state.Current[0]][goal_state.Current[1]])
    print("The cost of this path is {}".format(goal_state.cost))
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            if State([], [i, j], 0) == start_state:
                print('S', end=" ")
            elif State([], [i, j], 0) == goal_state:
                print('G', end=" ")
            elif State([], [i, j], 0) in path:
                print('*', end=" ")
            else:
                print(grid[i][j], end=" ")
        print(" ")

    print("", end="\n \n \n")


def bfs(start_state, goal_state):
    global grid
    global state_grid
    found = False
    path = []
    visited = grid.copy()
    path.append(start_state)
    while len(path) > 0:
        check_state = path.pop(0)
        if not state_grid[check_state.Current[0]][check_state.Current[1]].Parent:
            state_grid[check_state.Current[0]][check_state.Current[1]] = check_state
        if check_state == goal_state:
            found = True
            print(state_grid)
            print_path(start_state, check_state)
        visited[check_state.Current[0]][check_state.Current[1]] = 2
        for state in successors(check_state):
            if visited[state.Current[0]][state.Current[1]] < 1:
                path.append(state)

    return found


def dfs(start_state, goal_state):
    global grid
    global state_grid
    found = False
    path = []
    visited = grid.copy()
    path.append(start_state)
    while len(path) > 0:
        check_state = path.pop() #using list as a stack
        state_grid[check_state.Current[0]][check_state.Current[1]] = check_state
        if check_state == goal_state:
            found = True
            print(state_grid)
            print_path(start_state, check_state)
        visited[check_state.Current[0]][check_state.Current[1]] = 2
        for state in successors(check_state):
            if visited[state.Current[0]][state.Current[1]] < 1:
                path.append(state)
    return found


def dfs_level(start_state, goal_state, level, x):
    global grid
    global state_grid
    found = False
    path = []
    visited = grid.copy()
    path.append(start_state)
    while len(path) > 0:
        check_state = path.pop() #using list as a stack
        state_grid[check_state.Current[0]][check_state.Current[1]] = check_state
        if check_state == goal_state:
            found = True
            print(state_grid)
            print_path(start_state, check_state)
        visited[check_state.Current[0]][check_state.Current[1]] = 2

        if level > 0: #if there are levels to check
            level=level-1   #remaining levels to check
            for state in successors(check_state):
                if visited[state.Current[0]][state.Current[1]] < 1:
                    path.append(state)

    if level > 0:   #if there were more levels given and the depth in reality was less
        x[0]= 1
    return found

def iterativedeeping(start_state,goal_state):
    value =[0]
    flag=True
    level =0
    while flag:
        if dfs_level(start_state, goal_state,level, value):
            return True
        if value[0]==1:   #total depth has been checked
            return False
        level=level+1     #increase level of depth by 1
    return False

def main():
    global dimensions
    global grid

    start_state, goal_state = file_input('grid.txt')
    print(start_state)
    print(goal_state)
    if not bfs(start_state, goal_state):
        print("No path found")
    if not dfs(start_state, goal_state):
        print("No path found")

    print(grid)


if __name__ == "__main__":
    main()
