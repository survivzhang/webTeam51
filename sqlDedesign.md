import sqlite3

db_path='database.db'

def init_db():
    """
    Initialize the SQLite database using the schema.
    :param db_path: Path to the SQLite database file.
    """
    schema = """
    -- Enable foreign key constraints (Required for SQLite)
    PRAGMA foreign_keys = ON;

    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Meal types table (System predefined)
    CREATE TABLE IF NOT EXISTS meal_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        display_name TEXT NOT NULL
    );

    -- Initial data
    INSERT OR IGNORE INTO meal_types (name, display_name) VALUES
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack');

    -- Calorie entries table (Core data)
    CREATE TABLE IF NOT EXISTS calorie_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        meal_type_id INTEGER NOT NULL,
        date DATE NOT NULL,
        calories INTEGER NOT NULL,
        food_detail TEXT,               -- Food details
        photo_url TEXT,                 -- Photo storage path
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (meal_type_id) REFERENCES meal_types(id)
    );

    -- Friendships table (Bidirectional relationships)
    CREATE TABLE IF NOT EXISTS friendships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        friend_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',  -- pending/accepted/rejected
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        CHECK (user_id != friend_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE (user_id, friend_id)  -- Prevent duplicate relationships
    );

    -- Shared calories table (Core permission control)
    CREATE TABLE IF NOT EXISTS shared_calories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sharer_id INTEGER NOT NULL,
        recipient_id INTEGER NOT NULL,
        conditions TEXT NOT NULL,       -- JSON format sharing conditions
        expires_at DATE,                -- Sharing validity period (optional)
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (sharer_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
    );

    -- Notifications table (Sharing notifications)
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        is_read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        related_share_id INTEGER,       -- Associated sharing ID
        
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (related_share_id) REFERENCES shared_calories(id)
    );

    -- Index optimization
    CREATE INDEX IF NOT EXISTS idx_entries_user_date ON calorie_entries(user_id, date);
    CREATE INDEX IF NOT EXISTS idx_shared_conditions ON shared_calories(recipient_id, expires_at);
    CREATE INDEX IF NOT EXISTS idx_friendships_status ON friendships(user_id, status);
    """

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute schema
        cursor.executescript(schema)
        conn.commit()

        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

if __name__ == '__main__':
    # Run the initialization
    initialize_database()