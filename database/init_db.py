import sqlite3
import json
import uuid
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

def initialize_database(db_path, schema_path):
    """
    Initialize the database with the provided schema if it does not already exist.

    :param schema_path: Path to the SQL schema file.
    """
    if os.path.exists(db_path):
        os.remove(db_path)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the schema file
    with open(schema_path, 'r', encoding='utf-8') as schema_file:
        schema = schema_file.read()

    # Execute the schema
    cursor.executescript(schema)
    print("Database initialized with the following schema:")
    print(schema)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    

def insert_users_from_json(db_path, users_path):
    """
    Insert user data from a JSON file into the database.

    :param users_path: Path to the JSON file containing user data.
    """

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the users file
    with open(users_path, 'r', encoding='utf-8') as users_file:
        users = json.load(users_file)

    # Insert users into the database
    for user in users:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user['username'], user['password'])
        )
    print("Users added to the database:")
    for user in users:
        print(user)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":

    db_path = os.getenv('DATABASE').replace("sqlite:///", "")
    schema_path = os.getenv('SCHEMA')
    users_path = os.getenv('USERS')
    initialize_database(db_path, schema_path)
    insert_users_from_json(db_path, users_path)
