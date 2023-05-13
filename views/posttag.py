import sqlite3
import json
from models import PostTags

def create_posttag(new_posttag):
    """Could I be that guy in terms of movies"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO PostTags ( post_id, tag_id ) 
        VALUES (?, ?)                  
        """, (new_posttag['post_id'], new_posttag['tag_id']))
        
        id = db_cursor.lastrowid
        
        new_posttag['id'] = id
        
        return json.dumps(new_posttag)
      
def get_all_posttags():
    """The rain knows what he's doing"""
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id
            
        FROM PostTags pt
        JOIN posts p
            ON p.id = pt.post_id
        JOIN tags t
            ON t.id = pt.tag_id                  
        """)
        
        posttags = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            posttag = PostTags(row['id'], row['post_id'], row['tag_id'])
          
            posttags.append(posttag.__dict__)
            
        return posttags
      
def delete_posttag(id):
    """Tag Team back again check it correct it let's begin"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE FROM posttags
        WHERE id = ?                  
        """, (id, ))
  
def update_posttag(id, new_posttag):
    """Trap Sabbath"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE PostTags
            SET
                post_id = ?,
                tag_id = ?
        WHERE id = ?              
        """, (new_posttag['post_id'], new_posttag['tag_id'], id, ))
        
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else: 
        return True
     
            
