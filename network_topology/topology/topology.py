"""Implementation for topology."""

from .abstract import AbstractTopology
import networkx as nx
from rtree import index
from itertools import count
from shapely.geometry import LineString, Point
from heapq import heappop, heappush


class Topology(AbstractTopology):
    """Class to implement topology."""

    def __init__(self,
                 graph=None,
                 spatialIndex=None,
                 nodes=None,
                 coordinates=None):
        """Contstructor for topology."""
        self._graph = graph or nx.MultiDiGraph()
        self._index = spatialIndex or index.Index()
        self._nodes = nodes or []
        self._coordinates = coordinates or {}

    def addEdge(self, points):
        """Add an edge to the topology."""
        endpoints = self._getNodes(points)
        for order in [1, -1]:
            self._addOneEdge(endpoints[::order],
                             LineString(points[::order]))

    def _addOneEdge(self, nodes, lineString):
        u, v = nodes
        i = self._graph.add_edge(u, v, geom=lineString)
        self._index.insert(hash((u, v, i)), lineString.bounds, obj=(u, v, i))

    def _getNodes(self, points):
        return [self._getNodeIndex(points[i]) for i in [0, -1]]

    def _getNodeIndex(self, point):
        point = tuple(point)
        try:
            return self._coordinates[point]
        except KeyError:
            nodeID = len(self._nodes)
            self._coordinates[point] = nodeID
            self._nodes.append(Point(point))
            return nodeID

    def getEdge(self, start, finish, index):
        """Get the geometry for an edge."""
        return self._graph[start][finish][index]['geom']

    def shortestPath(self, source, target):
        """Find path from source to target nodes.

        Adapted for MultiDiGraph from astar_path in networkx, BSD licence.
        https://github.com/networkx/networkx/blob/master/networkx/algorithms/shortest_paths/astar.py
        """
        targetCoord = self._nodes[target]
        push = heappush
        pop = heappop

        # The queue stores priority, node, cost to reach, and parent.
        # Uses Python heapq to keep in priority order.
        # Add a counter to the queue to prevent the underlying heap from
        # attempting to compare the nodes themselves. The hash breaks ties in
        # the priority and is guarenteed unique for all nodes in the graph.
        c = count()
        queue = [(0, next(c), source, 0, None, None)]

        # Maps enqueued nodes to distance of discovered paths and the
        # computed heuristics to target. We avoid computing the heuristics
        # more than once and inserting the node into the queue too many times.
        enqueued = {}
        # Maps explored nodes to parent closest to the source.
        explored = {}

        while queue:
            # Pop the smallest item from queue.
            _, __, curnode, dist, parent, via = pop(queue)

            if curnode == target:
                path = []
                distances = []
                node = curnode
                edge = via
                while parent is not None:
                    path.append((parent, node, edge))
                    distances.append(
                        self._graph[parent][node][edge]['geom'].length)
                    node = parent
                    parent, edge = explored[node]
                path.reverse()
                distances.reverse()
                return path, distances

            if curnode in explored:
                continue

            explored[curnode] = parent, via

            for neighbor, es in self._graph[curnode].items():
                for edge, w in es.items():
                    if neighbor in explored:
                        continue
                    ncost = dist + w['geom'].length
                    if neighbor in enqueued:
                        qcost, h = enqueued[neighbor]
                        # if qcost < ncost, a longer path to neighbor remains
                        # enqueued. Removing it would need to filter the whole
                        # queue, it's better just to leave it there and ignore
                        # it when we visit the node a second time.
                        if qcost <= ncost:
                            continue
                    else:
                        h = targetCoord.distance(self._nodes[neighbor])
                    enqueued[neighbor] = ncost, h
                    push(queue,
                         (ncost + h, next(c), neighbor, ncost, curnode, edge))

        return [], [float('inf')]

    def getNearbyEdges(self, point, tolerance):
        """Find candidate edges near the point."""
        scope = tolerance * 2.0
        # candidates = set()
        for item in self._index.intersection(
            (point.x - scope, point.y - scope, point.x + scope,
             point.y + scope),
                objects=True):
            # We check if the segment is already in the candidate list,
            # allowing the spatial index to contain discretized parts of each
            # segment.
            if (  # item.object not in candidates and
                    point.distance(self.getEdge(*item.object)) < scope):
                # candidates.add(item.object)
                yield item.object
