import copy
import random


class PuzzleNode:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic


def print_puzzle(state):
    for row in state:
        print(" ".join(map(str, row)))
    print()


def find_blank(state):
    for i, row in enumerate(state):
        for j, value in enumerate(row):
            if value == 0:
                return i, j


def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            value = state[i][j]
            if value != 0:
                position = find_position(goal_state, value)
                if position is not None:
                    goal_i, goal_j = position
                    distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


def find_position(state, value):
    for i, row in enumerate(state):
        if value in row:
            return i, row.index(value)
    return None


def get_neighbors(state):
    i, j = find_blank(state)
    neighbors = []

    if i > 0:
        new_state = copy.deepcopy(state)
        new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        neighbors.append(new_state)

    if i < len(state) - 1:
        new_state = copy.deepcopy(state)
        new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        neighbors.append(new_state)

    if j > 0:
        new_state = copy.deepcopy(state)
        new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        neighbors.append(new_state)

    if j < len(state[0]) - 1:
        new_state = copy.deepcopy(state)
        new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
        neighbors.append(new_state)

    return neighbors


def generate_random_puzzle(size):
    flat_puzzle = [i for i in range(size * size)]
    random.shuffle(flat_puzzle)
    return [flat_puzzle[i:i+size] for i in range(0, size*size, size)]


def astar(initial_state, goal_state):
    initial_node = PuzzleNode(
        state=initial_state, heuristic=manhattan_distance(initial_state, goal_state))
    priority_queue = [initial_node]
    visited = set()

    while priority_queue:
        priority_queue.sort(key=lambda x: x.cost + x.heuristic)
        current_node = priority_queue.pop(0)

        if current_node.state == goal_state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        if tuple(map(tuple, current_node.state)) in visited:
            continue

        visited.add(tuple(map(tuple, current_node.state)))

        neighbors = get_neighbors(current_node.state)
        for neighbor_state in neighbors:
            neighbor_node = PuzzleNode(state=neighbor_state, parent=current_node, action="Move",
                                       cost=current_node.cost + 1, heuristic=manhattan_distance(neighbor_state, goal_state))
            priority_queue.append(neighbor_node)

    return None


if __name__ == "__main__":
    N = int(input("Enter the size of the puzzle (3 for 8-puzzle): "))

    # Generate random initial state and goal state
    initial_state = generate_random_puzzle(N)
    goal_state = [[i * N + j + 1 for j in range(N)] for i in range(N)]
    goal_state[N - 1][N - 1] = 0

    print("Start State:")
    print_puzzle(initial_state)

    path = astar(initial_state, goal_state)

    if path:
        print("Solution:")
        for step, state in enumerate(path):
            print(f"Step {step + 1}:")
            print_puzzle(state)
    else:
        print("No solution found.")
