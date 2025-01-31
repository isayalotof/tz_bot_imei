import sqlite3

import os
import binascii

db = sqlite3.connect('data.db')

c = db.cursor()

def is_user(user_id: int) -> bool:
    c.execute("SELECT COUNT(*) FROM White_list WHERE user_id = ?", (user_id,))
    exists = c.fetchone()[0] > 0
    return exists


def is_valid_token(api_token: str) -> bool:
    c.execute("SELECT COUNT(*) FROM White_list WHERE api_token = ?", (api_token,))
    exists = c.fetchone()[0] > 0
    return exists


def generate_access_token(length=12) -> str:
    return binascii.hexlify(os.urandom(length)).decode()


def check_imei(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False

    # Применяем алгоритм Луна
    total = 0
    for i in range(15):
        digit = int(imei[i])
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0

def add_user(user_id: int) -> None:
    api_token = generate_access_token(12)
    c.execute("""INSERT INTO White_list(user_id, api_token)
                      VALUES (?, ?)
                      ON CONFLICT(user_id) DO NOTHING
        """, (user_id, api_token))

    db.commit()


def get_token(user_id: int) -> str:
    c.execute("SELECT api_token FROM White_list WHERE user_id = ?", (user_id,))
    exists = c.fetchone()[0]
    return exists

