from enum import unique
from re import A
from xml.dom.pulldom import END_ELEMENT
from Vertex import Vertex
from queue import PriorityQueue

"""
Graph Class
----------

This class represents the Graph modelling our courier network. 

Each Graph consists of the following properties:
    - vertices: A list of vertices comprising the graph

The class also supports the following functions:
    - add_vertex(vertex): Adds the vertex to the graph
    - remove_vertex(vertex): Removes the vertex from the graph
    - add_edge(vertex_A, vertex_B): Adds an edge between the two vertices
    - remove_edge(vertex_A, vertex_B): Removes an edge between the two vertices
    - send_message(s, t): Returns a valid path from s to t containing at most one untrusted vertex
    - check_security(s, t): Returns the set of edges that, if any are removed, would result in any s-t path having to use an untrusted edge

Your task is to complete the following functions which are marked by the TODO comment.
Note that your modifications to the structure of the Graph should be correctly updated in the underlying Vertex class!
You are free to add properties and functions to the class as long as the given signatures remain identical.
"""


class Graph():
    # These are the defined properties as described above
    vertices: 'list[Vertex]'

    def __init__(self) -> None:
        """
        The constructor for the Graph class.
        """
        self.vertices = []

    def add_vertex(self, vertex: Vertex) -> None:
        """
        Adds the given vertex to the graph.
        If the vertex is already in the graph or is invalid, do nothing.
        :param vertex: The vertex to add to the graph.
        """

        if vertex not in self.vertices and isinstance(vertex, Vertex):
            self.vertices.append(vertex)

    def remove_vertex(self, vertex: Vertex) -> None:
        """
        Removes the given vertex from the graph.
        If the vertex is not in the graph or is invalid, do nothing.
        :param vertex: The vertex to remove from the graph.
        """

        if vertex in self.vertices and isinstance(vertex, Vertex):
            self.vertices.remove(vertex)

    def add_edge(self, vertex_A: Vertex, vertex_B: Vertex) -> None:
        """
        Adds an edge between the two vertices.
        If adding the edge would result in the graph no longer being simple or the vertices are invalid, do nothing.
        :param vertex_A: The first vertex.
        :param vertex_B: The second vertex.
        """

        # TODO Fill this in
        if vertex_A in self.vertices and vertex_B in self.vertices and isinstance(vertex_A, Vertex)  and isinstance(vertex_B, Vertex):
            vertex_A.add_edge(vertex_B)


    def remove_edge(self, vertex_A: Vertex, vertex_B: Vertex) -> None:
        """
        Removes an edge between the two vertices.
        If an existing edge does not exist or the vertices are invalid, do nothing.
        :param vertex_A: The first vertex.
        :param vertex_B: The second vertex.
        """

        if vertex_A in self.vertices and vertex_B in self.vertices and isinstance(vertex_A, Vertex)  and isinstance(vertex_B, Vertex):
            vertex_A.remove_edge(vertex_B)

    def send_message(self, s: Vertex, t: Vertex) -> 'list[Vertex]':
        """
        Returns a valid path from s to t containing at most one untrusted vertex.
        Any such path between s and t satisfying the above condition is acceptable.
        Both s and t can be assumed to be unique and trusted vertices.
        If no such path exists, return None.
        :param s: The starting vertex.
        :param t: The ending vertex.
        :return: A valid path from s to t containing at most one untrusted vertex.
        """

        if not (s in self.vertices and t in self.vertices and isinstance(s, Vertex) and isinstance(t, Vertex)):
            return []

        untrustedVertex = 0
        stack = [(s, [s])]
        visited = set()

        while stack:
            (vertex, path) = stack.pop()
            untrustedVertex = self.check_path_security(path)

            if vertex not in visited:
                if vertex == t and untrustedVertex <= 1:
                    return path
                visited.add(vertex)
                for neighbour in vertex.get_edges():
                    stack.append((neighbour, path + [neighbour]))

        return []


    def check_path_security(self, path: 'list[Vertex]') -> int:
        """
        Returns the number of untrusted vertices in the path.
        :param path: The path to check.
        :return: The number of untrusted vertices in the path.
        """
        untrusted = [ 1 for i in range(len(path)) if path[i].get_is_trusted() == False ]

        return sum(untrusted)
        

    def path_finder(self, start: Vertex, end: Vertex, path=[]) -> 'list[Vertex]':
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.vertices:
            return []
        paths = []
        for vertex in start.edges:
            if vertex not in path:
                newpaths = self.path_finder(vertex, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        
        # for i in range(len(paths)):
        #     for v in paths[i]:
        #         print(v, end=' ')
        #     print()
                
        return paths


    def is_path_secure(self, path: 'list[Vertex]') -> bool:
        """
        Returns True if the path is secure, False otherwise.
        :param path: The path to check.
        :return: True if the path is secure, False otherwise.
        """

        last_node = True
        for i in range(len(path)):
            if path[i].get_is_trusted() == False:
                if last_node == False:
                    return False
                last_node = False
            else:
                last_node = True
        return True

    def get_edges_from_graph(self) -> 'list[(Vertex, Vertex)]':
        """
        Returns a list of all edges in the graph.
        :return: A list of all edges in the graph.
        """
        edges = []
        
        for vertex in self.vertices:
            for edge in vertex.get_edges():
                edge_set = {vertex, edge}
                if edge_set not in edges:
                    edges.append(edge_set)
                    # print([f"{vertex} {edge}" for vertex, edge in edges])
        
        return edges


    def semitrusted_edges_from_set_edges(self, edges: 'list[set(Vertex, Vertex)]') -> 'list[(Vertex, Vertex)]':
        """
        Returns a list of all untrusted edges in the graph.
        :param edges: A list of all edges in the graph.
        :return: A list of all untrusted edges in the graph.
        """
        semi_trusted_edges = []
        for edge in edges:
            edge_list = list(edge)
            if edge_list[0].get_is_trusted() != edge_list[1].get_is_trusted():
                semi_trusted_edges.append(tuple(edge_list))
                # print(f"{edge_list[0]} {edge_list[1]}")
        return semi_trusted_edges

    def check_security(self, s: Vertex, t: Vertex) -> 'list[(Vertex, Vertex)]':
        """
        Returns the list of edges as tuples of vertices (v1, v2) such that the removal 
        of the edge (v1, v2) means a path between s and t is not possible or must use
        two or more untrusted vertices in a row. v1 and v2 must also satisfy the criteria
        that exactly one of v1 or v2 is trusted and the other untrusted.        
        Both s and t can be assumed to be unique and trusted vertices.
        :param s: The starting vertex
        :param t: The ending vertex
        :return: A list of edges which, if removed, means a path from s to t uses an untrusted edge or is no longer possible. 
        Note these edges can be returned in any order and are unordered.
        """

        if not (s in self.vertices and t in self.vertices and isinstance(s, Vertex) and isinstance(t, Vertex)):
            return []

        all_paths = self.path_finder(s, t)

        if len(all_paths) == 0:
            set_edges = self.get_edges_from_graph()
            semi_trusted_edges = self.semitrusted_edges_from_set_edges(set_edges)
            return semi_trusted_edges


        # remove the paths which have 2 untrusted vertices
        i = 0
        # print(len(all_paths))

        while i < len(all_paths):
            # for v in all_paths[i]:
            #     print(v, end=' ')
            # print()
            if self.is_path_secure(all_paths[i]) == False:
                all_paths.pop(i)
                continue
            i+=1

        # print(len(all_paths))
        
        if len(all_paths) == 0:
            set_edges = self.get_edges_from_graph()
            semi_trusted_edges = self.semitrusted_edges_from_set_edges(set_edges)
            # for edge in semi_trusted_edges:
                # print(f"{edge[0]} {edge[1]}")
            semi_trusted_edges = list(dict.fromkeys(semi_trusted_edges))
            return semi_trusted_edges


        # for path in all_paths:
        #     for vertex in path:
        #         print(vertex, end=' ')
        #     print()
        edge_paths = []
        for path in all_paths:
            edge_path = self.get_edges_from_path(path)
            # for edge in edge_path:
            #     print(f"{type(edge)} {edge[0]} {edge[1]}")
            if set(edge_path) not in edge_paths:
                edge_paths.append(edge_path)

        edge_freq = {}
        for edge_path in edge_paths:
            for edge in edge_path:
                edge_freq[edge] = edge_freq.get(edge, 0) + 1

        critical_edges = []

        for edge, freq in edge_freq.items():
            if freq == len(all_paths) and self.check_path_security(list(edge)) == 1:
                critical_edges.append(edge)
        
        return critical_edges
                

    def get_edges_from_path(self, path: 'list[Vertex]') -> 'list[(Vertex, Vertex)]':
        """
        Returns the list of edges in the path.
        :param path: The path to check.
        :return: A list of edges in the path.
        """
        edges = []
        for i in range(len(path) - 1):
            edges.append((path[i], path[i + 1]))

        return edges
    
if __name__ == "__main__":

    G = Graph()

    a = Vertex(True)
    b = Vertex(False)
    c = Vertex(True)
    d = Vertex(False)
    e = Vertex(False)
    f = Vertex(False)
    g = Vertex(True)
    h = Vertex(True)
    i = Vertex(True)
    j = Vertex(True)
    k = Vertex(True)
    l = Vertex(False)
    m = Vertex(True)
    n = Vertex(False)
    o = Vertex(True)
    p = Vertex(False)
    q = Vertex(True)
    r = Vertex(False)
    s = Vertex(True)
    t = Vertex(False)
    u = Vertex(True)
    v = Vertex(False)
    w = Vertex(True)
    x = Vertex(False)
    y = Vertex(True)
    z = Vertex(False)

    G.add_vertex(a)
    G.add_vertex(b)
    G.add_vertex(c)
    G.add_vertex(d)
    G.add_vertex(e)
    G.add_vertex(f)
    G.add_vertex(g)
    G.add_vertex(h)
    G.add_vertex(i)
    G.add_vertex(j)
    G.add_vertex(k)
    G.add_vertex(l)
    G.add_vertex(m)
    G.add_vertex(n)
    G.add_vertex(o)
    G.add_vertex(p)
    G.add_vertex(q)
    G.add_vertex(r)
    G.add_vertex(s)
    G.add_vertex(t)
    G.add_vertex(u)
    G.add_vertex(v)
    G.add_vertex(w)
    G.add_vertex(x)
    G.add_vertex(y)
    G.add_vertex(z)

    G.add_edge(a, b)
    G.add_edge(a, c)
    G.add_edge(b, c)
    G.add_edge(b, d)
    G.add_edge(b, h)
    G.add_edge(c, d)
    G.add_edge(e, f)
    G.add_edge(e, h)
    G.add_edge(e, k)
    G.add_edge(f, g)
    G.add_edge(f, i)
    G.add_edge(f, l)
    G.add_edge(g, n)
    G.add_edge(i, l)
    G.add_edge(j, l)
    G.add_edge(j, m)
    G.add_edge(j, o)
    G.add_edge(k, l)




    all = G.check_security(a, c)
    print(len(all))
#     for edge in all:
#         print(f"{type(edge)}: {edge[0].name} {edge[1].name}")

