import json
import bcrypt

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def register_user(self, username, email, password, preferences=None):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        preferences_json = json.dumps(preferences) if preferences else None
        return self.db_manager.execute_query(
            '''INSERT INTO users (username, email, password, preferences) VALUES (?, ?, ?, ?)''',
            (username, email, hashed_password, preferences_json)
        )

    def authenticate_user(self, username, password):
        user = self.db_manager.fetch_one(
            'SELECT password FROM users WHERE username = ?', (username,)
        )
        return user and bcrypt.checkpw(password.encode('utf-8'), user[0])

    def get_user_profile(self, username):
        user = self.db_manager.fetch_one(
            'SELECT name, bio, preferences, profile_picture FROM users WHERE username = ?',
            (username,)
        )
        if user:
            name, bio, preferences_json, profile_picture = user
            preferences = json.loads(preferences_json) if preferences_json else {}
            return {"name": name, "bio": bio, "preferences": preferences, "profile_picture": profile_picture}
        return None

    def update_user_profile(self, username, name, bio, preferences, profile_picture):
        preferences_json = json.dumps(preferences)
        return self.db_manager.execute_query(
            '''UPDATE users SET name = ?, bio = ?, preferences = ?, profile_picture = ? WHERE username = ?''',
            (name, bio, preferences_json, profile_picture, username)
        )

    def calculate_compatibility(self, user_prefs, other_prefs):
        if not user_prefs or not other_prefs:
            return 0
        match_count = sum(1 for key in user_prefs if user_prefs.get(key) == other_prefs.get(key))
        total_questions = len(user_prefs)
        return round((match_count / total_questions) * 100) if total_questions > 0 else 0