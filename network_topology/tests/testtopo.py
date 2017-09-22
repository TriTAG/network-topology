import unittest
from network_topology import getNetworkTopology
from shapely.geometry import LineString

class FullTestCase(unittest.TestCase):

    def test_X(self):
        ntX = getNetworkTopology(self.X, turnThreshold=90)
        self.assertEqual(len(ntX), 5, 'incorrect number of nodes')
        self.assertEqual(len(ntX.edges()), 8, 'incorrect number of edges')

    def test_T(self):
        ntT = getNetworkTopology(self.T, turnThreshold=90)
        self.assertEqual(len(ntT), 4, 'incorrect number of nodes')
        self.assertEqual(len(ntT.edges()), 6, 'incorrect number of edges')

    def test_I(self):
        ntI = getNetworkTopology(self.I, turnThreshold=90)
        self.assertEqual(len(ntI), 2, 'incorrect number of nodes')
        self.assertEqual(len(ntI.edges()), 2, 'incorrect number of edges')

    def test_P(self):
        ntP = getNetworkTopology(self.P, turnThreshold=30, thickness=10, minInnerPerimeter=1)
        self.assertEqual(len(ntP), 4, 'incorrect number of nodes')
        self.assertEqual(len(ntP.edges()), 8, 'incorrect number of edges')

    def setUp(self):
        self.P = [LineString([[0, 0], [0, 100]]),
                  LineString([[0, 50], [25, 75], [0, 100]])]
        self.I = [LineString([[0, 0], [100, 100]]),
                  LineString([[20, 20], [70, 70]])]
        self.X = [LineString([[0, 0], [100, 100]]),
                  LineString([[100, 0], [0, 100]])]
        self.T = [LineString([[0, 0], [100, 100]]),
                  LineString([[100, 0], [60, 50], [100, 100]])]

if __name__ == '__main__':
    unittest.main()
