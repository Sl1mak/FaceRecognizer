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
    SELECT name
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

    import bcrypt
    import json
    from deepface import DeepFace

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, email, password_hash))

    user_id = cursor.fetchone()[0]

    try:
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name=model_name,
            enforce_detection=True
        )[0]["embedding"]
    except Exception:
        raise ValueError("No face detected in the image")

    try:
        cursor.execute("""
            INSERT INTO face_embeddings (user_id, embedding, model_name)
            VALUES (%s, %s, %s)
        """, (user_id, json.dumps(embedding), model_name))
    except Exception:
        raise ValueError("Failed to extract embedding from the image")

    con.commit()
    cursor.close()
    con.close()

def getAllEmbeddings(model_name="Facenet"):
    con = get_connection()
    cursor = con.cursor()

    query = """
    SELECT u.username, f.embedding
    FROM face_embeddings f
    JOIN users u ON u.id = f.user_id
    WHERE f.model_name = %s
    """

    cursor.execute(query, (model_name,))
    rows = cursor.fetchall()

    cursor.close()
    con.close()

    db_embeddings = {}
    for username, emb in rows:
        db_embeddings[username] = emb  # jsonb → уже list

    return db_embeddings