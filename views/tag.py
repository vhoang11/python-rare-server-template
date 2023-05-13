import sqlite3
import json
from models import Tags

def create_tag(new_tag):
    """Tag, you're it!"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags (label)
        VALUES (?)
        """, (new_tag['label'],))

        id = db_cursor.lastrowid

        new_tag['id'] = id

        return new_tag
      
def get_all_tags():
    """Pinkerton is a great album
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
          
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
              
        FROM Tags t              
        """)
                
        tags = []
          
        dataset = db_cursor.fetchall()
          
        for row in dataset:
            tag = Tags(row['id'], row['label'])
              
            tags.append(tag.__dict__)
        return tags
      
def delete_tag(id):
    """Tag you're not it!"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM tags
        WHERE id = ?                     
        """, (id, ))
        
def update_tag(id, new_tag):
    """We were good as married in my mind, but married in my mind's no good
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?               
        """, (new_tag['label'], id, ))
        
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True
