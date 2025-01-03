import time
import random
import json
from datetime import datetime
import socket

# Define stalls and their items
stalls = {
    "FoodTruck-1": ["Soda", "Hotdog", "Burger"],
    "FoodTruck-2": ["Pizza", "Water", "Salad"],
    "Merchandise-1": ["T-Shirt", "Cap", "Poster"],
    "Merchandise-2": ["Jersey", "Mug", "Scarf"]
}

def generate_sales_data():
    stall_id = random.choice(list(stalls.keys()))
    item = random.choice(stalls[stall_id])
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    items_sold = random.randint(1, 5)
    stock_remaining = max(0, 100 - items_sold)  # Simulate decreasing stock
    return {
        "stall_id": stall_id,
        "item": item,
        "timestamp": timestamp,
        "items_sold": items_sold,
        "stock_remaining": stock_remaining
    }

def send_to_socket():
    host = "localhost"
    port = 9997
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Socket is ready at {host}:{port}")
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        with conn:
            while True:
                message = generate_sales_data()
                conn.sendall((json.dumps(message) + "\n").encode())
                time.sleep(random.uniform(0.5, 2))  # Simulate varying data intervals

if __name__ == "__main__":
    send_to_socket()
