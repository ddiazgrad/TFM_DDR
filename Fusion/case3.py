import time
from object_track import create_track
from tracker import Tracker
import random
from scipy.spatial import KDTree


sensor_data = {
    "uav": {
        "location": {
            "x": 37.7749,
            "y": -122.4194,
            "altitude": 2000
        }
    },
    "adsb": {
        "module": "adsb",
        "identification": "ABC123",
        "location": {
            "x": 37.7749,
            "y": -122.4194,
            "altitude": 5000
        },
        "timestamp": 100323232
    },
    "array_rf": {
        "module": "array_rf",
        "identification": "ABC123",
        "location": {
            "x": 37.7749,
            "y": -122.4194,
            "altitude": 1000
        },
        "timestamp": 100323232,
    },
    "camera": {
        "module": "camera",
        "flight_type": "drone",
        "identification": "ABC123",
        "location": {
            "x": 37.7749,
            "y": -122.4194,
            "altitude": 3000
        },
        "timestamp": 100323232
    }
}

def process_camera(data, line, i):
    final_data = {
        "sensor": "camera",
        "identification": data["identification"],
        "location": {
            "x": line[2*i],
            "y": line[(2*i)+1],
            "altitude": data["location"]["altitude"]
        },
        "distance": None,
        "azimuth": None,
        "frequency": None,
        "flight_type": data["flight_type"],
        "timestamp": data["timestamp"],
        "speed": None
    }

    return final_data


def process_adsb(data, line, i):
    final_data = {
        "sensor": "ads-b",
        "identification": data["identification"],
        "location": {
            "x": line[2*i],
            "y": line[(2*i)+1],
            "altitude": data["location"]["altitude"]
        },
        "distance": None,
        "azimuth": None,
        "frequency": None,
        "flight_type": "heavyplane",
        "timestamp": data["timestamp"],
        "speed": None
    }

    return final_data

def process_array_rf(data, line, i):
    final_data = {
        "sensor": "rf_sensor",
        "identification": data["identification"],
        "location": {
            "x": line[2*i],
            "y": line[(2*i)+1],
            "altitude": data["location"]["altitude"]
        },
        "distance": None,
        "azimuth": None,
        "frequency": None,
        "flight_type": "heavyplane",
        "timestamp": data["timestamp"],
        "speed": None
    }

    return final_data

def process_uav(data, line, i):
    final_data = {
        "location": {
            "x": line[2*i],
            "y": line[(2*i)+1],
            "altitude": data["location"]["altitude"]
        }
    }
    
    return final_data

def generate_fake_data(sensor_data, sensor, lines, i, j):
    fake_data = sensor_data
    final_data = None

    timestamp = time.time()

    fake_data["timestamp"] = timestamp
    
    if sensor == "uav":
        final_data = process_uav(fake_data, lines[j], i)
    else:
        if sensor == "adsb" and (i < 50 or i > 58):
            final_data = process_adsb(fake_data, lines[j], i)
        elif sensor == "camera":
            final_data = process_camera(fake_data, lines[j], i)
        elif sensor == "array_rf":
            final_data = process_array_rf(fake_data, lines[j], i)
        
    return final_data

def create_sensors_data(lines):
    tracker = Tracker(50, 10)
    for i in range(150):
        print("Iteration:", i)
        coordinates = []
        faking = ["uav", "camera", "adsb", "array_rf"]
        for j, sensor in enumerate(faking):
            final_data = generate_fake_data(sensor_data[sensor], sensor, lines, i, j)
            if final_data is not None:
                coordinates.append(final_data)
        try:
            combine_close(coordinates, 50)
        except:
            pass
        create_track(coordinates, tracker, i)

def combine_close(coordinates, distance_threshold):
    points = [(coord["location"]["x"], coord["location"]["y"]) for coord in coordinates[1:]]  # Exclude the first element

    kdtree = KDTree(points)
    positions_to_remove = []

    for i, point in enumerate(points, start=1):  # Start at 1 instead of 0
        i += 1  # Adjust the index to align with the original array
        close_points = kdtree.query_ball_point(point, distance_threshold)
        if len(close_points) > 1:
            for close_point in close_points:
                if coordinates[close_point + 1]["sensor"] == "remoteid":
                    pass
                else:
                    positions_to_remove.append(close_point + 1)

    for position in sorted(positions_to_remove, reverse=True):
        try:
            del coordinates[position]
        except:
            pass

def read_file():
    lines = []
    with open("centers.txt", 'r') as file:
        for line in file:
            coordinates_str = line.strip().replace("(", "").replace(")", "")
            coordinates = tuple(map(float, [value.strip() for value in coordinates_str.split(',')]))
            lines.append(coordinates)
    return lines

lines = read_file()
create_sensors_data(lines)
