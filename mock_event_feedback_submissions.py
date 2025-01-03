import time
import random
import json
from datetime import datetime
import socket

# Predefined categories and example comments
categories = ["Food Options", "Ambiance", "Staff Behavior", "Event Organization", "Pricing"]
example_comments = [
    "The food was great but the staff was rude.",
    "Loved the ambiance, but the pricing was too high.",
    "The event organization was fantastic!",
    "The snacks were okay, but the drinks were overpriced.",
    "The staff was very helpful and friendly."
]

def generate_feedback():
    feedback_id = f"F{random.randint(1000, 9999)}"
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    comments = random.choice(example_comments)
    ratings = {category: random.randint(1, 5) for category in categories}  # Ratings from 1 to 5
    return {
        "feedback_id": feedback_id,
        "timestamp": timestamp,
        "comments": comments,
        "ratings": ratings
    }

def send_to_socket():
    host = "localhost"
    port = 9996
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Socket is ready at {host}:{port}")
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        with conn:
            while True:
                message = generate_feedback()
                conn.sendall((json.dumps(message) + "\n").encode())
                time.sleep(random.uniform(2, 5))  # Simulate slower feedback intervals

if __name__ == "__main__":
    send_to_socket()
