import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


df = pd.read_csv('clean_data_with_nodes.csv')
# Filter rows by pickup_node_id or dropoff_node_id
pickup_df = df[df.pickup_node_id == 268487335]
dropoff_df = df[df.dropoff_node_id == 268487335]

# Extract coordinates
pickup_coords = pickup_df[['pickup_longitude', 'pickup_latitude']].values
dropoff_coords = dropoff_df[['dropoff_longitude', 'dropoff_latitude']].values

# Plot coordinates on map
fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(pickup_coords[:, 0], pickup_coords[:, 1], c='blue', label='Pickup')
ax.scatter(dropoff_coords[:, 0], dropoff_coords[:, 1], c='red', label='Dropoff')
ax.legend()
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Pickup and Dropoff Locations')
plt.show()
"""
the location are scattered away from one another. so no problem with the coordinates
"""