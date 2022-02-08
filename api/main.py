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

versions='Working on Vercel.com \n CIRC-SheduleManager\n(beta1.1)'
Flax=Flax()
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handle = WebhookHandler(LINE_CHANNEL_SECRET)
Friends = friend()
Schedule  =Schedular()

app = Flask(__name__)

#部分テスト用
@app.route('/test')
def test():
    Schedule.organize()
    print(Schedule.data)
    return'OK',200

#月移行動作
@app.route("/nextmonth",methods=['POST'])
def month():
    friend=Friends.LIST()
    #友達それぞれに対して
    for username in friend:
        #JSONのDICを作成して
        JSON_DIC=Flax.DICT(username)
        #Flaxメッセージに変えて
        container_obj = FlexSendMessage(alt_text='今月の日程を入力してください',contents=JSON_DIC)
        #プッシュメッセージを送信
        line_bot_api.push_message(username, messages=container_obj)
    return 'OK',200

#日々の確認
@app.route("/checkdate",methods=['POST'])
def checker():
    current_dt=datetime.datetime.now()+datetime.timedelta(days=7)
    str = current_dt.strftime('%Y/%m/%d')
    no = count_part(str)
    if int(no)>2:
        message=''+str+'に'+no+'人が参加可能です'
        line_bot_api.push_message(username, messages=message)

    return 'OK',200

#日程アンケート
@app.route("/questionaire")
def question():
    #UIDのクエリ引数を取る
    req = request.args
    req_user_id = req.get("UID")
    if req_user_id==None:
        abort(401)
    ret_data = Schedule.Schedule_list(req_user_id)
    return render_template('questionaire.html', userdata = ret_data)

#アンケート受付
@app.route("/postdata",methods=['POST'])
def post():
    data = request.data
    data = json.loads(data)
    print(data['name'])
    print(data['UID'])
    print(data['data'])
    data['data'].insert(0,data['name'])
    print(data['data'])
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
    return render_template('participants.html',data=Schedule.All_lists()),200

#APIに応答
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    #Webhook bodyをハンドル
    try:
        handle.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

#メッセージが送られたら
@handle.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text=='version':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=versions))

#フォローEvent
@handle.add(FollowEvent)
def handle_follow(event):
    Friends.add(event.source.user_id)
    JSON_DIC=Flax.DIC(event.source.user_id)
    #Flaxメッセージに変えて
    container_obj = FlexSendMessage(alt_text='今月の日程を入力してください',contents=JSON_DIC)
    #プッシュメッセージを送信
    line_bot_api.push_message(event.source.user_id, messages=container_obj)

#フォロー解除Event
@handle.add(UnfollowEvent)
def handle_unfollow(event):
    Friends.remove(event.source.user_id)
print("2")
#if __name__ == "__main__":
#app.run(host='0.0.0.0',debug=False)
