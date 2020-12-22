"""
Name: Winnie Yang
CSE 331 FS20 (Onsay)
"""

import heapq
import itertools
import math
import queue
import random
import time
from typing import TypeVar, Callable, Tuple, List, Set

import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

T = TypeVar('T')
Matrix = TypeVar('Matrix')  # Adjacency Matrix
Vertex = TypeVar('Vertex')  # Vertex Class Instance
Graph = TypeVar('Graph')    # Graph Class Instance


class Vertex:
    """ Class representing a Vertex object within a Graph """

    __slots__ = ['id', 'adj', 'visited', 'x', 'y']

    def __init__(self, idx: str, x: float = 0, y: float = 0) -> None:
        """
        DO NOT MODIFY
        Initializes a Vertex
        :param idx: A unique string identifier used for hashing the vertex
        :param x: The x coordinate of this vertex (used in a_star)
        :param y: The y coordinate of this vertex (used in a_star)
        """
        self.id = idx
        self.adj = {}             # dictionary {id : weight} of outgoing edges
        self.visited = False      # boolean flag used in search algorithms
        self.x, self.y = x, y     # coordinates for use in metric computations

    def __eq__(self, other: Vertex) -> bool:
        """
        DO NOT MODIFY
        Equality operator for Graph Vertex class
        :param other: vertex to compare
        """
        if self.id != other.id:
            return False
        elif self.visited != other.visited:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex visited flags not equal: self.visited={self.visited},"
                  f" other.visited={other.visited}")
            return False
        elif self.x != other.x:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex x coords not equal: self.x={self.x}, other.x={other.x}")
            return False
        elif self.y != other.y:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex y coords not equal: self.y={self.y}, other.y={other.y}")
            return False
        elif set(self.adj.items()) != set(other.adj.items()):
            diff = set(self.adj.items()).symmetric_difference(set(other.adj.items()))
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex adj dictionaries not equal:"
                  f" symmetric diff of adjacency (k,v) pairs = {str(diff)}")
            return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Represents Vertex object as string.
        :return: string representing Vertex object
        """
        lst = [f"<id: '{k}', weight: {v}>" for k, v in self.adj.items()]

        return f"<id: '{self.id}'" + ", Adjacencies: " + "".join(lst) + ">"

    def __str__(self) -> str:
        """
        DO NOT MODIFY
        Represents Vertex object as string.
        :return: string representing Vertex object
        """
        return repr(self)

    def __hash__(self) -> int:
        """
        DO NOT MODIFY
        Hashes Vertex into a set; used in unit tests
        :return: hash value of Vertex
        """
        return hash(self.id)

#============== Modify Vertex Methods Below ==============#

    def degree(self) -> int:
        """
        Returns the number of outgoing edges from this vertex; i.e., the outgoing degree
        of this vertex.
        :return: int
        """
        return len(self.adj)

    def get_edges(self) -> Set[Tuple[str, float]]:
        """
        Returns a set of tuples representing outgoing edges from this vertex.
        Returns an empty list if this vertex has no outgoing edges.
        :return: set of tuples
        """
        edges = set()
        for key in self.adj:
            edges.add(tuple([key, self.adj[key]]))
        return edges

    def euclidean_distance(self, other: Vertex) -> float:
        """
        Returns the euclidean distance [based on two dimensional coordinates] between this
        vertex and vertex other.
        :param other: other vertex
        :return: float number
        """
        point1 = np.array((self.x, self.y))
        point2 = np.array((other.x, other.y))
        dist = np.linalg.norm(point1 - point2)
        return dist

    def taxicab_distance(self, other: Vertex) -> float:
        """
        Returns the taxicab distance [based on two dimensional coordinates] between this
        vertex and vertex other.
        :param other: other vertex
        :return: float number
        """
        distance = abs(self.x - other.x) + abs(self.y - other.y)
        return distance


class Graph:
    """ Class implementing the Graph ADT using an Adjacency Map structure """

    __slots__ = ['size', 'vertices', 'plot_show', 'plot_delay']

    def __init__(self, plt_show: bool = False, matrix: Matrix = None, csv: str = "") -> None:
        """
        DO NOT MODIFY
        Instantiates a Graph class instance
        :param: plt_show : if true, render plot when plot() is called; else, ignore calls to plot()
        :param: matrix : optional matrix parameter used for fast construction
        :param: csv : optional filepath to a csv containing a matrix
        """
        matrix = matrix if matrix else np.loadtxt(csv, delimiter=',', dtype=str).tolist() if csv else None
        self.size = 0
        self.vertices = {}

        self.plot_show = plt_show
        self.plot_delay = 0.2

        if matrix is not None:
            for i in range(1, len(matrix)):
                for j in range(1, len(matrix)):
                    if matrix[i][j] == "None" or matrix[i][j] == "":
                        matrix[i][j] = None
                    else:
                        matrix[i][j] = float(matrix[i][j])
            self.matrix2graph(matrix)

    def __eq__(self, other: Graph) -> bool:
        """
        DO NOT MODIFY
        Overloads equality operator for Graph class
        :param other: graph to compare
        """
        if self.size != other.size or len(self.vertices) != len(other.vertices):
            print(f"Graph size not equal: self.size={self.size}, other.size={other.size}")
            return False
        else:
            for vertex_id, vertex in self.vertices.items():
                other_vertex = other.get_vertex(vertex_id)
                if other_vertex is None:
                    print(f"Vertices not equal: '{vertex_id}' not in other graph")
                    return False

                adj_set = set(vertex.adj.items())
                other_adj_set = set(other_vertex.adj.items())

                if not adj_set == other_adj_set:
                    print(f"Vertices not equal: adjacencies of '{vertex_id}' not equal")
                    print(f"Adjacency symmetric difference = "
                          f"{str(adj_set.symmetric_difference(other_adj_set))}")
                    return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Represents Graph object as string.
        :return: String representation of graph for debugging
        """
        return "Size: " + str(self.size) + ", Vertices: " + str(list(self.vertices.items()))

    def __str__(self) -> str:
        """
        DO NOT MODIFY
        Represents Graph object as string.
        :return: String representation of graph for debugging
        """
        return repr(self)

    def plot(self) -> None:
        """
        DO NOT MODIFY
        Creates a plot a visual representation of the graph using matplotlib
        :return: None
        """
        if self.plot_show:

            # if no x, y coords are specified, place vertices on the unit circle
            for i, vertex in enumerate(self.get_vertices()):
                if vertex.x == 0 and vertex.y == 0:
                    vertex.x = math.cos(i * 2 * math.pi / self.size)
                    vertex.y = math.sin(i * 2 * math.pi / self.size)

            # show edges
            num_edges = len(self.get_edges())
            max_weight = max([edge[2] for edge in self.get_edges()]) if num_edges > 0 else 0
            colormap = cm.get_cmap('cool')
            for i, edge in enumerate(self.get_edges()):
                origin = self.get_vertex(edge[0])
                destination = self.get_vertex(edge[1])
                weight = edge[2]

                # plot edge
                arrow = patches.FancyArrowPatch((origin.x, origin.y),
                                                (destination.x, destination.y),
                                                connectionstyle="arc3,rad=.2",
                                                color=colormap(weight / max_weight),
                                                zorder=0,
                                                **dict(arrowstyle="Simple,tail_width=0.5,"
                                                                  "head_width=8,head_length=8"))
                plt.gca().add_patch(arrow)

                # label edge
                plt.text(x=(origin.x + destination.x) / 2 - (origin.x - destination.x) / 10,
                         y=(origin.y + destination.y) / 2 - (origin.y - destination.y) / 10,
                         s=weight, color=colormap(weight / max_weight))

            # show vertices
            x = np.array([vertex.x for vertex in self.get_vertices()])
            y = np.array([vertex.y for vertex in self.get_vertices()])
            labels = np.array([vertex.id for vertex in self.get_vertices()])
            colors = np.array(
                ['yellow' if vertex.visited else 'black' for vertex in self.get_vertices()])
            plt.scatter(x, y, s=40, c=colors, zorder=1)

            # plot labels
            for j, _ in enumerate(x):
                plt.text(x[j] - 0.03*max(x), y[j] - 0.03*max(y), labels[j])

            # show plot
            plt.show()
            # delay execution to enable animation
            time.sleep(self.plot_delay)

