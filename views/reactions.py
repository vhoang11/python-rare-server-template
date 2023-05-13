import sqlite3
import json
from datetime import datetime
from models import Reactions

def create_reaction(new_reaction):
    """Adds a post to the database
    Args: post (dictionary): The dictionary passed to the create post request
    Returns: json string: Contains the token of the newly created post
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Reactions (label, image_url) VALUES (?, ?)
        """, (
            new_reaction['label'],
            new_reaction['image_url']
            
        ))

        id = db_cursor.lastrowid
        
        new_reaction['id'] = id

        return new_reaction

def get_all_reactions():
    """get those posts or your code is toast
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            r.id,
            r.label,
            r.image_url
            
        
        FROM Reactions r   
        """)
        
        # Initialize an empty list to hold all post representations
        reactions = []
        
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            reaction = Reactions(row['id'], row['label'], row['image_url']
            )

            reactions.append(reaction.__dict__) # see the notes below for an explanation on this line of code.
    return reactions
  
def delete_reactions(id):
    """Let's get rid of that reaction!
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Reactions
        WHERE id = ?
        """, (id, ))
