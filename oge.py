#I watched video on you-tube on how to plot coordinates on a map using geopandas python by Code and Crust
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Read the dataset (Growlocations.csv) into a dataframe
data = pd.read_csv('Growlocations.csv')

# Create a new DataFrame without duplicates
df_non_duplicates = data.drop_duplicates(subset=['Serial'])

non_valued = (
    (df_non_duplicates['Latitude'] < -10.592) | (df_non_duplicates['Latitude'] > 1.6848) |
    (df_non_duplicates['Longitude'] < 50.681) | (df_non_duplicates['Longitude'] > 57.985)
)
uncleaned_data = df_non_duplicates[non_valued]

# Remove rows with outrageous values
ready_data = df_non_duplicates[~non_valued]

# Extract latitude and longitude columns from the dataframe
latitude = ready_data['Latitude']
longitude = ready_data['Longitude']



# Create a GeoDataFrame from the dataframe with coordinates
geometry = [Point(xy) for xy in zip(ready_data['Latitude'], ready_data['Longitude'])]
gdf = gpd.GeoDataFrame(ready_data, geometry=geometry, crs='EPSG:4326')

# Load the UK map from OpenStreetMap using geopandas
uk_map = plt.imread('map7.png')

# Plotting the UK map
fig, ax = plt.subplots(figsize=(10, 10))
#uk_map.plot(ax=ax, alpha=0.9, color='purple')
ax.imshow(uk_map, extent=[-10.592, 1.6848, 50.681, 57.985])

# Plotting the sensor locations on the map
gdf.plot(ax=ax, marker='o', color='purple', markersize=30, label='Sensor Locations')

# Set plot title and labels
plt.title('Sensor Locations on United Kingdom Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()

# Show the plot
plt.show()
# Save information about uncleaned values to a CSV file
uncleaned_data.to_csv('non_valued.csv', index=False)

# Save ready data to a CSV file
ready_data.to_csv('ready_data.csv', index=False)

# Read contents ready data
ready_data = pd.read_csv('ready_data.csv')

# Create filtered_data with swapped Latitude and Longitude columns
filtered_data = ready_data.copy()
filtered_data['Longitude'], filtered_data['Latitude'] = ready_data['Latitude'], ready_data['Longitude']

# Write filtered_data to a CSV file
filtered_data.to_csv('filtered_data.csv',index=False)