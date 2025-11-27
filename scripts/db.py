import psycopg2
from .config import DATABASE_CONFIGURATION
import bcrypt 

#Access database
def get_connection():
    connection = psycopg2.connect(
        dbname = DATABASE_CONFIGURATION['dbname'],
        user = DATABASE_CONFIGURATION['user'],
        password = DATABASE_CONFIGURATION['password'],
        host = DATABASE_CONFIGURATION['host'],
        port = DATABASE_CONFIGURATION['port']
    )
    return connection

#Creates all game tables if they don't yet exist
def db_init():
    connection = get_connection()
    curs = connection.cursor()

    # Metrics table
    curs.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id SERIAL PRIMARY KEY,
        score INTEGER NOT NULL,
        time_of_year TEXT NOT NULL
    )
    """)
    
    # Buildings table
    curs.execute("""
    CREATE TABLE IF NOT EXISTS buildings (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        level INTEGER DEFAULT 1
    )
    """)

    # Popups table
    curs.execute("""
    CREATE TABLE IF NOT EXISTS popups (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        already_completed BOOLEAN DEFAULT FALSE
    )
    """)
    
    # Users table
    curs.execute("""
    CREATE TABLE IF NOT EXISTS users (
        player_id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    # Scores table
    curs.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES users(player_id),
        score INTEGER NOT NULL
    )
    """)

    connection.commit()
    curs.close()
    connection.close()

    # Merics methods

def save_metrics(score, time_of_year):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM metrics")  # keep only one record
    cur.execute("INSERT INTO metrics (score, time_of_year) VALUES (%s, %s)",
                (score, time_of_year))
    conn.commit()
    cur.close()
    conn.close()

def load_metrics():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT score, time_of_year FROM metrics LIMIT 1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row if row else (0, "Spring")

    # Buildings methods

def save_buildings(buildings):
    conn = get_connection()
    cur = conn.cursor()
    for name, level in buildings.items():
        cur.execute("""
            INSERT INTO buildings (name, level)
            VALUES (%s, %s)
            ON CONFLICT (name) DO UPDATE SET level = EXCLUDED.level
        """, (name, level))
    conn.commit()
    cur.close()
    conn.close()

def load_buildings():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, level FROM buildings")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {name: level for name, level in rows}

    # Popups methods

def save_popups(popups):
    conn = get_connection()
    cur = conn.cursor()
    for popup in popups:
        cur.execute("""
            INSERT INTO popups (name, is_active, already_completed)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET is_active = EXCLUDED.is_active,
                already_completed = EXCLUDED.already_completed
        """, (popup['name'], popup['is_active'], popup['already_completed']))
    conn.commit()
    cur.close()
    conn.close()

def load_popups():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, is_active, already_completed FROM popups")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {'name': name, 'is_active': is_active, 'already_completed': completed}
        for name, is_active, completed in rows
    ]

# --- User auth functions ---
def create_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING player_id;",
        (username, hashed.decode())
    )
    player_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return player_id

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username=%s;", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        return True
    return False

# --- High score functions ---
def save_score(player_id, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (player_id, score) VALUES (%s, %s);", (player_id, score))
    conn.commit()
    cur.close()
    conn.close()

def get_high_scores(top_n=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.username, s.score
        FROM scores s
        JOIN users u ON s.player_id = u.player_id
        ORDER BY s.score DESC
        LIMIT %s;
    """, (top_n,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


