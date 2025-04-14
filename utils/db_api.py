import psycopg2, globals


def get_db_connection():
    if globals.db:
        return
    try:
        conn = psycopg2.connect(
            host=globals.HOST,
            port=globals.PORT,
            database=globals.DATABASE,
            user=globals.USERNAME,
            password=globals.PASSWORD,
            sslmode="require",
        )
        print("I'm online")
        print(conn)
        print(conn.cursor())
        globals.online = True
        globals.db = conn
        return conn
    except Exception as e:
        raise e


if __name__ == "__main__":
    db = get_db_connection()
    commands = [
        # """  ROOT COMMANDS
        # CREATE ROLE public_users;
        # CREATE USER public_user WITH PASSWORD '1234';
        # GRANT public_users TO public_user;
        # REVOKE CONNECT ON DATABASE bomberchal_0f22 FROM PUBLIC;
        # GRANT CONNECT ON DATABASE bomberchal_0f22 TO public_users;
        # GRANT USAGE ON SCHEMA public TO public_users;
        # GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO public_users;
        # ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO public_users;
        # """

        # """
        # ALTER USER public_user WITH PASSWORD '1234';
        # """

        # """
        # CREATE TABLE scoreboard (
        #     username TEXT NOT NULL PRIMARY KEY UNIQUE,
        #     pve_score INTEGER DEFAULT 0,
        #     bossfight_score INTEGER DEFAULT 0,
        #     duel_wins INTEGER DEFAULT 0,
        #     duel_loses INTEGER DEFAULT 0,
        #     duel_draws INTEGER DEFAULT 0
        # );
        # """,

        """
        SELECT * FROM scoreboard;
        """,
    ]
    with db.cursor() as cur:
        for command in commands:
            cur.execute(command)

        print(cur.fetchall())
        db.commit()
    print("SUCCESS")

