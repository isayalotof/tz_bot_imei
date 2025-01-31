import sqlite3

from config.config import first_admin_id
from tool.functions import generate_access_token

db = sqlite3.connect('data.db')
c = db.cursor()


def sql():
    c.execute("""CREATE TABLE IF NOT EXISTS White_list(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_token str
        )""")

    api_token = generate_access_token(12)
    c.execute("""INSERT INTO White_list(user_id, api_token)
                  VALUES (?, ?)
                  ON CONFLICT(user_id) DO NOTHING
    """, (first_admin_id, api_token))

    db.commit()
