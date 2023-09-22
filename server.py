import os
import json
import logging

from flask import Flask, request, make_response, Response
from dotenv import load_dotenv
import pandas as pd

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

from slashCommand import Slash
from sentiment_analyzer import analyze_sentiment

from predict_score import predict_score
from utils import clean_post

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route("/slack/test", methods=["POST"])
def command():
  # if not verifier.is_valid_request(request.get_data(), request.headers):
  #   return make_response("invalid request", 403)
  info = request.form

  # # send user a response via DM
  # im_id = slack_client.im_open(user=info["user_id"])["channel"]["id"]
  # ownerMsg = slack_client.chat_postMessage(
  #   channel=im_id,
  #   text=commander.getMessage()
  # )

  # # send channel a response
  # response = slack_client.chat_postMessage(
  #   channel='#{}'.format(info["channel_name"]), 
  #   text=commander.getMessage()
  # )

  try:
    response = slack_client.chat_postMessage(
      channel='#{}'.format(info["channel_name"]), 
      text=commander.getMessage()
    )#.get()
  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)
    return make_response("", e.response.status_code)

  return make_response("", response.status_code)

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
  SLACK_SIGNATURE = os.environ['SLACK_SIGNATURE']
  slack_client = WebClient(SLACK_BOT_TOKEN)
  verifier = SignatureVerifier(SLACK_SIGNATURE)

  commander = Slash("Hey there! It works.")

  app.run()