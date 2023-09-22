import re

def clean_post(text: str) -> str:
  res ="\n".join(text.split('\n')[1:])
  res = re.sub(r'http\S+', '', res)
  return res
