import bcrypt
import psycopg2

from app.database import get_connection
from deepface import DeepFace
import json

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
            "user_id": user_id,
            "username": username,
            "email": email,
            "role": role
        }
    
    return None

def addModel(name, path, user_id):
    con = get_connection()
    cursor = con.cursor()

    query = """
    INSERT INTO models (name, path, user_id)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, path, user_id))
    con.commit()

    cursor.close()
    con.close()

def getModels(user_id):
    con = get_connection()
    cursor = con.cursor()

    query = """
    SELECT name, path
    FROM models
    WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))
    models = cursor.fetchall()

    cursor.close()
    con.close()

    return models

def addUser(name, email, password, image_path, model_name="Facenet"):
    con = get_connection()
    cursor = con.cursor()

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    embedding = DeepFace.represent(
        img_path=image_path,
        model_name=model_name,
        enforce_detection=True
    )[0]["embedding"]
    
    embedding_json = json.dumps(embedding)

    query = """
        INSERT INTO users (name, email, password_hash, embedding)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (name, email, password_hash, embedding_json))
    con.commit()

    cursor.close()
    con.close()

def getAllEmbeddings():
    con = get_connection()
    cursor = con.cursor()

    query = "SELECT username embedding FROM users WHERE embedding IS NOT NULL"

    rows = cursor.fetchall()

    cursor.close()
    con.close()

    db_embeddings = {}
    for username, emb in rows:
        db_embeddings[username] = json.loads(emb)

    return db_embeddings