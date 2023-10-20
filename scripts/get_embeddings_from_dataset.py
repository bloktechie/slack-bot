import os
import pandas as pd
import tiktoken

import openai
from openai.embeddings_utils import get_embedding
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000

input_datapath = "data/posts.csv"  # to save space, we provide a pre-filtered dataset
df = pd.read_csv(input_datapath)
df = df[["content", "score", "project", "source"]]
df = df.dropna()

df["project"] = df["project"].str.lower()
df["source"] = df["source"].str.lower()

encoding = tiktoken.get_encoding(embedding_encoding)

df["n_tokens"] = df.content.apply(lambda x: len(encoding.encode(x)))
df = df[df.n_tokens <= max_tokens]

df["embedding"] = df.content.apply(lambda x: get_embedding(x, engine=embedding_model))

df.to_csv("data/posts_with_embeddings.csv")
