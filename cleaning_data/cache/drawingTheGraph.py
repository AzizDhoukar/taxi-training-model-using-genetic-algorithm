import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the nodes and edges into pandas dataframes
nodes_df = pd.read_csv('nodes.csv')
edges_df = pd.read_csv('edges.csv')

# Create an empty graph
G = nx.Graph()

# Add nodes to the graph
for _, node in nodes_df.iterrows():
    G.add_node(node['id'], pos=(node['lat'], node['lon']))

# Add edges to the graph
for _, edge in edges_df.iterrows():
    G.add_edge(edge['u'], edge['v'], weight=edge['weight'])

# Create a simple path from node 1 to node 10
path = nx.shortest_path(G, source=1, target=10)

# Plot the graph with the path highlighted
pos = nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)], edge_color='r', width=2)
nx.draw_networkx_labels(G, pos)

plt.show()