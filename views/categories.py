import sqlite3
import json
from datetime import datetime
from models import Categories

def create_category(new_category):
    """Adds a category to the database
    Args: category (dictionary): The dictionary passed to the create category request
    Returns: json string: Contains the token of the newly created category
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories (label) VALUES (?)
        """, (
            new_category['label'],
        ))

        id = db_cursor.lastrowid
        
        new_category['id'] = id

        return new_category

def get_all_categories():
    """get those categories or your code is toast
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c   
        """)
        
        # Initialize an empty list to hold all category representations
        categories = []
        
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a category instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # category class above.
            category = Categories(row['id'], row['label'])

            categories.append(category.__dict__) # see the notes below for an explanation on this line of code.
    return categories
  
def delete_category(id):
    """Let's get rid of that category!
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
        """, (id, ))
