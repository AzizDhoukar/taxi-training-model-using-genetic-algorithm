import xml.etree.ElementTree as ET
import csv

# Parse the GraphML data
tree = ET.parse('..\graph.graphml')
root = tree.getroot()

# Extract node and edge data
nodes = {}
edges = {}
for node in root.findall('.//{http://graphml.graphdrawing.org/xmlns}node'):
    node_id = node.get('id')
    lat = node.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d4"]')
    lon = node.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d5"]')
    if lat is not None and lon is not None:
        nodes[node_id] = {
            'latitude': lat.text,
            'longitude': lon.text,
            'connected_nodes': [],
            'travel_times': []
    }

for edge in root.findall('.//{http://graphml.graphdrawing.org/xmlns}edge'):
    source = edge.get('source')
    target = edge.get('target')
    travel_time = float(edge.find('.//{http://graphml.graphdrawing.org/xmlns}data[@key="d20"]').text)
    if source in edges:
        edges[source].append(target)
    else:
        edges[source] = [target]
    nodes[source]['connected_nodes'].append(target)
    nodes[source]['travel_times'].append(travel_time)
    nodes[target]['connected_nodes'].append(source)
    nodes[target]['travel_times'].append(travel_time)

# Write node data to CSV file
with open('nodes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['node_id', 'longitude', 'latitude', 'connected_nodes', 'travel_times'])
    for node_id, data in nodes.items():
        writer.writerow([node_id, data['longitude'], data['latitude'] ,data['connected_nodes'], data['travel_times']])

# Write edge data to CSV file
with open('edges.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['startnode', 'endnode'])
    for startnode, endnodes in edges.items():
        for endnode in endnodes:
            writer.writerow([startnode, endnode])