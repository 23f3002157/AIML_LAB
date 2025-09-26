import heapq
import time
import matplotlib.pyplot as plt

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __repr__(self):
        return f"PuzzleNode(state={self.state}, cost={self.cost}, heuristic={self.heuristic})"

    def string_state(self):
        return "".join(map(str, self.state))

class EightPuzzle:
    def __init__(self, initial_state):
        self.initial_state = tuple(initial_state)
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.goal_positions = {val: i for i, val in enumerate(self.goal_state)}

    def get_actions(self, state):
        actions = []
        empty_index = state.index(0)
        row, col = divmod(empty_index, 3)

        if row > 0: actions.append('U')
        if row < 2: actions.append('D')
        if col > 0: actions.append('L')
        if col < 2: actions.append('R')
        return actions

    def apply_action(self, state, action):
        new_state = list(state)
        empty_index = new_state.index(0)
        
        if action == 'U':
            swap_index = empty_index - 3
        elif action == 'D':
            swap_index = empty_index + 3
        elif action == 'L':
            swap_index = empty_index - 1
        elif action == 'R':
            swap_index = empty_index + 1
        
        new_state[empty_index], new_state[swap_index] = new_state[swap_index], new_state[empty_index]
        return tuple(new_state)

    def manhattan_distance(self, state):
        distance = 0
        for i, val in enumerate(state):
            if val != 0:
                goal_pos = self.goal_positions[val]
                current_row, current_col = divmod(i, 3)
                goal_row, goal_col = divmod(goal_pos, 3)
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def linear_conflict(self, state):
        conflicts = 0
        # Row conflicts
        for r in range(3):
            row_vals = [state[r*3+c] for c in range(3)]
            for i in range(3):
                for j in range(i + 1, 3):
                    val1, val2 = row_vals[i], row_vals[j]
                    if val1 != 0 and val2 != 0:
                        goal_pos1 = self.goal_positions[val1]
                        goal_pos2 = self.goal_positions[val2]
                        if divmod(goal_pos1, 3)[0] == r and divmod(goal_pos2, 3)[0] == r:
                            if (i < j and goal_pos1 > goal_pos2) or (i > j and goal_pos1 < goal_pos2):
                                conflicts += 2
        # Column conflicts
        for c in range(3):
            col_vals = [state[r*3+c] for r in range(3)]
            for i in range(3):
                for j in range(i + 1, 3):
                    val1, val2 = col_vals[i], col_vals[j]
                    if val1 != 0 and val2 != 0:
                        goal_pos1 = self.goal_positions[val1]
                        goal_pos2 = self.goal_positions[val2]
                        if divmod(goal_pos1, 3)[1] == c and divmod(goal_pos2, 3)[1] == c:
                            if (i < j and goal_pos1 > goal_pos2) or (i > j and goal_pos1 < goal_pos2):
                                conflicts += 2

        return self.manhattan_distance(state) + conflicts
        
    def solve(self, heuristic_func=None):
        if heuristic_func is None: # UCS
            h = lambda state: 0
        elif heuristic_func == 'manhattan':
            h = self.manhattan_distance
        elif heuristic_func == 'linear_conflict':
            h = self.linear_conflict
        else:
            raise ValueError("Invalid heuristic function specified.")

        start_node = PuzzleNode(self.initial_state, cost=0, heuristic=h(self.initial_state))
        frontier = [start_node]
        explored = set()
        nodes_expanded = 0

        while frontier:
            current_node = heapq.heappop(frontier)

            if current_node.string_state() in explored:
                continue
            
            explored.add(current_node.string_state())
            nodes_expanded += 1

            if current_node.state == self.goal_state:
                path = []
                while current_node.parent:
                    path.append(current_node.action)
                    current_node = current_node.parent
                return path[::-1], len(path), nodes_expanded

            for action in self.get_actions(current_node.state):
                new_state = self.apply_action(current_node.state, action)
                if new_state not in explored:
                    child_node = PuzzleNode(
                        state=new_state,
                        parent=current_node,
                        action=action,
                        cost=current_node.cost + 1,
                        heuristic=h(new_state)
                    )
                    heapq.heappush(frontier, child_node)
        
        return None, -1, nodes_expanded

def print_solution(name, path, cost, nodes_expanded, duration):
    print(f"--- {name} ---")
    if path:
        print(f"Solution found in {cost} moves.")
        print(f"Path: {' '.join(path)}")
    else:
        print("No solution found.")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Time Taken: {duration:.4f} seconds\n")

def plot_performance(results):
    labels = list(results.keys())
    nodes = [res['nodes'] for res in results.values()]
    times = [res['time'] for res in results.values()]
    costs = [res['cost'] for res in results.values()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.bar(labels, nodes, color=['#ff9999','#66b3ff','#99ff99'])
    ax1.set_ylabel('Nodes Expanded')
    ax1.set_title('Nodes Expanded by Algorithm')
    for i, v in enumerate(nodes):
        ax1.text(i, v + 10, str(v), ha='center', fontweight='bold')

    ax2.bar(labels, times, color=['#ff9999','#66b3ff','#99ff99'])
    ax2.set_ylabel('Time (seconds)')
    ax2.set_title('Time Taken by Algorithm')
    for i, v in enumerate(times):
        ax2.text(i, v, f"{v:.4f}", ha='center', va='bottom', fontweight='bold')

    fig.suptitle(f"Algorithm Performance (Solution Cost: {costs[0]})")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == '__main__':
    initial_puzzle_state = (7, 2, 4, 5, 0, 6, 8, 3, 1) 
    
    puzzle = EightPuzzle(initial_puzzle_state)
    results = {}

    start_time = time.time()
    path_ucs, cost_ucs, nodes_ucs = puzzle.solve(heuristic_func=None)
    duration_ucs = time.time() - start_time
    print_solution("Uniform Cost Search (UCS)", path_ucs, cost_ucs, nodes_ucs, duration_ucs)
    results['UCS'] = {'nodes': nodes_ucs, 'time': duration_ucs, 'cost': cost_ucs}

    start_time = time.time()
    path_man, cost_man, nodes_man = puzzle.solve(heuristic_func='manhattan')
    duration_man = time.time() - start_time
    print_solution("A* with Manhattan Distance", path_man, cost_man, nodes_man, duration_man)
    results['A* Manhattan'] = {'nodes': nodes_man, 'time': duration_man, 'cost': cost_man}

    start_time = time.time()
    path_lc, cost_lc, nodes_lc = puzzle.solve(heuristic_func='linear_conflict')
    duration_lc = time.time() - start_time
    print_solution("A* with Linear Conflict", path_lc, cost_lc, nodes_lc, duration_lc)
    results['A* Linear Conflict'] = {'nodes': nodes_lc, 'time': duration_lc, 'cost': cost_lc}

    plot_performance(results)

