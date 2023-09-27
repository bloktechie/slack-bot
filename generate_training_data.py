import json

import pandas as pd

df = pd.read_csv('./examples_raw.csv', sep=',')
df = df[['content', 'score', 'project', 'source']]
df = df.dropna()

data = []
for index,row in df.iterrows():
  data.append({
    "text": row["content"],
    "label": str(int(row["score"])),
    "meta": {
      "project": row["project"].lower(),
      "source": row["source"].lower()
    }
  })

with open('train.jsonl', 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False, indent=4)