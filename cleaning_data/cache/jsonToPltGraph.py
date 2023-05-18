import json
import matplotlib.pyplot as plt

# Load the JSON data from file
with open('graph.json', 'r') as f:
    data = json.load(f)

# Extract nodes and edges
nodes = {node["id"]: (node["lat"], node["lon"]) for node in data["elements"] if node["type"] == "node"}

edges = []
for element in data["elements"]:
    if element["type"] == "way":
        nodes_in_way = element["nodes"]
        for i in range(len(nodes_in_way) - 1):
            edge = (nodes_in_way[i], nodes_in_way[i+1])
            edges.append(edge)

# Plot the graph using Matplotlib
fig, ax = plt.subplots()
for edge in edges:
    node1 = nodes[edge[0]]
    node2 = nodes[edge[1]]
    ax.plot([node1[1], node2[1]], [node1[0], node2[0]], color="blue")
for node_id, (lat, lon) in nodes.items():
    ax.plot(lon, lat, "ro")
plt.show()