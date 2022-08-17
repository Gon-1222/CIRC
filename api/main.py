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
#自作ライブラリ
from Friends import friend
from scheduler import Schedular
from Flax import Flax
from notification import notify
from history import History
from manager import Manager
from permission import permit
#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
Group_ID=os.environ["LINE_MAIN_GROUP_ID"]
versions='RC11 2022/08/10'

#オブジェクトの生成
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handle = WebhookHandler(LINE_CHANNEL_SECRET)
Flax=Flax()
Friends = friend()
Schedule  =Schedular()
Notify = notify()
app = Flask(__name__)
auth = HTTPBasicAuth()

#パスワード判定
@auth.verify_password
def verify_password(username, password):
    permission=permit(1)
    return permission.check(username, password)
#ルートアクセス時
@app.route('/')
def root_pages():
    return "ここにはなにもないよ",404
#マネージメントページ
@app.route('/management',methods=['post'])
@auth.login_required
def managers():
    mana=Manager().read()
    Friends_data=list(set(Friends.member)-set(mana))
    for i in Friends_data:
        profile = line_bot_api.get_profile(i)
        Members_data=[]
        Members_data.append([profile,i])
    for j in mana:
                profile = line_bot_api.get_profile(i)
                Mana_data=[]
                Mana_data.append([profile,i])
    Now_manage,Now_req=permit().User_lists
    return render_template('management.html',Mana_data=Mana_data,Members_data=Members_data,Now_manage=Now_manage,Now_req=Now_req,Version=versions)
#マネージメントのインターフェイス
@app.route('/management',methods=['post'])
@auth.login_required
def posts_data():
    #エラー（タイプが無かったとき）
    if request.form.get('data_type', None):
        return 'Forbidden', 403
    #Historyに追加
    if request.form.get('data_type',None)=="Add_history":
        string=request.form.get('Add_date',None).replace("-","/")
        if re.fullmatch(r"^\d{4}/\d{2}/\d{1,2}$",string):
            History().Add(string)
        else:
            return "正規表現不一致",400
    #Historyから削除
    if request.form.get('data_type',None)=="Del_history":
        string=request.form.get('Add_date',None).replace("-","/")
        if re.fullmatch(r"^\d{4}/\d{2}/\d{1,2}$",string):
            History().Del(string)
        else:
            return "正規表現不一致",400
    #ブロードキャスト
    if request.form.get('data_type',None)=="broad_cast":
        if request.form.get('message',None)!="":
            messages = TextSendMessage(text=request.form.get('message',None))
            line_bot_api.broadcast(messages=messages)
    if request.form.get('data_type',None)=="del_mana":
        if request.form.get('delete',None)!="":
            permit().Del(request.form.get('delete',None))
    if request.form.get('data_type',None)=="permit_mana":
        if request.form.get('permit',None)!="":
            permit().Allow(request.form.get('permit',None))

    return "OK",200
#ブロードキャスト!非推奨・基本は使用禁止
@app.route("/broadcastpost",methods=['POST'])
def broad():
    data = request.data
    data = json.loads(data)
    #トークンは本当はenvironへ
    if data["pass"]!="%L5q3C)(dP-3(h%uwn,L":
        abort(403)
    print(data["message"])
    messages = TextSendMessage(text=data["message"])
    #line_bot_api.broadcast(messages=messages)!!!Don't Available
    #return 'OK',200
    return 'Forbidden', 403

#月移行動作
@app.route("/nextmonth",methods=['GET'])
def month():
    friend=Friends.LIST()
    #友達それぞれに対して
    for username in friend:
        #JSONのDICを作成して
        JSON_DIC=Flax.DIC(username)
        #Flaxメッセージに変えて
        container_obj = FlexSendMessage(alt_text='今月の日程を入力してください',contents=JSON_DIC)
        #プッシュメッセージを送信
        line_bot_api.push_message(username, messages=container_obj)
    return 'OK',200

