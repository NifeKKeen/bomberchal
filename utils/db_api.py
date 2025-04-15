import psycopg2, globals
from psycopg2 import pool

def query_check():
    try:
        with globals.db.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.close()
        return True
    except Exception as e:
        # print(e)
        return False

def check_db_connection():
    # using of multithreading to prevent infinite connection attempts
    import threading
    thr = threading.Thread(target=query_check)
    thr.start()
    thr.join(5) # giving 5 seconds to connect
    return not thr.is_alive()

def get_db_connection():
    if globals.db: # caching db
        if check_db_connection():
            return globals.db

    try:
        conn = psycopg2.connect(
            host=globals.HOST,
            port=globals.PORT,
            database=globals.DATABASE,
            user=globals.USERNAME,
            password=globals.PASSWORD,
            sslmode="require",
            connect_timeout=2,
            options='-c statement_timeout=2000'
        )
        globals.db = conn
        return conn
    except Exception as e:
        globals.db = None
        return None


if __name__ == "__main__":
    db = get_db_connection()
    commands = [
        # ROOT COMMANDS
        # """
        # CREATE ROLE public_users;
        # CREATE USER public_user WITH PASSWORD '1234';
        # GRANT public_users TO public_user;
        # REVOKE CONNECT ON DATABASE bomberchal_0f22 FROM PUBLIC;
        # GRANT CONNECT ON DATABASE bomberchal_0f22 TO public_users;
        # GRANT USAGE ON SCHEMA public TO public_users;
        # GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO public_users;
        # ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO public_users;
        # """,

        # """
        # ALTER USER public_user WITH PASSWORD '1234';
        # """,


        # """
        # CREATE TABLE users (
        #     id SERIAL PRIMARY KEY,
        #     username TEXT UNIQUE
        # )
        # """,
        #
        # """
        # DROP TABLE scoreboard
        # """,
        #
        # """
        # CREATE TABLE scoreboard (
        #     user_id INTEGER PRIMARY KEY,
        #     pve_score INTEGER DEFAULT 0,
        #     bossfight_score INTEGER DEFAULT 0,
        #     duel_wins INTEGER DEFAULT 0,
        #     duel_loses INTEGER DEFAULT 0,
        #     duel_draws INTEGER DEFAULT 0,
        #     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        # );
        # """,
        #
        # """
        # SELECT * FROM scoreboard;
        # """,
    ]
    if db:
        with db.cursor() as cur:
            for command in commands:
                cur.execute(command)

            print(cur.fetchall())
            db.commit()
        print("SUCCESS")

