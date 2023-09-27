import json

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

PROMPT_TEMPLATE = """"
You are a cryptocurrency trader with 10+ years of experience.
You always follow trend and deeply understand crypto projects on Twitter and Discord.
You always consider historical announcements for each project on Twitter and Discord.

You're given an announcement message from Twitter or Discord.

{message}

Tell us how important the announcement is for that project. Use numbers between 0 and 10, where 0 is least important
and 10 is extremely important.

Return just integer. Do not explain
"""

def analyze_sentiment(message: str) -> int:
  chat_gpt = ChatOpenAI(temperature=0)
  prompt = PromptTemplate(
    input_variables=["message"], template=PROMPT_TEMPLATE
  )
  sentiment_chain = LLMChain(llm=chat_gpt, prompt=prompt)
  response = sentiment_chain(
    {
      "message": message
    }
  )
  return json.loads(response["text"])