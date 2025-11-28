import psycopg2
from .config import DATABASE_CONFIGURATION
import bcrypt 

# Access database
def get_connection():
    connection = psycopg2.connect(
        dbname = DATABASE_CONFIGURATION['dbname'],
        user = DATABASE_CONFIGURATION['user'],
        password = DATABASE_CONFIGURATION['password'],
        host = DATABASE_CONFIGURATION['host'],
        port = DATABASE_CONFIGURATION['port']
    )
    return connection

# Creates all game tables if they don't yet exist
def db_init():
    connection = get_connection()
    curs = connection.cursor()

    curs.execute("""
    CREATE TABLE IF NOT EXISTS user_state (
        player_id INTEGER PRIMARY KEY REFERENCES users(player_id),
        state_json JSONB
    )
    """)
    
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

    # Per-User game save tables

    curs.execute("""
    CREATE TABLE IF NOT EXISTS user_metrics (
        player_id INTEGER PRIMARY KEY REFERENCES users(player_id),
        score INTEGER NOT NULL,
        time_of_year TEXT NOT NULL
    )
    """)

    curs.execute("""
    CREATE TABLE IF NOT EXISTS user_buildings (
        player_id INTEGER REFERENCES users(player_id),
        name TEXT NOT NULL,
        level INTEGER NOT NULL,
        PRIMARY KEY (player_id, name)
    )
    """)

    curs.execute("""
    CREATE TABLE IF NOT EXISTS user_popups (
        player_id INTEGER REFERENCES users(player_id),
        name TEXT NOT NULL,
        is_active BOOLEAN NOT NULL,
        already_completed BOOLEAN NOT NULL,
        PRIMARY KEY (player_id, name)
    )
    """)

    connection.commit()
    curs.close()
    connection.close()

# Global save methods

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

# User authentication methods

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

# High score methods

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

def get_user_id(username):
    """Return the player's ID for a given username, or None if not found."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT player_id FROM users WHERE username = %s;", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

# Per-user save and load methods

def save_game_for_user(player_id, metrics, buildings, popups):
    conn = get_connection()
    cur = conn.cursor()

    # Metrics
    cur.execute("""
        INSERT INTO user_metrics (player_id, score, time_of_year)
        VALUES (%s, %s, %s)
        ON CONFLICT (player_id) DO UPDATE
        SET score = EXCLUDED.score,
            time_of_year = EXCLUDED.time_of_year;
    """, (player_id, metrics["score"], metrics["time_of_year"]))

    # Buildings
    for name, level in buildings.items():
        cur.execute("""
            INSERT INTO user_buildings (player_id, name, level)
            VALUES (%s, %s, %s)
            ON CONFLICT (player_id, name) DO UPDATE
            SET level = EXCLUDED.level;
        """, (player_id, name, level))

    # Popups
    for popup in popups:
        cur.execute("""
            INSERT INTO user_popups (player_id, name, is_active, already_completed)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (player_id, name) DO UPDATE
            SET is_active = EXCLUDED.is_active,
                already_completed = EXCLUDED.already_completed;
        """, (player_id, popup['name'], popup['is_active'], popup['already_completed']))

    conn.commit()
    cur.close()
    conn.close()


def load_game_for_user(player_id):
    conn = get_connection()
    cur = conn.cursor()

    # metrics
    cur.execute("SELECT score, time_of_year FROM user_metrics WHERE player_id=%s;", (player_id,))
    row = cur.fetchone()
    metrics = {"score": row[0], "time_of_year": row[1]} if row else {"score": 0, "time_of_year": "Spring"}

    # buildings
    cur.execute("SELECT name, level FROM user_buildings WHERE player_id=%s;", (player_id,))
    buildings = {name: level for name, level in cur.fetchall()}

    # popups
    cur.execute("SELECT name, is_active, already_completed FROM user_popups WHERE player_id=%s;", (player_id,))
    popup_rows = cur.fetchall()
    popups = [
        {"name": n, "is_active": act, "already_completed": done}
        for n, act, done in popup_rows
    ]

    cur.close()
    conn.close()
    return metrics, buildings, popups

# Methods for loading a saved game
import json

def save_full_state(player_id, state_dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO user_state (player_id, state_json)
        VALUES (%s, %s)
        ON CONFLICT (player_id)
        DO UPDATE SET state_json = EXCLUDED.state_json
    """, (player_id, json.dumps(state_dict)))

    conn.commit()
    cur.close()
    conn.close()
    print("FULL STATE SAVED for", player_id)


def load_full_state(player_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT state_json FROM user_state WHERE player_id = %s
    """, (player_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        print("No saved state for user", player_id)
        return None

    print("FULL STATE LOADED for", player_id)
    return row[0]  
