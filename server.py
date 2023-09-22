import os
import logging
import sys

from flask import Flask, request, make_response
from dotenv import load_dotenv
import pandas as pd

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from predict_score import predict_score
from utils import clean_post

load_dotenv()

log_location = os.path.abspath(os.path.join("root", "logfile.log"))
FORMAT = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%m/%d/%Y %H:%M:%S', handlers=[
        logging.FileHandler(log_location),
        logging.StreamHandler(sys.stdout)])
logging.info("Testing the logger...")

app = Flask(__name__)

@app.route("/slack/message", methods=["POST"])
def handle_message():
  json  = request.json

  if json["type"] == "url_verification":
    response = make_response(json["challenge"])
    response.mimetype = "text/plain"
    return response
  
  if not "event" in json:
    return make_response("invalid request", 500)
  
  event = json["event"]

  if not "text" in event:
    return make_response("invalid request", 500)
  
  # only check project news channel
  if event["channel"] != "C05RPB8UJBF":
    return make_response("wrong channel", 403)
  
  # do not check thread message
  if "thread_ts" in event:
    return make_response("wrong message type", 403)
  
  score = predict_score(clean_post(event["text"]))
  if score < 1:
    return make_response("not important news")

  try:
    response = slack_client.chat_postMessage(
      channel=os.environ['SLACK_CHANNEL_NAME'], 
      text="🚨 " * score + event["text"]
    )#.get()

  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)
    return make_response("", e.response.status_code)
  
  return make_response("")

# Start the Flask server
if __name__ == "__main__":
  SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
  slack_client = WebClient(SLACK_BOT_TOKEN)

  app.run()