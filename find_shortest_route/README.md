# Find the road
This project will provide the user information about roads in California and Nevada.

The data available are dictionaries organized as such:
- *Distance graph*: file containing physical distances between each pair of nodes. Each line follows this structure: (Id_Node1, Id_Node2, d(Id_Node1,Id_Node2)), where d(x,y) is the physical distance between x and y.
- *Travel time graph*: file containing time distances between each pair of nodes. Each line follows this structure: (Node1, Node2, t(Id_Node1, Id_Node2)), where t(x,y) is the time distance between x and y.
- *Node information file*: file containing node coordinates. Each line follows this structure: (Id_Node, Latitude, Longitude)

Using the information provided I'll build two main functionalities:
- *Shortest ordered route*: given an input of a starting node, an arbitrary number of other nodes and a distance type (time, space, graph distance) the algorithm will provide the shortest ordered route and plot it on a map.
- *Shortest route*: given an input of a starting node, an arbitrary number of other nodes and a distance type (time, space, graph distance) the algorithm will provide the shortest route necessary to visit all nodes and plot it on a map.
