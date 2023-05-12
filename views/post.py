import sqlite3
import json
from datetime import datetime
from models import Posts

def create_post(new_post):
    """Adds a post to the database
    Args: post (dictionary): The dictionary passed to the create post request
    Returns: json string: Contains the token of the newly created post
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved) VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (
            new_post['user_id'],
            new_post['category_id'],
            new_post['title'],
            datetime.now(),
            new_post['image_url'],
            new_post['content']
        ))

        id = db_cursor.lastrowid
        
        new_post['id'] = id

        return new_post

def get_all_posts():
    """get those posts or your code is toast
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved 
        
        FROM Posts p   
        """)
        
        # Initialize an empty list to hold all post representations
        posts = []
        
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Post class above.
            post = Posts(row['id'], row['user_id'], row['category_id'],
            row['title'], row['publication_date'], row['image_url'],row['content'],row['approved'])

            posts.append(post.__dict__) # see the notes below for an explanation on this line of code.
    return posts
  
def delete_post(id):
    """Let's get rid of that post!
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))
        
def update_post(id, new_post):
    """Faking my own death just to get some rest
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?             
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved'], id, ))
        
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True
