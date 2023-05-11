import sqlite3
import json
from datetime import datetime
from models import Users

def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, bio,profile_image_url, created_on, active) values (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['password'],
            user['bio'],
            user['profile_image_url'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })
        #HEAD:views/user_request.py

def update_user(id, new_user):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE user
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                user_id = ?
        WHERE id = ?
        """, (new_user['name'], new_user['breed'],
              new_user['status'], new_user['locationId'],
              new_user['userId'], id, ))

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

def get_all_users():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.first_name,
            a.last_name,
            a.email,
            a.bio,
            a.username,
            a.password,
            a.profile_image_url,
            a.created_on,
            a.active
            
        FROM Users a
        """)

        # Initialize an empty list to hold all user representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an user instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # user class above.
            user = Users(row['id'], row['first_name'], row['last_name'],
                            row['email'], row['bio'],
                            row['username'],row['password'],row['profile_image_url'],row['created_on'],
                            row['active'])

            users.append(user.__dict__) # see the notes below for an explanation on this line of code.

    return users

<<<<<<< HEAD
def delete_user(id):
=======
def update_user(id, new_user):
>>>>>>> main
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
<<<<<<< HEAD
        DELETE FROM Users
        WHERE id = ?
        """, (id, ))
=======
        UPDATE Users
            SET
                first_name = ?,
                last_name = ?,
                email = ?,
                bio = ?,
                username = ?,
                password = ?,
                profile_image_url = ?,
                created_on = ?,
                active = ?
        WHERE id = ?
        """, (new_user['first_name'], new_user['last_name'], new_user['email'], new_user['bio'], 
              new_user['username'], new_user['password'], new_user['profile_image_url'], 
              new_user['created_on'], new_user['active'], id, ))

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
>>>>>>> main
