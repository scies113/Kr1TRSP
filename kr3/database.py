import sqlite3
from typing import Generator

DATABASE_NAME = "users.db"

def get_db_connection():
    #установка соединения с бд sqlite
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    #создание необходимых таблиц в базе данных
    with get_db_connection() as conn:
        cursor = conn.cursor()
        #таблица пользователей для задания 8.1
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        #таблица задач для задания 8.2
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0
            )
        """)
        conn.commit()

#создание таблиц при импорте модуля
create_tables()
