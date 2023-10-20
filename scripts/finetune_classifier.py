import os

import pandas as pd
import numpy as np

import openai
import joblib
import tiktoken

from openai.embeddings_utils import get_embedding
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000

encoding = tiktoken.get_encoding(embedding_encoding)

input_datapath = "../posts.json"  # to save space, we provide a pre-filtered dataset
df = pd.read_json(input_datapath)
df = df[["content", "score"]]
df = df.dropna()

df["n_tokens"] = df.content.apply(lambda x: len(encoding.encode(x)))
df = df[df.n_tokens <= max_tokens]

df["embedding"] = df.content.apply(lambda x: get_embedding(x, engine=embedding_model))

# df["embedding"] = df.embedding.apply(literal_eval).apply(np.array)

clf = joblib.load("data/posts_model.pkl")

clf.partial_fit(list(df.embedding.values), df.score, classes=np.unique(df.score))

joblib.dump(clf, "data/posts_model.pkl", compress=9)
