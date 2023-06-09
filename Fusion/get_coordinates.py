import math
import matplotlib.pyplot as plt

def calculate_transmitter_coordinates(receiver_latitude, receiver_longitude, distances, azimuths):
    earth_radius = 6371  # Mean radius of the Earth in kilometers
    
    receiver_latitude_rad = math.radians(receiver_latitude)
    receiver_longitude_rad = math.radians(receiver_longitude)
    
    transmitter_coordinates = []
    
    for i in range(len(distances)):
        distance = distances[i]
        azimuth = azimuths[i]
        
        azimuth_rad = math.radians(azimuth)
        
        transmitter_latitude_rad = math.asin(math.sin(receiver_latitude_rad) * math.cos(distance / earth_radius) + math.cos(receiver_latitude_rad) * math.sin(distance / earth_radius) * math.cos(azimuth_rad))
        
        transmitter_longitude_rad = receiver_longitude_rad + math.atan2(math.sin(azimuth_rad) * math.sin(distance / earth_radius) * math.cos(receiver_latitude_rad), math.cos(distance / earth_radius) - math.sin(receiver_latitude_rad) * math.sin(transmitter_latitude_rad))
        
        transmitter_latitude = math.degrees(transmitter_latitude_rad)
        transmitter_longitude = math.degrees(transmitter_longitude_rad)
        
        transmitter_coordinates.append((transmitter_latitude, transmitter_longitude))
    
    return transmitter_coordinates

def plot_coordinates(receiver_coordinates, transmitter_coordinates, distances, azimuths):
    latitudes = [receiver_coordinates[0]]
    longitudes = [receiver_coordinates[1]]
    
    for coordinate in transmitter_coordinates:
        latitudes.append(coordinate[0])
        longitudes.append(coordinate[1])
    
    plt.figure(figsize=(8, 6))
    plt.scatter(longitudes, latitudes, color='red', marker='o', label='Tx')
    plt.scatter(receiver_coordinates[1], receiver_coordinates[0], color='blue', label='Rx')
    
    for i in range(len(transmitter_coordinates)):
        transmitter = transmitter_coordinates[i]
        distance = distances[i]
        azimuth = azimuths[i]
        
        plt.plot([receiver_coordinates[1], transmitter[1]], [receiver_coordinates[0], transmitter[0]], color='gray', linestyle='dotted')
        midpoint_x = (receiver_coordinates[1] + transmitter[1]) / 2
        midpoint_y = (receiver_coordinates[0] + transmitter[0]) / 2
        plt.annotate(f"Distance: {distance} km\nAzimuth: {azimuth}°", xy=(midpoint_x, midpoint_y), xytext=(10, 10), textcoords='offset points', ha='left', va='bottom')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Tx and Rx Ubication')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
receiver_latitude = 40.7128
receiver_longitude = -74.0060
distances = [100, 200, 300]  # Distances of the transmitters in kilometers
azimuths = [45, 90, 135]  # Azimuths of the transmitters in degrees

receiver_coordinates = (receiver_latitude, receiver_longitude)
transmitter_coordinates = calculate_transmitter_coordinates(receiver_latitude, receiver_longitude, distances, azimuths)

plot_coordinates(receiver_coordinates, transmitter_coordinates, distances, azimuths)
