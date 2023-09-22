import numpy as np
import joblib

from openai.embeddings_utils import get_embedding

embedding_model = "text-embedding-ada-002"

model = joblib.load('data/posts_model.pkl')

def predict_score(text: str) -> int:
  embedding =get_embedding(text, engine=embedding_model)
  return int(model.predict([embedding])[0])
