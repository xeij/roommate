class FriendsManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_received_requests(self, recipient_username):
        query = """
        SELECT sender 
        FROM friend_requests 
        WHERE receiver = ? AND LOWER(status) = 'pending'
        """
        results = self.db_manager.fetch_all(query, (recipient_username,))
        print(f"Received requests for {recipient_username}: {results}")  # Debugging
        return [row[0] for row in results]

    def get_sent_requests(self, sender_username):
        query = """
        SELECT receiver 
        FROM friend_requests 
        WHERE sender = ? AND LOWER(status) = 'pending'
        """
        results = self.db_manager.fetch_all(query, (sender_username,))
        print(f"Sent requests for {sender_username}: {results}")  # Debugging
        return [row[0] for row in results]

    def accept_request(self, receiver, sender):
        """Accept a friend request by adding to the friends table and removing the request."""
        try:
            # Add the friendship with status 'accepted'
            query_add_friend = """
            INSERT INTO friends (user1, user2, status) VALUES (?, ?, 'accepted')
            """
            self.db_manager.execute_query(query_add_friend, (sender, receiver))
            
            # Remove the friend request
            query_delete_request = """
            DELETE FROM friend_requests WHERE sender = ? AND receiver = ?
            """
            self.db_manager.execute_query(query_delete_request, (sender, receiver))
            
            print(f"Friend request accepted: {sender} -> {receiver}")
            return True
        except Exception as e:
            print(f"Error accepting friend request: {e}")
            return False

    def send_request(self, sender, receiver):
        """Send a friend request if no pending request or existing friendship exists."""
        # Check if a friend request already exists
        query_check_request = """
        SELECT 1 
        FROM friend_requests 
        WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?) AND LOWER(status) = 'pending'
        """
        existing_request = self.db_manager.fetch_one(query_check_request, (sender, receiver, receiver, sender))
        if existing_request:
            print(f"Friend request already exists between {sender} and {receiver}")
            return "Friend request already pending."

        # Check if the two users are already friends
        query_check_friendship = """
        SELECT 1 
        FROM friends 
        WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)
        """
        existing_friendship = self.db_manager.fetch_one(query_check_friendship, (sender, receiver, receiver, sender))
        if existing_friendship:
            print(f"{sender} and {receiver} are already friends.")
            return "Already friends."

        # Insert the friend request
        query_insert = """
        INSERT INTO friend_requests (sender, receiver, status) VALUES (?, ?, 'Pending')
        """
        try:
            self.db_manager.execute_query(query_insert, (sender, receiver))
            print(f"Friend request sent: {sender} -> {receiver}")
            return "Friend request sent."
        except sqlite3.IntegrityError as e:
            print(f"Database error: {e}")
            return "Database error."
    
    def decline_request(self, receiver, sender):
        query = "DELETE FROM friend_requests WHERE sender = ? AND receiver = ?"
        self.db_manager.execute_query(query, (sender, receiver))
        return True

    def get_friends_list(self, username):
        query = """
        SELECT user1 
        FROM friends 
        WHERE user2 = ? AND status = 'accepted'
        UNION
        SELECT user2 
        FROM friends 
        WHERE user1 = ? AND status = 'accepted'
        """
        return [row[0] for row in self.db_manager.fetch_all(query, (username, username))]
    
    def remove_friend(self, user1, user2):
        """Remove a friendship between two users."""
        query = """
        DELETE FROM friends 
        WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)
        """
        return self.db_manager.execute_query(query, (user1, user2, user2, user1))