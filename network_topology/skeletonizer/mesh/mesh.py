"""Class to store and manipulate a mesh."""

from ..discrete.abstractgeom import AbsDiscreteGeometry
from ...geometry.geomath import GeometryProcessor
from ...geometry.point import Point
import networkx as nx
import numpy as np
import math
from rtree import index
from collections import defaultdict
from itertools import count, combinations
from shapely.geometry import Polygon, LineString
from .edgeiterator import EdgeIterator


class Mesh(AbsDiscreteGeometry):
    """Class to store and manipulate a mesh."""

    def __init__(self, vertices, edge_nodes, graph):
        """Initialize mesh object.

        Parameters
        ----------
        vertices : sequence
            A sequence of coordinate sequences
        edge_nodes:
            A sequence of:
                1 if coordinate is on an outer edge
                0 otherwise
        graph:
            A graph represending topological connections between points
        tolerance:

        """
        self._vertices = np.array(vertices)
        self._graph = graph
        self._count = count(len(graph))
        self._edge_nodes = np.array(edge_nodes)

    def polygons(self):
        """Return an iterator of polygon vertex lists."""
        for p in self._graph:
            yield self._graph.node[p]['vertices']

    def getVertex(self, nodeId):
        """Return coordinates of the given vertex."""
        return self._vertices[nodeId]

    def getShape(self, polyId):
        """Generate shapely object of the given polygon."""
        return Polygon([self._vertices[v]
                        for v in self._graph.node[polyId]['vertices']])

    def collapseShapes(self):
        """Merge polygons that are fully internal or have internal nodes."""
        polygons = self._findPolygonsToMerge()
        subgraph = self._graph.subgraph(polygons)
        for cluster in list(nx.connected_components(subgraph)):
            self._mergeCluster(cluster)

    def _findPolygonsToMerge(self):
        """Return indexes of all polygons that share all their edges."""
        internal = []
        for poly, data in self._graph.nodes(data=True):
            if (len(self._graph[poly]) == len(data['vertices']) or
                    any(map(self._isInternal, data['vertices']))):
                internal.append(poly)
        return internal

    def _isInternal(self, nodeId):
        """Return true if the given vertex index is internal to the shape."""
        return not self._edge_nodes[nodeId]

    def _mergeCluster(self, polyIds):
        """Combine adjacent polygons into a single one.

        Parameters
        ----------
        polyIds : sequence
            A sequence of index values of adjacent polygons
        """
        polyIds = list(polyIds)
        base = polyIds[0]
        edges = defaultdict(list)

        for poly in polyIds:
            for neighbour, data in self._graph[poly].items():
                if neighbour not in polyIds:
                    self._graph.add_edge(base, neighbour, **data)
            nodes = self._graph.node[poly]['vertices']
            for edge in EdgeIterator(nodes):
                edges[edge].append(poly)
            if poly != base:
                self._graph.remove_node(poly)
        neighbours = defaultdict(list)
        for (n1, n2), polys in edges.items():
            if len(polys) == 1:
                neighbours[n1].append(n2)
                neighbours[n2].append(n1)
        current = next(iter(neighbours.keys()))
        nodes = [current]
        while neighbours[current]:
            for neighbour in neighbours[current]:
                neighbours[current].remove(neighbour)
                if neighbour not in nodes:
                    nodes.append(neighbour)
                    current = neighbour
        self._graph.nodes[base]['vertices'] = nodes

    def splitShapes(self, cutoffRatio=2):
        """Divide any shape that has an aspect ratio above the cutoff."""
        geometryProcessor = GeometryProcessor()
        stack = list(self._graph.nodes(data=True))
        while stack:
            poly, data = stack.pop()
            if len(data['vertices']) > 3:
                shape = self.getShape(poly)
                (px, py), ratio = geometryProcessor.principalAxis(shape)
                if ratio > cutoffRatio:
                    top, bottom = self._findSplitNodes(poly, px, py,
                                                       geometryProcessor)
                    newPoly = self._splitPoly(poly, top, bottom)
                    if newPoly is not None:
                        stack.append((poly, data))
                        stack.append((newPoly, self._graph.node[newPoly]))

    def _splitPoly(self, polyId, top, bottom):
        """Divide a shape along the principal axis."""
        nodes = self._graph.nodes[polyId]['vertices']
        loop = {a: b for (a, b) in EdgeIterator(nodes, sort=False)}
        firstHalf = self._getHalf(top, bottom, loop)
        secondHalf = self._getHalf(bottom, top, loop)
        if len(firstHalf) > 3 and len(secondHalf) > 3:
            secondPoly = next(self._count)
            n1, n2 = sorted((top, bottom))
            self._graph.add_edge(polyId, secondPoly, common=(n1, n2))
            self._graph.node[polyId]['vertices'] = firstHalf
            self._graph.node[secondPoly]['vertices'] = secondHalf
            for neighbour, data in dict(self._graph[polyId]).items():
                n1, n2 = data['common']
                if n1 not in firstHalf or n2 not in firstHalf:
                    self._graph.add_edge(secondPoly, neighbour, **data)
                    self._graph.remove_edge(polyId, neighbour)
            return secondPoly

    def _findSplitNodes(self, polyId, px, py, geometryProcessor):
        """Determine which pair of nodes to split the polygon with."""
        shape = self.getShape(polyId)
        nearestTop, lowestTop = None, 1
        nearestBottom, lowestBottom = None, 1
        for v in self._graph.nodes[polyId]['vertices']:
            dx, dy = self.getVertex(v)
            dx -= shape.centroid.x
            dy -= shape.centroid.y
            dx, dy = geometryProcessor.normalize(dx, dy)
            dotProd = dx*px + dy*py
            crossProd = dx*py - dy*px
            if crossProd > 0:
                if abs(dotProd) < lowestTop:
                    lowestTop = abs(dotProd)
                    nearestTop = v
            elif abs(dotProd) < lowestBottom:
                lowestBottom = abs(dotProd)
                nearestBottom = v
        return nearestTop, nearestBottom

    def _getHalf(self, startNode, endNode, loop):
        half = [startNode]
        current = startNode
        while current != endNode:
            current = loop[current]
            half.append(current)
        return half

    def skeletonize(self, splitAtEndpoints, topology):
        """Generate a SkeletonGraph of the geometry."""
        # find the midpoints
        self._calculateMidPoints()

        # calculate projections between midpoints
        self._calculateProjections()

        # recalculate polygon centroids based on projections from neighbours
        self._calculateCentroids()

        # create new graph with collapsed edges in both directions
        self._constructSkeleton(topology)

    def _calculateMidPoints(self):
        for p1, p2, data in self._graph.edges(data=True):
            nodes = list(data['common'])
            centroid = sum(self._vertices[nodes]) * 0.5
            data['point'] = Point(*centroid)

    def _calculateProjections(self):
        for p, data in self._graph.nodes(data=True):
            data['projections'] = []
        for p in self._graph.nodes:
            for nbr1, nbr2 in combinations(self._graph[p], 2):
                p1 = self._graph[p][nbr1]['point']
                p2 = self._graph[p][nbr2]['point']
                vector = p1 - p2
                normal = vector / abs(vector)
                self._graph.node[nbr1]['projections'].append((p, normal))
                self._graph.node[nbr2]['projections'].append((p, normal))

    def _calculateCentroids(self):
        for p, data in self._graph.nodes(data=True):
            shape = self.getShape(p)
            length = math.sqrt(shape.area)
            for nbr, normal in data['projections']:
                pt = self._graph[p][nbr]['point']
                p1 = pt + 10. * length * normal
                p2 = pt - 10. * length * normal
                line = LineString([p1, p2]).buffer(length/8.)
                shape = shape.intersection(line)
            if shape.area == 0:
                shape = self.getShape(p)
            self._graph.node[p]['point'] = Point(shape.centroid.x,
                                                 shape.centroid.y)

    def _constructSkeleton(self, topology):
        # self._diagnosticPlot()
        visited = set()
        for node in self._graph:
            if len(self._graph[node]) in (1, 2) and node not in visited:
                subEdge = self._getEdge(node)
                edge = [self._graph.nodes[subEdge[0]]['point']]
                visited.add(subEdge[0])
                for n1, n2 in zip(subEdge[:-1], subEdge[1:]):
                    edge.append(self._graph[n1][n2]['point'])
                    edge.append(self._graph.nodes[n2]['point'])
                    visited.add(n1)
                    visited.add(n2)
                topology.addEdge(edge)

    def _getEdge(self, node):
        stack = [node]
        visited = {node}
        startNode = None
        while stack and startNode is None:
            node = stack.pop()
            for child in self._graph[node]:
                if child not in visited:
                    visited.add(child)
                    if len(self._graph[child]) == 2:
                        stack.append(child)
                    else:
                        startNode = child
                        break
        nodes = [startNode, node]
        visited = set(nodes)
        while len(self._graph[nodes[-1]]) == 2:
            for child in self._graph[nodes[-1]]:
                if child != nodes[-2]:
                    visited.add(child)
                    nodes.append(child)
                    break
        return list(reversed(nodes))

    def _makeIndex(self):
        pointsIdx = index.Index()
        for i, v in enumerate(self._vertices):
            pointsIdx.insert(i, list(v)*2)
        return pointsIdx

    def _diagnosticPlot(self):
        from matplotlib.patches import Polygon
        from matplotlib.collections import PatchCollection
        import matplotlib.pyplot as plt
        patches = []
        labels = []
        fig, ax = plt.subplots()
        for node in self._graph:
            shape = self.getShape(node)
            labels.append((node, shape.centroid))
            polygon = Polygon(shape.exterior.coords[:], True)
            patches.append(polygon)

        p = PatchCollection(patches, alpha=0.4)
        p.set_edgecolor('black')

        ax.add_collection(p)
        for node, centroid in labels:
            ax.text(centroid.x, centroid.y, str(node),
                    horizontalalignment="center")
        ax.autoscale()

        plt.show()
