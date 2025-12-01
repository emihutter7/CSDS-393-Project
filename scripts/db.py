import psycopg2
from .config import DATABASE_CONFIGURATION
import bcrypt
import json

# Fallback in-memory storage if Postgres is unavailable.
DB_AVAILABLE = True
_fallback_users = {}
_fallback_user_seq = 1
_fallback_metrics = {"score": 0, "time_of_year": "Spring"}
_fallback_buildings = {}
_fallback_popups = []
_fallback_user_metrics = {}
_fallback_user_buildings = {}
_fallback_user_popups = {}
_fallback_user_state = {}
_fallback_scores = []

# Access database
def get_connection():
    global DB_AVAILABLE
    if not DB_AVAILABLE:
        return None
    try:
        connection = psycopg2.connect(
            dbname = DATABASE_CONFIGURATION['dbname'],
            user = DATABASE_CONFIGURATION['user'],
            password = DATABASE_CONFIGURATION['password'],
            host = DATABASE_CONFIGURATION['host'],
            port = DATABASE_CONFIGURATION['port']
        )
        return connection
    except Exception as exc:
        print("Postgres unavailable, using in-memory fallback. Error:", exc)
        DB_AVAILABLE = False
        return None

# Creates all game tables if they don't yet exist
def db_init():
    connection = get_connection()
    if connection is None:
        return

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

    # -------------------------
    # Per-user game save tables
    # -------------------------
    # Metrics
    curs.execute("""
    CREATE TABLE IF NOT EXISTS user_metrics (
        player_id INTEGER PRIMARY KEY REFERENCES users(player_id),
        score INTEGER NOT NULL,
        time_of_year TEXT NOT NULL
    )
    """)

    # User 
    curs.execute("""
    CREATE TABLE IF NOT EXISTS user_buildings (
        player_id INTEGER REFERENCES users(player_id),
        name TEXT NOT NULL,
        level INTEGER NOT NULL,
        PRIMARY KEY (player_id, name)
    )
    """)

    # Popups
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

# -------------------
# Global save methods
# -------------------
def save_metrics(score, time_of_year, turn):
    conn = get_connection()
    if conn is None:
        _fallback_metrics["score"] = score
        _fallback_metrics["time_of_year"] = time_of_year
        _fallback_metrics["turn"] = turn 
        return

    cur = conn.cursor()
    cur.execute("DELETE FROM metrics")  
    cur.execute("INSERT INTO metrics (score, time_of_year) VALUES (%s, %s)",
                (score, time_of_year))
    conn.commit()
    cur.close()
    conn.close()


def load_metrics():
    conn = get_connection()
    
    if conn is None:
        return (
            _fallback_metrics.get("score", 0),
            _fallback_metrics.get("time_of_year", "Spring"),
            _fallback_metrics.get("turn", 1)
        )
    
    cur = conn.cursor()
    cur.execute("SELECT score, time_of_year FROM metrics LIMIT 1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        score, time_of_year, turn = row
        return score, time_of_year, turn

    return 0, "Spring", 1


# -------------------------
# Save and loading buildings
# -------------------------
def save_buildings(buildings):
    conn = get_connection()
    if conn is None:
        _fallback_buildings.update(buildings)
        return

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
    if conn is None:
        return dict(_fallback_buildings)

    cur = conn.cursor()
    cur.execute("SELECT name, level FROM buildings")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {name: level for name, level in rows}

# -------------------------
# Save and loading popups
# -------------------------
def save_popups(popups):
    conn = get_connection()
    if conn is None:
        _fallback_popups[:] = popups
        return

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
    if conn is None:
        return list(_fallback_popups)

    cur = conn.cursor()
    cur.execute("SELECT name, is_active, already_completed FROM popups")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {'name': name, 'is_active': is_active, 'already_completed': completed}
        for name, is_active, completed in rows
    ]


# -------------------------
# User authentication functions
# -------------------------
def create_user(username, password):
    global _fallback_user_seq
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = get_connection()
    if conn is None:
        if username in _fallback_users:
            raise ValueError("Username already exists")
        player_id = _fallback_user_seq
        _fallback_user_seq += 1
        _fallback_users[username] = {"hash": hashed.decode(), "player_id": player_id}
        return player_id

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
    if conn is None:
        user = _fallback_users.get(username)
        if not user:
            return False
        return bcrypt.checkpw(password.encode(), user["hash"].encode())

    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username=%s;", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        return True
    return False

# -------------------------
# High score functions
# -------------------------
def save_score(player_id, score):
    conn = get_connection()
    if conn is None:
        _fallback_scores.append((player_id, score))
        return

    cur = conn.cursor()
    cur.execute("INSERT INTO scores (player_id, score) VALUES (%s, %s);", (player_id, score))
    conn.commit()
    cur.close()
    conn.close()

def get_high_scores(top_n=10):
    conn = get_connection()
    if conn is None:
        # In fallback, we don't have usernames for scores, so just return ids
        sorted_scores = sorted(_fallback_scores, key=lambda x: x[1], reverse=True)[:top_n]
        return [("player_"+str(pid), score) for pid, score in sorted_scores]

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
    if conn is None:
        user = _fallback_users.get(username)
        return user["player_id"] if user else None

    cur = conn.cursor()
    cur.execute("SELECT player_id FROM users WHERE username = %s;", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None


# -------------------------
# Per-user save and load functions
# -------------------------
def save_game_for_user(player_id, metrics, buildings, popups):
    conn = get_connection()
    if conn is None:
        _fallback_user_metrics[player_id] = metrics
        _fallback_user_buildings[player_id] = buildings
        _fallback_user_popups[player_id] = popups
        return

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
    if conn is None:
        metrics = _fallback_user_metrics.get(player_id, {"score": 0, "time_of_year": "Spring"})
        buildings = _fallback_user_buildings.get(player_id, {})
        popups = _fallback_user_popups.get(player_id, [])
        return metrics, buildings, popups

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

# ----------------------------------
# Functions for loading a saved game
# ----------------------------------
def save_full_state(player_id, state_dict):
    conn = get_connection()
    if conn is None:
        _fallback_user_state[player_id] = state_dict
        print("FULL STATE SAVED (fallback) for", player_id)
        return

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
    if conn is None:
        if player_id not in _fallback_user_state:
            print("No saved state for user", player_id)
            return None
        print("FULL STATE LOADED (fallback) for", player_id)
        return _fallback_user_state[player_id]

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
