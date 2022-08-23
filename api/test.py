#Flask
from flask import Flask, request, abort,render_template
from flask_httpauth import HTTPBasicAuth
#LINEAPI関連
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent,UnfollowEvent, TextMessage, TextSendMessage,FlexSendMessage,MemberJoinedEvent
#その他のライブラリ
import os
import json
import datetime
import requests
import re
#環境変数取得

#オブジェクトの生成
app = Flask(__name__)
auth = HTTPBasicAuth()

#パスワード判定

#日程アンケート
@app.route("/questionaire")
def question():

    ret_data = []
    return render_template('questionaire.html', userdata = ret_data)

#アンケート受付
@app.route("/postdata",methods=['POST'])
def post():
    data = request.data
    data = json.loads(data)
    data['data'].insert(0,data['name'])
    Schedule.add(data['UID'],data['data'])
    Schedule.save()
    return "Accepted",202

#日程送信完了
@app.route('/end')
def end():
    return render_template('end.html'),200
#参加者一覧
@app.route('/participants')
def part():
    res = requests.get("https://weather.tsukumijima.net/api/forecast/city/080010")
    json_data = res.json()
    forecast_data = [json_data["forecasts"][i]["image"]["url"] for i in range(0,3,1)]
    return render_template('participants.html',data={"2022/12/22":["宮坂","伊藤","石井","スズキ"],"2022/12/23":[],"2022/12/24":["宮坂","伊藤","石井","スズキ","骨川"],"2022/12/25":["宮坂","伊藤","石井","スズキ"]},forecast_data = forecast_data,news_str="「ニュース」hogehagehigehogehagehige"),200

#APIに応答

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
