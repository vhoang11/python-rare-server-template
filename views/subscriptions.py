import sqlite3
import json
from datetime import datetime
from models import Subscriptions

def create_subscription(new_subscription):
    """Adds a post to the database
    Args: post (dictionary): The dictionary passed to the create post request
    Returns: json string: Contains the token of the newly created post
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscriptions (follower_id, author_id, created_on) VALUES (?, ?, ?)
        """, (
            new_subscription['follower_id'],
            new_subscription['author_id'],
            datetime.now()
            
        ))

        id = db_cursor.lastrowid
        
        new_subscription['id'] = id

        return new_subscription

def get_all_subscriptions():
    """get those posts or your code is toast
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on 
        
        FROM Subscriptions s   
        """)
        
        # Initialize an empty list to hold all post representations
        subscriptions = []
        
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            subscription = Subscriptions(row['id'], row['follower_id'], row['author_id'],
            row['created_on'])

            subscriptions.append(subscription.__dict__) # see the notes below for an explanation on this line of code.
    return subscriptions
  
def delete_post(id):
    """Let's get rid of that post!
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))
