import sqlite3
import json
from datetime import datetime
from models import Subscriptions

def create_postreaction(new_postreaction):
    """Adds a post to the database
    Args: post (dictionary): The dictionary passed to the create post request
    Returns: json string: Contains the token of the newly created post
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostReactions (user_id, reaction_id, post_id) VALUES (?, ?, ?)
        """, (
            new_postreaction['user_id'],
            new_postreaction['reaction_id'],
            new_postreaction['post_id']
            
        ))

        id = db_cursor.lastrowid
        
        new_postreaction['id'] = id

        return new_postreaction

def get_all_postreactions():
    """get those posts or your code is toast
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.reaction_id,
            p.post_id 
        
        FROM PostReactions p   
        """)
        
        # Initialize an empty list to hold all post representations
        postreactions = []
        
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            postreaction = Subscriptions(row['id'], row['user_id'], row['reaction_id'],
            row['post_id'])

            postreactions.append(postreaction.__dict__) # see the notes below for an explanation on this line of code.
    return postreactions
  
def delete_postreactions(id):
    """Let's get rid of that post!
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM PostReactions
        WHERE id = ?
        """, (id, ))
