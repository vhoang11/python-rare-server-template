import sqlite3
import json
from datetime import datetime

def create_post(new_post):
    """Adds a post to the database

    Args:
        post (dictionary): The dictionary passed to the create post request

    Returns:
        json string: Contains the token of the newly created post
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Posts (title, publication_date, image_url, content, approved) values (?, ?, ?, ?, 1)
        """, (
            new_post['title'],
            datetime.now(),
            new_post['image_url'],
            new_post['content']
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })
