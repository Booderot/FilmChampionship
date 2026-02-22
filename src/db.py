import sqlite3

DB_PATH = "../data/scores.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    curs = conn.cursor()
    curs.executescript('''CREATE TABLE IF NOT EXISTS User (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Film (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        watch_date DATE,
        prediction_date DATE,
        multiplier INTEGER DEFAULT 1,
        fk_user_id VARCHAR(255),
        FOREIGN KEY (fk_user_id) REFERENCES User(id)
    );

    CREATE TABLE IF NOT EXISTS FilmEntry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_film_id INTEGER NOT NULL,
        fk_user_id VARCHAR(255) NOT NULL,
        rank INTEGER,
        prediction INTEGER,
        FOREIGN KEY (fk_film_id) REFERENCES Film(id),
        FOREIGN KEY (fk_user_id) REFERENCES User(id)
    );
    ''')

    conn.commit()
    conn.close()

def add_user_to_db(user_id, name):
    conn = get_connection()
    curs = conn.cursor()
    curs.execute('INSERT INTO User (id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    curs = conn.cursor()
    curs.execute('SELECT *, name FROM User')
    users = curs.fetchall()
    conn.close()
    return users

def remove_user_from_db(user_id):
    conn = get_connection()
    curs = conn.cursor()
    curs.execute('DELETE FROM User WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()