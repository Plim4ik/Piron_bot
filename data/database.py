import sqlite3

def create_connection():
    return sqlite3.connect("bot_users.db")

def setup_database():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'unassigned' CHECK(role IN ('unassigned', 'admin', 'allowed_user')),
        user_type TEXT CHECK(user_type IN ('owner', 'manager', 'operator')),
        minutes INTEGER,
        salary REAL
    )
    """)


    connection.commit()
    connection.close()

if __name__ == "__main__":
    setup_database()
