# Path_Blind_Search
Using DFS , IDFS and BFS to navigate a maze

For all three algorithms we have used iterative approach and the 
Information about path is stored in a state_grid , which is same dimensions as the input grid.

In the state_grid each state is stored in it's location (A state has Parent coordinates, current coordinates
cost to reach it and the level that it is at). A state is defined by it's position in the 
state_grid, the search algorithm populates the states as it explores the search space.

After the search is completed state_grid is used to retrieve the path, and then that path is printed on console and also 
displayed on a graphical window .

Steps 

* set the file you want to read
* Run the program 
* Select 1 for BFS, 2 for DFS and 3 for IDFS
* To continue click in the Graphical window once and then press enter 
* You will again be given choices , this time when you run the code the graphical window wouldn't popup automatically so you would 
have to open it yourself from the taskbar
* To exit input 4
