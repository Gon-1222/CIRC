from flask import Flask, request, abort,render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent,UnfollowEvent, TextMessage, TextSendMessage,FlexSendMessage
from Friends import friend
from scheduler import Schedular
from Flax import Flax
import os
import json
import datetime
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

versions='beta1'
Flax=Flax()
#line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
h#andler = WebhookHandler(LINE_CHANNEL_SECRET)
Friends = friend()
Schedule  =Schedular()

app = Flask(__name__)
