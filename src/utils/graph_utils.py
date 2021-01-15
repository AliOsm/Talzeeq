"""Graph utils file to handle common graph operations.

Available methods:
- create_graph_from_qt_elements.
- is_one_connected_component.
- create_graph_topological_sort.
"""


# Built-in imports.
from typing import Dict, List, Union

# First-party package imports.
from widgets.diagram_item import DiagramItem
from widgets.arrow import Arrow


def create_graph_from_qt_elements(
    nodes: List[DiagramItem],
    edges: List[Arrow],
    nodes_mapping: Dict[DiagramItem, int],
    is_bi_directional: bool = False,
) -> List[List[int]]:
    """Generates a uni-directional graph from the given DiagramItem(s) and Arrow(s).

    Args:
        nodes: A list of DiagramItem(s) to be used as graph nodes.
        edges: A list of Arrow(s) to be used as graph edges.
        nodes_mapping: A dictionary of mappings from a DiagramItem to an integer.
        is_bi_directional: A boolean indicates whether to build uni-directional or bi-directional graph.

    Returns:
        A uni/bi-directional graph represented in adjacency list format.
    """

    graph = [list() for _ in range(len(nodes))]

    for edge in edges:
        start_item = edge.get_start_item()
        end_item = edge.get_end_item()

        graph[nodes_mapping[start_item]].append(nodes_mapping[end_item])
        if is_bi_directional:
            graph[nodes_mapping[end_item]].append(nodes_mapping[start_item])

    return graph


def is_one_connected_component(graph: List[List[int]]) -> bool:
    """Uses BFS algorithm ti check if the given bi-directional graph is one connected component of not.
    
    Reference: https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph.

    Args:
        graph: A bi-directional graph represented in adjacency list format.

    Returns:
        If the given graph is one connected component, then the returned value is True. False otherwise.
    """

    queue = [0]
    visited = [False for _ in range(len(graph))]

    while len(queue):
        current_node = queue[0]
        queue.pop(0)

        if visited[current_node]:
            continue
        visited[current_node] = True

        for child in graph[current_node]:
            queue.append(child)

    if sum(visited) != len(visited):
        return False
    return True


def create_graph_topological_sort(graph: List[List[int]]) -> Union[List[int], bool]:
    """Uses Kahn’s algorithm to creates a list contains the graph nodes sorted topologically.
    
    Reference: https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution.

    Args:
        graph: A directed acyclic graph (DAG) represented in adjacency list format.

    Returns:
        If the given graph is valid, then the returned value is a list contains the graph nodes sorted topologically.
        None otherwise.
    """
    
    nodes_in_degree = [0] * len(graph)
    for node in range(len(graph)):
        for child in graph[node]:
            nodes_in_degree[child] += 1

    queue = list()
    for index, node_in in enumerate(nodes_in_degree):
        if node_in == 0:
            queue.append(index)

    topological_sort = list()
    while len(queue):
        current_node = queue[0]
        queue.pop(0)
        topological_sort.append(current_node)

        for child in graph[current_node]:
            nodes_in_degree[child] -= 1
            if nodes_in_degree[child] == 0:
                queue.append(child)

    if len(topological_sort) != len(graph):
        return None

    return topological_sort
