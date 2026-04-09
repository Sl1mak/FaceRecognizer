import bcrypt
import psycopg2

from app.database import get_connection

def login(l_input, p_input):
    con = get_connection()
    cursor = con.cursor()

    query = """
    SELECT id, username, email, password_hash, role
    FROM users
    WHERE username = %s OR email = %s
    """

    cursor.execute(query, (l_input, l_input))
    user = cursor.fetchone()

    cursor.close()
    con.close()

    if not user:
        return None

    user_id, username, email, password_hash, role = user

    if bcrypt.checkpw(p_input.encode(), password_hash.encode()):
        return {
            "user_id": id,
            "username": username,
            "email": email,
            "role": role
        }
    
    return None
