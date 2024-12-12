import bcrypt
from User import User  

class Admin(User):
    def __init__(self, db_manager):
        super().__init__(db_manager)

    def review_flagged_messages(self):
        result = self.db_manager.execute_query('SELECT * FROM flagged_messages')  
        flagged_messages = result.fetchall()  

        if flagged_messages:
            print("Flagged Messages:")
            for message in flagged_messages:
                print(f"Message ID: {message[0]}, User ID: {message[1]}, Content: {message[2]}")
        else:
            print("No flagged messages found.")

    def ban_user(self, user_id):
        result = self.db_manager.execute_query(
            'UPDATE users SET status = ? WHERE id = ?', 
            ('banned', user_id)
        )

        if result.rowcount > 0:
            print(f"User with ID {user_id} has been banned.")
        else:
            print(f"Failed to ban user with ID {user_id}. User may not exist.")

    def unban_user(self, user_id):
        result = self.db_manager.execute_query(
            'UPDATE users SET status = ? WHERE id = ?', 
            ('active', user_id)
        )

        if result.rowcount > 0:
            print(f"User with ID {user_id} has been unbanned.")
        else:
            print(f"Failed to unban user with ID {user_id}. User may not exist.")

    def remove_message(self, message_id):
        result = self.db_manager.execute_query('DELETE FROM messages WHERE id = ?', (message_id,))

        if result.rowcount > 0:
            print(f"Message with ID {message_id} has been removed.")
        else:
            print(f"Failed to remove message with ID {message_id}. Message may not exist.")

    def update_app_permissions(self, key, value):
        result = self.db_manager.execute_query(
            'UPDATE app_settings SET value = ? WHERE key = ?',
            (value, key)
        )

        if result.rowcount > 0:
            print(f"Setting '{key}' updated to '{value}'.")
        else:
            print(f"Failed to update setting '{key}'. Setting may not exist.")

    def list_admin_responsibilities(self):
        responsibilities = [
            "Monitor and review flagged messages.",
            "Ban or unban users.",
            "Remove inappropriate content.",
            "Update application settings.",
        ]
        print("Admin Responsibilities:")
        for responsibility in responsibilities:
            print(f"- {responsibility}")
