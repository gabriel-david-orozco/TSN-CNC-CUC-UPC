def sssp_dijkstra(self, source):

    total_vertex = len(self.vertex)
    Q = np.array(self.vertex)

    dist = np.zeros(total_vertex)
    dist.fill(np.inf)

    dist[self.vertex == source] = 0

    while len(Q) != 0:

        min = np.inf
        u = 0
        for q in Q:
            if dist[self.vertex == q] <= min:
                min = dist[self.vertex == q]
                u = q

        Q = np.delete(Q, np.argwhere(Q == u))

        for v in self.target[self.source == u]:
            alt = dist[self.vertex == u] + self.get_weight(u, v)
            index_v = self.vertex == v
            if alt < dist[index_v]:
                dist[index_v] = alt

def apsp_dijkstra(self):

    result = np.full((self.vertex.size, self.vertex.size), np.inf)
    count = 0
    for v in self.vertex:
        result[count] = self.sssp_dijkstra(v)
        count = count + 1

    return result

from _graph.GraphPro import GraphPro as g
from time import time
import os

os.system('clear')
print("<--------Test Dijkstra------->\n")

weights = [1, 2, 3, 4, 5]
graph = g.creategraph(6, .75, weights, directed=False)
graph.print_r()
print('.........................')
t = time()
print(graph.apsp_dijkstra())
elapsed = time() - t
print("Time: ", elapsed)

graph.draw()
