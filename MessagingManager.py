class MessagingManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def send_message(self, sender, receiver, message):
        return self.db_manager.execute_query(
            '''INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)''',
            (sender, receiver, message)
        )

    def get_user_messages(self, username, other_user=None):
        if other_user:
            query = '''
            SELECT sender, receiver, message, timestamp 
            FROM messages 
            WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
            ORDER BY timestamp DESC
            '''
            params = (username, other_user, other_user, username)
        else:
            query = '''
            SELECT sender, receiver, message, timestamp 
            FROM messages 
            WHERE sender = ? OR receiver = ?
            ORDER BY timestamp DESC
            '''
            params = (username, username)
        return self.db_manager.fetch_all(query, params)
    
    def get_conversation_users(self, username):
        """Fetch unique users with whom the user has exchanged messages."""
        query = '''
            SELECT DISTINCT sender 
            FROM messages 
            WHERE receiver = ?
            UNION
            SELECT DISTINCT receiver 
            FROM messages 
            WHERE sender = ?
        '''
        result = self.db_manager.fetch_all(query, (username, username))
        return [row[0] for row in result]
    
    def get_messages_with_user(self, username, other_user):
        """Fetch all messages between the user and a specific other user."""
        query = '''
            SELECT sender, receiver, message, timestamp 
            FROM messages 
            WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
            ORDER BY timestamp ASC
        '''
        result = self.db_manager.fetch_all(query, (username, other_user, other_user, username))
        return result