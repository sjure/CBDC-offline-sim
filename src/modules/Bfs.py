from queue import Queue
from modules.Types import NETWORK, INTERMEDIARY


def bfs_to_intermediary(start_node):
    """ BFS search """
    visited = set()
    queue = Queue()

    queue.put(start_node)
    visited.add(start_node)
    path_found = False
    intermediary_node = -1
    while not queue.empty():
        current_node_data = queue.get()
        current_node_id = current_node_data.node_id
        if (current_node_data.type == INTERMEDIARY and current_node_data.is_online):
            path_found = True
            intermediary_node = current_node_data
            break
        elif ((current_node_data.type == NETWORK and current_node_data.is_online) or current_node_id == start_node.node_id):
            for next_node in current_node_data.network_neighbors:
                if next_node not in visited:
                    queue.put(next_node)
                    visited.add(next_node)

    return (path_found, intermediary_node)
