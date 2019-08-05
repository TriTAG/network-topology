"""Support iterating over the edges of a polygon."""


class EdgeIterator(object):
    """Iterate over the edges of a polygon given a list of nodes."""

    def __init__(self, nodes, sort=True):
        """Constructor."""
        self._nodes = list(nodes)
        self._sort = sort

    def __iter__(self):
        """Iterate over the nodes of the polygon."""
        for n1, n2 in zip(self._nodes,
                          self._nodes[1:] + self._nodes[:1]):
            if self._sort:
                n1, n2 = sorted([n1, n2])
            yield n1, n2
