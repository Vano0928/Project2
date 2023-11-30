from .db import DefaultInterface

class DbUsers(DefaultInterface):
    def create_default_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(32) NOT NULL,
                first_name VARCHAR(256),
                last_name VARCHAR(256),
                telegram_user_id INTEGER,
                english_level VARCHAR(2)
            );
        """)
        return self.conn.commit()


    def get_user_by_telegram_id(self, telegram_user_id: int):
        self.cursor.execute(f"""
            SELECT *
            FROM users
            WHERE telegram_user_id = ?
        """, (telegram_user_id, ))

        return self.cursor.fetchone()
    
    def user_exists(self, telegram_user_id: int):
        self.cursor.execute("""
            SELECT COUNT(1)
            FROM users
            WHERE telegram_user_id = ?
        """, (telegram_user_id, ))
        return bool(self.cursor.fetchone()[0])
    
    def register_user(self, from_user):

        telegram_user_id = from_user.id
        first_name = from_user.first_name
        last_name = from_user.last_name
        username = from_user.username

        self.cursor.execute("""
            INSERT INTO users (telegram_user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """, (telegram_user_id, username, first_name, last_name, ))

        return self.conn.commit()
    
    def delete_user(self, telegram_user_id: int):
        self.cursor.execute("""
            DELETE FROM users WHERE telegram_user_id = ?
        """, (telegram_user_id, ))
        return self.conn.commit()
    

    def edit_user_data(self, telegram_user_id: int, first_name: str, last_name: str, username: str):
        self.cursor.execute("""
            UPDATE users
            SET first_name = ?, last_name = ?, username = ?
            WHERE telegram_user_id = ?
            """, (first_name, last_name, username, telegram_user_id))
