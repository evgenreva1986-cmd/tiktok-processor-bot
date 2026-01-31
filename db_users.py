import sqlite3
class users_info:
    def __init__(self):
        self.connection = sqlite3.connect("us_stats.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS us_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT,
            link TEXT NOT NULL
                            ) 
        ''')
        self.connection.commit()

    def add_info(self, us_id, us_name, link):
        self.cursor.execute(
            'INSERT INTO us_info (user_id, user_name, link) VALUES (?, ?, ?)', (us_id, us_name, link)
        )
        self.connection.commit()
    
    def return_info(self):
        self.cursor.execute('SELECT * FROM us_info')
        users_info = self.cursor.fetchall()
        return users_info
    