from graphics import *
# def draw_path(start_state, goal_state):
#     global grid
#     global state_grid
#     global min_cost
#
#     path = generate_path(start_state, goal_state)


def draw_path(grid, algo_name, cost ):


    win = GraphWin(algo_name, 700, 700)
    block_size = 35
    start_x = 200
    start_y = 100
    Help_message =Text(Point(300, 50), "1) Press on the screen to exit, do not press x")
    Message = Text(Point(300, 75), "2) The cost for this path is {} \n3) The path is on the console".format(cost))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            block = Rectangle(Point(start_x + (j * block_size), start_y + (i * block_size)), Point(start_x + (j * block_size) + block_size, start_y + (i * block_size) + block_size))
            if grid[i][j] == '1':
                block.setFill("black")
            elif grid[i][j] == 'S':
                block.setFill("blue")
            elif grid[i][j] == 'G':
                block.setFill("red")
            elif grid[i][j] == '*':
                block.setFill("green")
            block.draw(win)
    Message.draw(win)
    Help_message.setFill("red")
    Help_message.draw(win)


    win.getMouse()

