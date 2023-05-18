import json
import pandas as pd

with open('graph.json', 'r') as f:
    data = json.load(f)

nodes = []
for element in data['elements']:
    if element['type'] == 'node':
        node_id = element['id']
        node_lat = element['lat']
        node_lon = element['lon']
        nodes.append({'id': node_id, 'lat': node_lat, 'lon': node_lon})
nodes_df = pd.DataFrame(nodes)

edges = []
for element in data["elements"]:
    if element["type"] == "way":
        nodes_in_way = element["nodes"]
        for i in range(len(nodes_in_way) - 1):
            edge_id = str(element['id']) + str(i)
            edge_start_node = nodes_in_way[i]
            edge_end_node = nodes_in_way[i+1]
            edges.append({'id': edge_id, 'start_node': edge_start_node, 'end_node': edge_end_node})

edges_df = pd.DataFrame(edges)

nodes_df.to_csv('nodes.csv', index=False)
edges_df.to_csv('edges.csv', index=False)
