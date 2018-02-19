# network-topology
Simplifies overlapping lines into a single graph

## Usage
```python
import network_topology
from shapely.geometry import LineString

linestrings = {'route 1': LineString([[...]], ...}

# Create a NetworkX MultiDiGraph from a list of linestrings
simplified_graph = network_topology.getNetworkTopology(linestrings.values(),
                                                       thickness=30.0,
                                                       minInnerPerimeter=100)
# Each edge of simplified_graph will have a 'geom' attribute, a LineString
# from the start node to the end node of that edge.

# Get a list of all the edges in simplified_graph that each linestring traverses
route_edges = network_topology.getMatchedRoutes(linestrings,
                                                simplified_graph)
# route_edges = {'route_1': [(0, 1, 0), (1, 2, 0), ...], ...}
```
