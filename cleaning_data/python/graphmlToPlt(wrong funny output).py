import networkx as nx
import matplotlib.pyplot as plt


G = nx.read_graphml('graph.graphml')
nx.draw(G)
plt.show()