#日々の確認
@app.route("/checkdate",methods=['POST'])
def checker():
    #----------------------------------------
    #1週間以内にライドが計画されているかの確認
    #----------------------------------------
    for i in range(1,8,1):
        current_dt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))+datetime.timedelta(days=i)#現日付+1~8日
        string = current_dt.strftime('%Y/%m/%d')#現日付+1~8日の文字列
        no = Schedule.count_part(string)#参加可能メンバーの人数が
        #3人以上で且つ通知をしていなかったら
        if int(no)>2 and not(string in Notify.data):
                #通知履歴の追加と保存
                Notify.Add(string)
                Notify.save()
                #HP用ホームページの追加
                History().Add(string)
                #メッセージの生成
                message=''+string+'に'+str(no)+'人が参加可能です'
                #送信！
                line_bot_api.push_message(Group_ID, TextSendMessage(text=message))
                print("通知完了")
    #----------------------------------------
    #しばらくライドが行われなかったとき
    #----------------------------------------
    if (Notify.data!=[]):
        #現日付
        current_dt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        #最後の通知日をdatetimeオブジェクトに変形して
        buf = datetime.datetime.strptime(Notify.data[-1],'%Y/%m/%d')
        #タイムゾーンつけて
        buf = buf.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
        #時間差を得て
        dt=current_dt-buf
        print("前回の通知からの日数:",dt.days)
        #前回の計画から30日計画されていいなかったら
        if (dt.days==30):
            message="3人以上参加可能な日が30日間ありませんでした。\nそろそろライドを計画しませんか？"
            line_bot_api.push_message(Group_ID, TextSendMessage(text=message))
            print("しばらくライドが行われなかった。")
    #----------------------------------------
    #メール転送
    #----------------------------------------
    #POSTの中身があるときだけ
    if request.data.decode():
        query = json.loads(request.data.decode())
        #通知すべきメールがあるとき
        if query!=[]:
            #メッセージリストの作成
            send_list=[]
            text="[メール通知]"
            send_list.append(TextSendMessage(text=text))
            for i in query:
                text=("<"+i["title"]+">\n"+i["body"])
                send_list.append(TextSendMessage(text=text))
            #メッセージをマネージャーに送信
            manage=Manager()
            for i in manage.read():
                line_bot_api.push_message(i, send_list)
    else:
        #POSTの中身がないとき
        abort(403)
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
    res = requests.get("https://weather.tsukumijima.net/api/forecast/city/080010")
    json_data = res.json()
    forecast_data = [json_data["forecasts"][i]["image"]["url"] for i in range(0,3,1)]
    return render_template('participants.html',data=Schedule.All_lists(),forecast_data = forecast_data),200

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
    if event.message.text=='Members':
        message="メンバー一覧:"
        for i in Friends.member:
            print(i)
            profile = line_bot_api.get_profile(i)
            message+='\n'
            message+=profile.display_name
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))

    if event.message.text=='明日の天気':
        res=requests.get("https://weather.tsukumijima.net/api/forecast/city/080010")
        data=res.json()
        message="【明日の天気】\n天気:"+data["forecasts"][1]["telop"]+"\n最低気温:"+data["forecasts"][1]["temperature"]["min"]["celsius"]+"℃\n最高気温:"+data["forecasts"][1]["temperature"]["max"]["celsius"]+"℃\n\n降水確率\n"+" 0~6時:"+data["forecasts"][1]['chanceOfRain']["T00_06"]+"\n 6~12時:"+data["forecasts"][1]['chanceOfRain']["T06_12"]+"\n 12~18時:"+data["forecasts"][1]['chanceOfRain']["T12_18"]+"\n 18~24時:"+data["forecasts"][1]['chanceOfRain']["T18_24"]

        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    return
#フォローEvent
@handle.add(FollowEvent)
def handle_follow(event):
    Friends.add(event.source.user_id)
    Friends.save()
    JSON_DIC=Flax.DIC(event.source.user_id)
    #Flaxメッセージに変えて
    container_obj = FlexSendMessage(alt_text='ご参加ありがとうございます。',contents=JSON_DIC)
    container_obj2 = FlexSendMessage(alt_text='ご参加ありがとうございます。',contents=Flax.DIC3())
    #プッシュメッセージを送信(リプライのほうがよくね)
    line_bot_api.reply_message(event.reply_token, [container_obj,container_obj2])
    return
#新たに参加した方
@handle.add(MemberJoinedEvent)
def handle_joined(event):
    message2="サークルの共有事項等は、ノートに記載しておりますので、ご確認ください。"
    JSON_DIC=Flax.DIC2()
    #Flaxメッセージに変えて
    container_obj = FlexSendMessage(alt_text='ご参加ありがとうございます。',contents=JSON_DIC)
    #プッシュメッセージを送信
    line_bot_api.reply_message(event.reply_token,[container_obj,TextSendMessage(text=message2)])
    return

#フォロー解除Event
@handle.add(UnfollowEvent)
def handle_unfollow(event):
    Friends.remove(event.source.user_id)
    return
print("main.py is Loaded...")

#if __name__ == "__main__":
#app.run(host='0.0.0.0',debug=False)
