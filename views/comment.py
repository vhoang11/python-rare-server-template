import sqlite3
import json
from models import Comments

def create_comment(new_comment):
    """Adds a comment to the database
    Args: comment (dictionary): The dictionary passed to the create comment request
    Returns: json string: Contains the token of the newly created comment
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments (author_id, post_id, content) VALUES (?, ?, ?)
        """, (
            new_comment['author_id'],
            new_comment['post_id'],
            new_comment['content']
        ))

        id = db_cursor.lastrowid

        new_comment['id'] = id

        return new_comment

def get_all_comments():
    """get those comments or your code is toast
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content
        FROM comments c   
        """)
        
        # Initialize an empty list to hold all comment representations
        comments = []
        
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a comment instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # comment class above.
            comment = Comments(row['id'], row['author_id'], row['post_id'], row['content'])

            comments.append(comment.__dict__) # see the notes below for an explanation on this line of code.
    return comments

def update_comment(id, new_comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Comments
            SET
              	author_id = ?,
            	post_id = ?,
            	content = ?
        WHERE id = ?
        """, (new_comment['author_id'], 
              new_comment['post_id'],
              new_comment['content'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
    
def delete_comment(id):
    """Let's get rid of that comment!
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))