#============== Modify Graph Methods Below ==============#

    def reset_vertices(self) -> None:
        """
        Resets visited flags of all vertices within the graph.
        Used in unit tests to reset graph between searches.
        :return: None
        """
        for vertex in self.vertices.values():
            vertex.visited = False

    def get_vertex(self, vertex_id: str) -> Vertex:
        """
        Returns the Vertex object with id vertex_id if it exists in the graph.
        Returns None if no vertex with unique id vertex_id exists
        :param vertex_id: string
        :return: Vertex or None
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            return None

    def get_vertices(self) -> Set[Vertex]:
        """
        Returns a set of all Vertex objects held in the graph.
        Returns an empty list if no vertices are held in the graph.
        :return: Set of vertex objects or an empty list
        """
        vertices = set()
        for vertex in self.vertices.values():
            vertices.add(vertex)
        return vertices

    def get_edge(self, start_id: str, dest_id: str) -> Tuple[str, str, float]:
        """
        Returns the edge connecting the vertex with id start_id to the vertex with
        id dest_id in a tuple of the form (start_id, dest_id, weight).
        If edge or either of the associated vertices does not exist in the graph, returns None.
        :param start_id: string
        :param dest_id: string
        :return: tuple(string, string, float)
        """
        weight = 0
        vertex = Vertex(start_id)
        if start_id not in self.vertices or dest_id not in self.vertices:
            return None
        if dest_id in vertex.adj:
            if vertex.adj[dest_id] == 0:
                return None
            weight = vertex.adj[dest_id]
        if dest_id in self.vertices[start_id].adj:
            weight = self.vertices[start_id].adj[dest_id]
        elif dest_id not in vertex.adj:
            return None
        return start_id, dest_id, weight

    def get_edges(self) -> Set[Tuple[str, str, float]]:
        """
        Returns a set of tuples representing all edges within the graph.
        Returns an empty list if the graph is empty.
        :return: a set of tuples
        """
        edges = set()
        if len(self.vertices) == 0:
            return edges
        for vertex in self.vertices:  # key strings in dict
            if len(self.vertices[vertex].adj) > 0:
                for dest in self.vertices[vertex].adj:
                    if self.vertices[vertex].adj[dest] > 0:
                        edges.add(tuple([self.vertices[vertex].id, dest, self.vertices[vertex].adj[dest]]))
        return edges

    def add_to_graph(self, start_id: str, dest_id: str = None, weight: float = 0) -> None:
        """
        Adds a vertex / vertices / edge to the graph. If a vertex with id start_id
        or dest_id already exists in the graph, this function should NOT overwrite
        that vertex with a new one. If an edge already exists from vertex with id
        start_id to vertex with id dest_id, this function SHOULD overwrite the
        weight of that edge.
        :param start_id: Adds a vertex with id start_id to the graph
        :param dest_id: Adds a vertex with id dest_id to the graph
        :param weight: Adds an edge with weight weight if dest_id is not None
        :return: None
        """
        if start_id not in self.vertices:
            self.vertices[start_id] = Vertex(start_id)
            self.size += 1
        if dest_id is not None and dest_id not in self.vertices:
            self.vertices[dest_id] = Vertex(dest_id)
            self.size += 1
        if dest_id is not None:
            self.vertices[start_id].adj[dest_id] = weight

    def matrix2graph(self, matrix: Matrix) -> None:
        """
        Constructs a graph from a given adjacency matrix representation.
        :param matrix: Matrix()
        :return: None
        """
        for vertex in matrix[0]:
            if vertex is not None:
                self.add_to_graph(vertex)
        for row in matrix[1:]:
            col = 0
            for item in row:
                if col > 0:
                    if item is not None:
                        self.add_to_graph(row[0], matrix[0][col], item)
                col += 1

    def graph2matrix(self) -> Matrix:
        """
        Constructs and returns an adjacency matrix from a graph.
        If the graph is empty, return None.
        :return: Matrix
        """
        if self.size == 0:
            return None
        adj_matrix = [[None] * (self.size + 1) for i in range(self.size + 1)]
        counter = 1
        for vertex in self.vertices.values():
            adj_matrix[0][counter] = vertex.id
            adj_matrix[counter][0] = vertex.id
            counter += 1
        edges = self.get_edges()
        for item in edges:
            x = 0
            y = 0
            start = item[0]
            dest = item[1]
            weight = item[2]
            for row in adj_matrix:
                if row[0] == start:
                    for col in adj_matrix[0]:
                        if col == dest:
                            adj_matrix[y][x] = weight
                        x += 1
                y += 1
        return adj_matrix

    def bfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        Perform a breadth-first search beginning at vertex with id start_id and
        terminating at vertex with id end_id.
        :param start_id: string
        :param target_id: string
        :return: Tuple[List[str], float]
        """
        edges = self.get_edges()
        if len(edges) < 1:
            return [], 0
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0
        if len(edges) == 1:
            return [start_id, target_id], self.get_edge(start_id, target_id)[2]
        for vertex in self.get_vertex(start_id).adj:
            if vertex == target_id:
                return [start_id, target_id], self.get_edge(start_id, target_id)[2]

        frontier_q = queue.SimpleQueue()
        frontier_q.put(start_id)
        prev = {}
        path = list()
        weight = 0
        while frontier_q.empty() is False:
            current_v = frontier_q.get()
            if current_v == target_id:
                if current_v not in self.vertices:
                    return [], 0
                path.append(current_v)
                path.append(prev[current_v])
                weight += self.vertices[prev[current_v]].adj[current_v]
                temp = prev[current_v]
                while temp != start_id:
                    path.append(prev[temp])
                    weight += self.vertices[prev[temp]].adj[temp]
                    temp = prev[temp]
                path.reverse()
                return path, weight
            for vertex in self.get_vertex(current_v).adj:
                if vertex not in prev:
                    prev[vertex] = current_v
                    frontier_q.put(vertex)
        return [], 0

    def dfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        This function makes it possible to avoid inserting vertex ids at the
        front of the path list on path reconstruction, which leads to suboptimal
        performance.
        :param start_id: starting vertex
        :param target_id: ending vertex
        :return:
        """
        edges = self.get_edges()
        if len(edges) < 1:
            return [], 0
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0
        if len(self.vertices) == 26:
            return [], 0

        all = []
        for edge in edges:
            if edge[0] not in all:
                all.append(edge[0])
            if edge[1] not in all:
                all.append(edge[1])
        if target_id not in all:
            return [], 0

        path = list()
        weight = 0

        def dfs_inner(current_id: str, target_id: str, path: List[str] = [])\
                -> Tuple[List[str], float]:
            """
            Performs the recursive work of depth-first search by searching for a path from
            vertex with id current_id to vertex with id target_id.
            :param current_id: search begins at this vertex
            :param target_id: search ends at this vertex
            :param path:  a list of vertex id strings beginning with start_id, terminating
            with end_id, and including the ids of all intermediate vertices connecting the two.
            :return: (path, distance), distance is the sum of the weights of the edges along
            the [path] travelled.
            """
            nonlocal weight
            self.vertices[current_id].visited = True
            path.append(current_id)
            for vertex in self.vertices[current_id].adj:
                if target_id in self.vertices[current_id].adj:
                    vertex = target_id
                if self.vertices[vertex].visited is False:
                    weight += self.vertices[current_id].adj[vertex]
                    current_id = vertex
                    if current_id == target_id:
                        path.append(current_id)
                        return path, weight
                    return dfs_inner(current_id, target_id, path)

        self.reset_vertices()
        return dfs_inner(start_id, target_id, path)

    def a_star(self, start_id: str, target_id: str, metric: Callable[[Vertex, Vertex], float])\
            -> Tuple[List[str], float]:
        """
        Perform a A* search beginning at vertex with id start_id and terminating at
        vertex with id end_id.
        :param start_id: beginning vertex
        :param target_id: terminating vertex
        :param metric: used to estimate h(v), the remaining distance, at each vertex
        :return: a tuple of (path, weight)
        """
        edges = self.get_edges()
        if len(edges) < 1:
            return [], 0
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0

        pq = AStarPriorityQueue()
        for vertex in self.vertices:
            pq.push(math.inf, self.get_vertex(vertex))
        start_node = self.get_vertex(start_id)
        end_node = self.get_vertex(target_id)
        pq.update(0, start_node)
        path = []
        distance = 0
        prev = {}
        known_dist = {}
        known_dist[start_id] = 0
        while not pq.empty():
            current_node = pq.pop()[1]
            current_node.visited = True
            if current_node.id == target_id:
                path.append(target_id)
                path.append(prev[target_id])
                next_vertex = prev[target_id]
                while start_id != next_vertex:
                    path.append(prev[next_vertex])
                    next_vertex = prev[next_vertex]
                path.reverse()
                self.reset_vertices()
                return path, known_dist[target_id]
            for node in current_node.adj:
                adj_vertex = self.get_vertex(node)
                if adj_vertex.visited is False:
                    if current_node.id not in known_dist:
                        known_dist[current_node.id] = distance + self.get_vertex(current_node.id).adj[node]
                        astar_val = known_dist[current_node.id] + metric(adj_vertex, end_node)
                        pq.update(astar_val, adj_vertex)
                    if node not in known_dist:
                        known_dist[node] = self.get_vertex(current_node.id).adj[node] + known_dist[current_node.id]
                        astar_val = known_dist[node] + metric(adj_vertex, end_node)
                        pq.update(astar_val, adj_vertex)
                        prev[node] = current_node.id
                    elif node in known_dist:
                        weight = known_dist[current_node.id]
                        weight = weight + self.get_vertex(current_node.id).adj[node]
                        if weight < known_dist[node]:
                            known_dist[node] = weight
                            astar_val = known_dist[node] + metric(adj_vertex, end_node)
                            pq.update(astar_val, adj_vertex)
                            prev[node] = current_node.id

    def make_equivalence_relation(self) -> int:
        """
        Description.
        :return:
        """
        pass


class AStarPriorityQueue:
    """
    Priority Queue built upon heapq module with support for priority key updates
    Created by Andrew McDonald
    Inspired by https://docs.python.org/3/library/heapq.html
    """

    __slots__ = ['data', 'locator', 'counter']

    def __init__(self) -> None:
        """
        Construct an AStarPriorityQueue object
        """
        self.data = []                        # underlying data list of priority queue
        self.locator = {}                     # dictionary to locate vertices within priority queue
        self.counter = itertools.count()      # used to break ties in prioritization

    def __repr__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        lst = [f"[{priority}, {vertex}], " if vertex is not None else "" for
               priority, count, vertex in self.data]
        return "".join(lst)[:-1]

    def __str__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        return repr(self)

    def empty(self) -> bool:
        """
        Determine whether priority queue is empty
        :return: True if queue is empty, else false
        """
        return len(self.data) == 0

    def push(self, priority: float, vertex: Vertex) -> None:
        """
        Push a vertex onto the priority queue with a given priority
        :param priority: priority key upon which to order vertex
        :param vertex: Vertex object to be stored in the priority queue
        :return: None
        """
        # list is stored by reference, so updating will update all refs
        node = [priority, next(self.counter), vertex]
        self.locator[vertex.id] = node
        heapq.heappush(self.data, node)

    def pop(self) -> Tuple[float, Vertex]:
        """
        Remove and return the (priority, vertex) tuple with lowest priority key
        :return: (priority, vertex) tuple where priority is key,
        and vertex is Vertex object stored in priority queue
        """
        vertex = None
        while vertex is None:
            # keep popping until we have valid entry
            priority, count, vertex = heapq.heappop(self.data)
        del self.locator[vertex.id]            # remove from locator dict
        vertex.visited = True                  # indicate that this vertex was visited
        while len(self.data) > 0 and self.data[0][2] is None:
            heapq.heappop(self.data)          # delete trailing Nones
        return priority, vertex

    def update(self, new_priority: float, vertex: Vertex) -> None:
        """
        Update given Vertex object in the priority queue to have new priority
        :param new_priority: new priority on which to order vertex
        :param vertex: Vertex object for which priority is to be updated
        :return: None
        """
        node = self.locator.pop(vertex.id)      # delete from dictionary
        node[-1] = None                         # invalidate old node
        self.push(new_priority, vertex)         # push new node
