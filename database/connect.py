import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
database = os.getenv("DATABASE").replace("sqlite:///", "")

conn = sqlite3.connect(database)

def get_db_connection():
    return sqlite3.connect(database)

def execute_query(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_one(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result

def fetch_all(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result
