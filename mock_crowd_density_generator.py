import time
import random
import json
from datetime import datetime
import socket

# Define zones and their capacities
zones = ["Zone-A", "Zone-B", "Zone-C", "Zone-D"]

def generate_crowd_density():
    zone_id = random.choice(zones)
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    crowd_density = random.randint(0, 100)  # Percentage of zone capacity
    return {
        "zone_id": zone_id,
        "timestamp": timestamp,
        "crowd_density": crowd_density
    }

def send_to_socket():
    host = "localhost"
    port = 9998
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Socket is ready at {host}:{port}")
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        with conn:
            while True:
                print("Generating crowd density data...")
                message = generate_crowd_density()
                print(message)
                conn.sendall((json.dumps(message) + "\n").encode())
                time.sleep(random.uniform(0.5, 2))  # Simulate varying data intervals

if __name__ == "__main__":
    send_to_socket()
