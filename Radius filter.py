import pandas as pd
import numpy as np
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the Earth's surface
    using the Haversine formula.
    """
    # Convert coordinates to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c  # Earth's radius in kilometers
    #print(distance)

    return distance

def filter_points_within_radius(center_lat, center_lon, points, radius_km):
    """
    Filter points within a specified radius from a given center coordinate.
    """
    filtered_points = []
    filtered_node = []
    i = 0
    for point in points:
        point_lat, point_lon = point
        distance = haversine_distance(center_lat, center_lon, point_lat, point_lon)
        if distance <= radius_km:
            filtered_points.append(point)
            filtered_node.append(i)
        i += 1
    
    return filtered_points, filtered_node

df = pd.read_csv("SiouxFalls_node.tntp", sep='\t')
points = list(zip(df['Y'].values, df['X'].values))

radius_km = 25  # Radius in kilometers
my_list = []
for _,latlong in df.iterrows():
    filtered_points, filtered_node = filter_points_within_radius(latlong[2], latlong[1], points, radius_km)
    print(latlong[2], latlong[1], _+1, filtered_points)
    my_tuple = filtered_node
    my_list.append(my_tuple)

df1 = pd.DataFrame(my_list)
#df1.columns = [ "Node number"]

df1.to_csv("filtered_nodes.csv", index=False)