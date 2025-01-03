import random
import time
import json
from datetime import datetime
from transformers import pipeline
import socket

# Pre-defined categories and associated keywords
categories = {
    "Food Options": ["food", "snacks", "drinks", "beverage", "concession"],
    "Ambiance": ["lighting", "music", "cleanliness", "atmosphere", "ambiance"],
    "Staff Behavior": ["staff", "helpfulness", "rudeness", "service"],
    "Event Organization": ["schedule", "timing", "organization", "logistics"],
    "Pricing": ["ticket price", "concession cost", "value", "worth"]
}

# Adjectives to use in tweet generation
adjectives = {
    "positive": ["amazing", "great", "fantastic", "reasonable", "lovely"],
    "negative": ["awful", "bad", "terrible", "horrible", "overpriced"]
}

# Sentiment analysis pipeline (Hugging Face)
sentiment_analyzer = pipeline("sentiment-analysis")

# Contextual templates for each category
templates = {
    "positive": [
        "The {keyword} was {adjective}. Really enjoyed it.",
        "Honestly, the {keyword} feels {adjective}. Great experience.",
        "The {keyword} is {adjective}. Very well done!",
    ],
    "negative": [
        "I'm disappointed with the {keyword}. It's {adjective}.",
        "The {keyword} needs serious improvement. Totally {adjective}.",
        "Honestly, the {keyword} feels {adjective}. Not acceptable."
    ]
}

def generate_mock_tweet():
    category = random.choice(list(categories.keys()))
    keyword = random.choice(categories[category])
    sentiment = random.choice(["positive", "negative"])
    adjective = random.choice(adjectives[sentiment])
    template = random.choice(templates[sentiment])
    tweet = template.format(keyword=keyword, adjective=adjective)
    return {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "content": tweet,
        "categories": [category],
        "sentiment_score": sentiment_analyzer(tweet)[0]['score'] * (1 if sentiment == "positive" else -1)
    }

def send_to_socket():
    host = "localhost"
    port = 9999
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Socket is ready at {host}:{port}")
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        with conn:
            while True:
                message = generate_mock_tweet()
                conn.sendall((json.dumps(message) + "\n").encode())
                time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    send_to_socket()
