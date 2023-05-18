import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from math import isnan

# create an empty graph
G = nx.Graph()

# read edge and node data from csv files
edges_df = pd.read_csv('edges.csv')
nodes_df = pd.read_csv('nodes.csv')

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
    if isnan(node):
        nan_nodes.append(node)
G.remove_nodes_from(nan_nodes)

fig, ax = plt.subplots(figsize=(10,10))
nx.draw(G, pos=node_pos, node_size=10, node_color='blue', alpha=0.5, ax=ax)

# Load the CSV file into a Pandas dataframe
df = pd.read_csv('clean_data.csv')

# Remove rows with missing or invalid values
df.dropna(inplace=True)

# Drop rows where pickup or dropoff location latitude is outside the range of 19.1 to 19.7
df = df[(df['pickup_latitude'] >= 19.41) & (df['pickup_latitude'] <= 19.44) &
        (df['dropoff_latitude'] >= 19.41) & (df['dropoff_latitude'] <= 19.44)]

df = df[(df['pickup_longitude'] >= -99.148) & (df['pickup_longitude'] <= -99.133) &
        (df['dropoff_longitude'] >= -99.148) & (df['dropoff_longitude'] <= -99.133)]

df.to_csv('test_clean_data.csv', index=False)

# Create a scatter plot of pickup and dropoff locations
plt.scatter(df['pickup_longitude'], df['pickup_latitude'], s=5, label='Pickup')
plt.scatter(df['dropoff_longitude'], df['dropoff_latitude'], s=5, c='red', label='Dropoff')
plt.legend()

# Set the plot title and axis labels
plt.title('Pickup and Dropoff Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the plot
plt.show()

