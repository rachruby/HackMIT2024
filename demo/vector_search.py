import os
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
import pandas as pd


username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972' 
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
engine = create_engine(CONNECTION_STRING)

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_database():
    with engine.connect() as conn:
        with conn.begin():# Load 
            sql = f"""
                    CREATE TABLE UserReviews7 (
        id INT PRIMARY KEY AUTO_INCREMENT,
        description TEXT,
        video TEXT,
        description_vector VECTOR(DOUBLE, 384)
    )
                    """
            result = conn.execute(text(sql))

def insert_data(video_path, description):
    # video_path = "../data/test.mov"
    # description = "a video taken at hackMIT for fun"
    single_embedding =model.encode(description, normalize_embeddings=True).tolist()
    print(single_embedding)
    with engine.connect() as conn:
        with conn.begin():# Load 
            sql = """
                    INSERT INTO UserReviews7
                    (description, video,  description_vector)
                    VALUES (:description, :video, TO_VECTOR(:description_vector))
                """
            conn.execute(
                text(sql),
                {"description": description, "video": video_path, "description_vector": str(single_embedding)}
            )
            print("Row inserted successfully.")

def vector_search(description_search):
    # description_search = "hackMIT"
    search_vector = model.encode(description_search, normalize_embeddings=True).tolist() # Convert search phrase into a vector

    with engine.connect() as conn:
        with conn.begin():
            sql = text("""
                SELECT TOP 1 * FROM UserReviews7
                ORDER BY VECTOR_DOT_PRODUCT(description_vector, TO_VECTOR(:search_vector)) DESC
            """)

            results = conn.execute(sql, {'search_vector': str(search_vector)}).fetchall()
            print(results)

    return results