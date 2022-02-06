from flask import Flask, request, abort,render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent,UnfollowEvent, TextMessage, TextSendMessage,FlexSendMessage
#from Friends import friend
#from scheduler import Schedular
#from Flax import Flax
import os
import json
import datetime
#CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
CHANNEL_ACCESS_TOKEN = "MlucX+/V3K9iTyDzXC3fYy/hGk6C0yv8BCdW49CyIDop+yzBUt7LU2n391vdeeoJ2GU+8sEnJy1RDlxNos+ftio20+Kb8Dzxgx78a1fVoifggtwC4DOA8tGo/0Kt/8UNFc7AHMi1gOYs7d23lRU3yQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "98cec7c460c13c1d7a211c12b37c0f2c"

versions='beta1'
#Flax=Flax()
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
#handler = WebhookHandler(LINE_CHANNEL_SECRET)
#Friends = friend()
#Schedule  =Schedular()

app = Flask(__name__)
@app.route('/')
def f():
    return "OK"
