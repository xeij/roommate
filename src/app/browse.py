import os
import json

user_data_file = os.path.join(os.path.dirname(__file__), "../user_data.json")

def search_user_by_name_or_building(name, building):
    """Search for a user by name or building."""
    if not name and not building:
        return None, "Please enter a name or building!"

    if not os.path.exists(user_data_file):
        return None, "The user data file does not exist."

    with open(user_data_file, "r") as file:
        user_data = json.load(file)

    for user, info in user_data.items():
        if (name and user.lower() == name.lower()) or (
            building and info.get("building", "").lower() == building.lower()
        ):
            return {"name": user, **info}, None

    return None, "No user found with the given details."
