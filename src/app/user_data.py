
import json
import os

user_data_file = os.path.join(os.path.dirname(__file__), "../user_data.json")

def load_user_data():
    """Load user data from JSON file."""
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as file:
            return json.load(file)
    return {}

def save_user_data(data):
    """Save user data to JSON file."""
    with open(user_data_file, "w") as file:
        json.dump(data, file)

def create_user(username, password):
    """Add a new user to the data."""
    user_data = load_user_data()
    user_data[username] = {"password": password, "profile_image": None, "building": ""}
    save_user_data(user_data)

def validate_user(username, password):
    """Validate if username and password are correct."""
    user_data = load_user_data()
    return username in user_data and user_data[username]["password"] == password

def update_profile_image(username, image_path):
    """Update the profile image for a user."""
    user_data = load_user_data()
    if username in user_data:
        user_data[username]["profile_image"] = image_path
        save_user_data(user_data)
