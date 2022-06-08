from __future__ import division
from __future__ import print_function

import queue
import sys
import math
import time
import queue as Q


#### SKELETON CODE ####
## The Class that Represents the Puzzle

class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if 0 <= self.blank_index <= self.n - 1:
            return None
        config = self.config[:]
        blank = self.blank_index
        goal = self.blank_index - self.n
        config[blank], config[goal] = config[goal], config[blank]
        state = PuzzleState(config=config, n=self.n, parent=self, action="Up", cost=self.cost + 1)
        return state

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.n * (self.n - 1) <= self.blank_index <= self.n * self.n - 1:
            return None
        config = self.config[:]
        blank = self.blank_index
        goal = self.blank_index + self.n
        config[blank], config[goal] = config[goal], config[blank]
        state = PuzzleState(config=config, n=self.n, parent=self, action="Down", cost=self.cost + 1)
        return state

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        for i in range(0, self.n * self.n, self.n):
            if self.blank_index == i:
                return None
        config = self.config[:]
        blank = self.blank_index
        goal = self.blank_index - 1
        config[blank], config[goal] = config[goal], config[blank]
        state = PuzzleState(config=config, n=self.n, parent=self, action="Left", cost=self.cost + 1)
        return state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        for i in range(self.n - 1, self.n * self.n + self.n, self.n):
            if self.blank_index == i:
                return None
        # if self.blank_index == 2 or self.blank_index == 5 or self.blank_index == 8:
        #     return None
        config = self.config[:]
        blank = self.blank_index
        goal = self.blank_index + 1
        config[blank], config[goal] = config[goal], config[blank]
        state = PuzzleState(config=config, n=self.n, parent=self, action="Right", cost=self.cost + 1)
        return state

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

    def __lt__(self, other):
        return calculate_total_cost(self) <= calculate_total_cost(other)


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, max_search_depth, nodes_expanded, time, ram_usage):
    ### Student Code Goes here
    path_to_goal = []
    cost_of_path = state.cost
    search_depth = state.cost
    cur_state = state

    while cur_state.parent:
        path_to_goal.append(cur_state.action)
        cur_state = cur_state.parent

    path_to_goal = path_to_goal[::-1]

    with open("output.txt", "w") as f:
        f.write("path_to_goal: " + str(path_to_goal) + '\n')
        f.write("cost_of_path: " + str(cost_of_path) + '\n')
        f.write("nodes_expanded: " + str(nodes_expanded) + '\n')
        f.write("search_depth: " + str(search_depth) + '\n')
        f.write("max_search_depth: " + str(max_search_depth) + '\n')
        f.write("running_time: " + str(time) + '\n')
        f.write("max_ram_usage: " + str(ram_usage))

def bfs_search(initial_state):
    import time
    import psutil
    import os
    start_time = time.time()
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    nodes_expanded = 0
    max_search_depth = 0
    frontier = queue.Queue()
    frontier_config = set()
    # explored = set()
    explored_config = set()
    frontier.put(initial_state)
    frontier_config.add(tuple(initial_state.config))

    while frontier.qsize() > 0:
        state = frontier.get()
        frontier_config.remove(tuple(state.config))
        # explored.add(state)
        explored_config.add(tuple(state.config))

        if test_goal(state):
            while frontier.qsize() > 0:
                s = frontier.get()
                max_search_depth = max(max_search_depth, s.cost)
            end_time = time.time()
            time = end_time - start_time
            ram_usage = psutil.Process(os.getpid()).memory_info().rss / pow(10, 6)
            writeOutput(state, max_search_depth, nodes_expanded, time, ram_usage)
            return True

        nodes_expanded += 1

        children = state.expand()
        for child in children:
            if tuple(child.config) not in frontier_config and tuple(child.config) not in explored_config:
                frontier.put(child)
                frontier_config.add(tuple(child.config))

    # print("fail")
    return False


def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    import time
    import psutil
    import os

    max_search_depth = 0
    start_time = time.time()
    nodes_expanded = 0
    frontier = []
    frontier_config = set()
    # explored = set()
    explored_config = set()
    frontier.append(initial_state)
    frontier_config.add(tuple(initial_state.config))

    while len(frontier) > 0:
        state = frontier.pop()
        frontier_config.remove(tuple(state.config))
        # explored.add(state)
        explored_config.add(tuple(state.config))
        max_search_depth = max(max_search_depth, state.cost)
        if test_goal(state):
            end_time = time.time()
            time = end_time - start_time
            ram_usage = psutil.Process(os.getpid()).memory_info().rss / pow(10, 6)
            writeOutput(state, max_search_depth, nodes_expanded, time, ram_usage)
            return True

        nodes_expanded += 1

        children = state.expand()[::-1]
        for child in children:
            if tuple(child.config) not in frontier_config and tuple(child.config) not in explored_config:
                frontier.append(child)
                frontier_config.add(tuple(child.config))

    # print("fail")
    return False


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    import time
    import psutil
    import os

    start_time = time.time()
    nodes_expanded = 0
    frontier = Q.PriorityQueue()
    frontier_config = set()
    # explored = set()
    explored_config = set()
    frontier.put(initial_state)
    frontier_config.add(tuple(initial_state.config))

    while frontier.qsize() > 0:
        state = frontier.get()
        frontier_config.remove(tuple(state.config))
        # explored.add(state)
        explored_config.add(tuple(state.config))

        if test_goal(state):
            max_search_depth = state.cost
            end_time = time.time()
            time = end_time - start_time
            ram_usage = psutil.Process(os.getpid()).memory_info().rss / pow(10, 6)
            writeOutput(state, max_search_depth, nodes_expanded, time, ram_usage)
            return True

        nodes_expanded += 1

        children = state.expand()
        for child in children:
            if tuple(child.config) not in frontier_config and tuple(child.config) not in explored_config:
                frontier.put(child)
                frontier_config.add(tuple(child.config))

    # print("fail")
    return False

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    config = state.config
    cost = state.cost
    for idx, value in enumerate(config):
        cost += calculate_manhattan_dist(idx, value, state.n)
    return cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    row = idx // n
    col = idx % n
    row_goal = value // n
    col_goal = value % n
    dist = abs(row - row_goal) + abs(col - col_goal)
    return dist


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    for idx, value in enumerate(puzzle_state.config):
        if idx != value:
            return False
    return True
    # if puzzle_state.config == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
    #     return True
    # return False


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == '__main__':
    main()
