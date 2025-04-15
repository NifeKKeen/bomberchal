import psycopg2
import globals


def get_db_connection(should_reconnect=False):
    if not should_reconnect and globals.db:  # caching db
        return globals.db

    try:
        conn = psycopg2.connect(
            host=globals.HOST,
            port=globals.PORT,
            database=globals.DATABASE,
            user=globals.USERNAME,
            password=globals.PASSWORD,
            sslmode="require",
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
        # );
        # """,
        # """
        # DROP TABLE pve_games;
        # """,
        # """
        # DROP TABLE bossfight_games;
        # """,
        # """
        # DROP TABLE duel_games;
        # """,
        # """
        # CREATE TABLE pve_games (
        #     user_id INTEGER NOT NULL,
        #     score INTEGER DEFAULT 0,
        #     recorded_at TIMESTAMP DEFAULT now(),
        #
        #     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        # );
        # """,
        # """
        # CREATE TABLE bossfight_games (
        #     user_id INTEGER NOT NULL,
        #     score INTEGER DEFAULT 0,
        #     recorded_at TIMESTAMP DEFAULT now(),
        #     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        # );
        # """,
        # """
        # CREATE TABLE duel_games (
        #     user_id INTEGER NOT NULL,
        #     wins INTEGER DEFAULT 0,
        #     draws INTEGER DEFAULT 0,
        #     loses INTEGER DEFAULT 0,
        #     recorded_at TIMESTAMP DEFAULT now(),
        #     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        # );
        # """,
    ]
    if db:
        with db.cursor() as cur:
            for command in commands:
                cur.execute(command)

            # print(cur.fetchall())
            db.commit()
        print("SUCCESS")

