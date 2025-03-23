import heapq

def a_star(start, goal, neighbors, heuristic):
    """
    A* search algorithm implementation.

    Args:
        start: The starting node.
        goal: The goal node.
        neighbors: A function that takes a node and returns a list of (neighbor, cost) tuples.
        heuristic: A function that takes a node and returns an estimated cost to the goal.

    Returns:
        A list of nodes representing the path from start to goal, or None if no path is found.
    """

    open_list = [(0 + heuristic(start), 0, start, [])]  # (f_score, g_score, node, path)
    closed_set = set()

    while open_list:
        f_score, g_score, current, path = heapq.heappop(open_list)

        if current == goal:
            return path + [current]

        if current in closed_set:
            continue

        closed_set.add(current)

        for neighbor, cost in neighbors(current):
            new_g_score = g_score + cost
            new_f_score = new_g_score + heuristic(neighbor)

            # Check if neighbor is in open_list with a higher g_score
            found_in_open = False
            for i, (f, g, n, p) in enumerate(open_list):
                if n == neighbor and g <= new_g_score:
                    found_in_open = True
                    break

            if found_in_open:
                continue

            heapq.heappush(open_list, (new_f_score, new_g_score, neighbor, path + [current]))

    return None  # No path found

# Example Usage (You'll need to adapt this to your map data):
def example_neighbors(node):
    """
    Example neighbor function. Replace with your actual map data.
    """
    neighbor_data = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 5), ('E', 12)],
        'C': [('A', 4), ('E', 15)],
        'D': [('B', 5), ('E', 2), ('F', 10)],
        'E': [('B', 12), ('C', 15), ('D', 2), ('F', 5)],
        'F': [('D', 10), ('E', 5)]
    }
    return neighbor_data.get(node, [])

def example_heuristic(node):
    """
    Example heuristic function. Replace with your actual heuristic (e.g., straight-line distance).
    """
    heuristic_values = {
        'A': 10,
        'B': 8,
        'C': 5,
        'D': 7,
        'E': 3,
        'F': 0
    }
    return heuristic_values.get(node, 0)

# Run the A* algorithm
start_node = 'A'
goal_node = 'F'
path = a_star(start_node, goal_node, example_neighbors, example_heuristic)

if path:
    print(f"Path from {start_node} to {goal_node}: {path}")
else:
    print(f"No path found from {start_node} to {goal_node}")