## Attach poster + learning facility link to the invite
# send link to const


import sqlite3

DATABASE = "users.db"


def get_db_connection():
    """Connects to the database and returns a connection object"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db():
    """Initialises the database from the schema file."""
    conn = get_db_connection()
    with open("schema.sql") as f:
        conn.executescript(f.read())

    # Insert a sample user
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (username, password)
                       VALUES (?, ?)''', ("admin", "password123"))
    conn.commit()
    conn.close()
    print("Database initialised with a sample user")


