import sqlite3

class DataBaseManager:
    def __init__(self, db_name="roommate_finder.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create all required tables."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            bio TEXT,
            preferences TEXT,
            profile_picture TEXT
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS friend_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS friends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1 TEXT NOT NULL,
                user2 TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('pending', 'accepted')),
                UNIQUE(user1, user2)
            )
        ''')
        self.conn.commit()

    def execute_query(self, query, params=()):
        """Execute a query and return the cursor."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except sqlite3.IntegrityError as e:
            print(f"Database error: {e}")
            return None

    def fetch_all(self, query, params=()):
        """Fetch all rows from a query."""
        result = self.execute_query(query, params)
        return result.fetchall() if result else []

    def fetch_one(self, query, params=()):
        """Fetch one row from a query."""
        result = self.execute_query(query, params)
        return result.fetchone() if result else None

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()