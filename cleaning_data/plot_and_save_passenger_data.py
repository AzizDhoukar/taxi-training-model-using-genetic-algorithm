import matplotlib.pyplot as plt
import pandas as pd


# Load the CSV file into a Pandas dataframe
df = pd.read_csv('mex_clean.csv', usecols = ['id','pickup_datetime','dropoff_datetime',
                                             'pickup_longitude','pickup_latitude','dropoff_longitude',
                                             'dropoff_latitude','trip_duration'])

# Remove irrelevant columns
#df.drop(['vendor_id', 'dist_meters', 'wait_sec', 'store_and_fwd_flag'], axis=1, inplace=True)

# Remove rows with missing or invalid values
df.dropna(inplace=True)

# Remove rows with trip_duration more than 1500
df = df[df['trip_duration'] <= 1500]

# Convert pickup and dropoff datetime columns to datetime type
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])

# Drop rows where pickup date is not the same as dropoff date
df = df[df['pickup_datetime'].dt.date == df['dropoff_datetime'].dt.date]

# Drop rows where pickup or dropoff location latitude is outside the range of 19.1 to 19.7
df = df[(df['pickup_latitude'] >= 19.1) & (df['pickup_latitude'] <= 19.7) &
        (df['dropoff_latitude'] >= 19.1) & (df['dropoff_latitude'] <= 19.7)]

df.to_csv('clean_data.csv', index=False)

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

