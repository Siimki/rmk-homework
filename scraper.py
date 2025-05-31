import requests
import time
import csv
import os

from zoneinfo import ZoneInfo  
from datetime import datetime
from math import radians, cos, sqrt

def init_csv_log(path="bus_events.csv"):
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "timestamp_pretty", "vehicle_id", "event", "latitude", "longitude"])

def log_event(event_type, bus_data, path="bus_events.csv"):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            bus_data["timestamp"],
            bus_data["timestamp_pretty"],
            bus_data["vehicle_id"],
            event_type,
            bus_data["latitude"],
            bus_data["longitude"]
        ])


def is_near(lat1, lon1, lat2, lon2, radius_m=40):

    """
    Returns True if (lat1, lon1) is within `radius_m` of (lat2, lon2)
    """
    R = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    x = (lon2 - lon1) * cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    return R * sqrt(x * x + y * y) < radius_m

def parse_bus_row(row: str):
    parts = row.strip().split(",")
    if len(parts) < 10:
        return None

    bus_line = parts[1].strip()
    if bus_line != "8":
        return None

    destination = parts[9].strip().lower()
    if "igrum" not in destination:
        return None

    try:
        lon = int(parts[2]) / 1_000_000
        lat = int(parts[3]) / 1_000_000
        vehicle_id = parts[8].strip()
    except ValueError:
        return None
    
    now = datetime.now(ZoneInfo("Europe/Tallinn"))    
    
    return {
        "timestamp": now.isoformat(),
        "timestamp_pretty": now.strftime("%H:%M:%S"),  
        "latitude": lat,
        "longitude": lon,
        "destination": destination,
        "vehicle_id": vehicle_id
    }

def main():
    init_csv_log()

    response = requests.get("https://transport.tallinn.ee/gps.txt")
    lines = response.text.strip().split("\n")

    ZOO_COORDINATES = (59.426263, 24.658947)
    TOOMPARK_COORDINATES = (59.436826, 24.733261)

    bus_states = {}  # vehicle_id → {"at_zoo": bool, "at_toompark": bool}

    print("Filtered results (bus 8 to Äigrumäe):\n")
    while True:
        try:
            response = requests.get("https://transport.tallinn.ee/gps.txt", timeout=5)
            lines = response.text.strip().split("\n")

            for line in lines:
                bus_data = parse_bus_row(line)
                if bus_data:
                    vehicle_id = bus_data["vehicle_id"]
                    lat = bus_data["latitude"]
                    lon = bus_data["longitude"]

                    # Initialize state if not seen before
                    if vehicle_id not in bus_states:
                        bus_states[vehicle_id] = {"at_zoo": False, "at_toompark": False}

                    # ZOO
                    near_zoo = is_near(lat, lon, *ZOO_COORDINATES)
                    if near_zoo and not bus_states[vehicle_id]["at_zoo"]:
                        log_event("arrived_zoo", bus_data)
                        bus_states[vehicle_id]["at_zoo"] = True
                        print("Bus arrived to zoo!", bus_data["timestamp_pretty"])
                    elif not near_zoo and bus_states[vehicle_id]["at_zoo"]:
                        log_event("left_zoo", bus_data)
                        bus_states[vehicle_id]["at_zoo"] = False
                        print("Bus left zoo!", bus_data["timestamp_pretty"])


                    # TOOMPARK
                    near_toompark = is_near(lat, lon, *TOOMPARK_COORDINATES)
                    if near_toompark and not bus_states[vehicle_id]["at_toompark"]:
                        log_event("arrived_toompark", bus_data)
                        bus_states[vehicle_id]["at_toompark"] = True
                        print("Bus arrived toompark!", bus_data["timestamp_pretty"])

                    elif not near_toompark and bus_states[vehicle_id]["at_toompark"]:
                        log_event("left_toompark", bus_data)
                        bus_states[vehicle_id]["at_toompark"] = False
                        print("Bus left toompark!", bus_data["timestamp_pretty"])



        except Exception as e:
            print(f"Error fetching data: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
