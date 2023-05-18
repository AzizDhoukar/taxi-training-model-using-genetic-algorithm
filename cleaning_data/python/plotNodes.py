import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math

# read edge and node data from csv files
edges_df = pd.read_csv('../csv/edges.csv')
nodes_df = pd.read_csv('../csv/nodes.csv')

# create an empty graph
G = nx.Graph()

# add nodes to the graph
for _, row in nodes_df.iterrows():
    G.add_node(row['node_id'], pos=(row['longitude'], row['latitude']))

# add edges to the graph
for _, row in edges_df.iterrows():
    G.add_edge(row['startnode'], row['endnode'])

# get node positions
node_pos = nx.get_node_attributes(G, 'pos')

nan_nodes = []
for node in G.nodes():
    if math.isnan(node):
        nan_nodes.append(node)
G.remove_nodes_from(nan_nodes)

#print(G.nodes())
#print(G.edges)
#for node in node_pos:
#    print(node)
# draw the graph

fig, ax = plt.subplots(figsize=(10,10))
nx.draw(G, pos=node_pos, node_size=10, node_color='blue', alpha=0.5, ax=ax)
plt.show()
