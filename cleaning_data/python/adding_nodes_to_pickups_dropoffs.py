import pandas as pd
import numpy as np
from math import radians, cos, sin, sqrt, atan2

# Load the clean data file
clean_data = pd.read_csv("../clean_data.csv")

# Load the nodes file
nodes = pd.read_csv("../csv/nodes.csv")

# Define a function to calculate the Haversine distance between two sets of coordinates
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    '''
    # Haversine formula
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r
    '''
    return (lon1 - lon2)**2 + (lat1 - lat2)**2

# Define a function to find the ID of the closest node to a set of coordinates
def find_closest_node(lat, lon):
    distances = []
    min_distance = haversine(nodes.iloc[1][1], nodes.iloc[1][2], lon, lat)
    for i, row in nodes.iterrows():
        distance = haversine(row['longitude'], row['latitude'], lon, lat)
        if distance < min_distance:
            min_distance = distance
            closest_node = row['node_id']
            distances.append([closest_node, distance])
    print(distances)
    return closest_node

# Add a column to the clean data file with the ID of the closest node to each pickup location
clean_data['pickup_node_id'] = clean_data.apply(lambda row: find_closest_node(row['pickup_latitude'], row['pickup_longitude']), axis=1)

# Add a column to the clean data file with the ID of the closest node to each dropoff location
clean_data['dropoff_node_id'] = clean_data.apply(lambda row: find_closest_node(row['dropoff_latitude'], row['dropoff_longitude']), axis=1)

# Save the updated clean data file
clean_data.to_csv("clean_data_with_nodes.csv", index=False)