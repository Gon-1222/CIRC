from flask import Flask, request, abort,render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent,UnfollowEvent, TextMessage, TextSendMessage,FlexSendMessage
import os
import json
import datetime
from Friends import friend
from scheduler import Schedular
from Flax import Flax
from notification import notify

#環境変数
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
Group_ID=os.environ["LINE_MAIN_GROUP_ID"]
versions='Beta3.0\n2022/02/10'

#オブジェクトの生成
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handle = WebhookHandler(LINE_CHANNEL_SECRET)
Flax=Flax()
Friends = friend()
Schedule  =Schedular()
Notify = notify()
app = Flask(__name__)

#部分テスト用
@app.route('/test')
def test():
    Schedule.organize()
    print(Schedule.data)
    return'OK',200

#月移行動作
@app.route("/nextmonth",methods=['GET'])
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
@app.route("/checkdate",methods=['GET'])
def checker():
    for i in range(1,8,1):
        current_dt=datetime.datetime.now()+datetime.timedelta(days=i)
        string = current_dt.strftime('%Y/%m/%d')
        no = Schedule.count_part(string)
        Notify.Clean_Up()
        if int(no)>2:
            print("OK1")
            if not(string in Notify.data):
                print("OK2")
                Notify.Add(string)
                message=''+string+'に'+str(no)+'人が参加可能です'
                line_bot_api.push_message(Group_ID, TextSendMessage(text=message))

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
    Friends.save()
    JSON_DIC=Flax.DIC(event.source.user_id)
    #Flaxメッセージに変えて
    container_obj = FlexSendMessage(alt_text='今月の日程を入力してください',contents=JSON_DIC)
    #プッシュメッセージを送信(リプライのほうがよくね)
    line_bot_api.push_message(event.source.user_id, messages=container_obj)

#フォロー解除Event
@handle.add(UnfollowEvent)
def handle_unfollow(event):
    Friends.remove(event.source.user_id)
print("main.py is Loaded...")

#if __name__ == "__main__":
#app.run(host='0.0.0.0',debug=False)
