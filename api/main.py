#------------------------------------------
#県央RC-BOT Ver 1.0
#Published 08/29/2022
#Presented by Gon-1222
#------------------------------------------
# Flask
from flask import Flask, request, abort, render_template
from flask_httpauth import HTTPBasicAuth
# LINEAPI関連
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, UnfollowEvent, TextMessage, TextSendMessage, FlexSendMessage, MemberJoinedEvent
# その他のライブラリ
import os
import json
import datetime
import requests
import re
import time
# 自作ライブラリ
from Friends import friend
from scheduler import Schedular
from Flax import Flax
from notification import notify
from history import History
from manager import Manager
from permission import permit
from news import News
from lazy import Lazy
from All_data import All_Data

# 環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
Group_ID = os.environ["LINE_MAIN_GROUP_ID"]
versions = 'Ver 1.0-a　2022/09/03 \n a:Activity reduction prevention alerts have been changed. '


# オブジェクトの生成
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handle = WebhookHandler(LINE_CHANNEL_SECRET)
app = Flask(__name__)
auth = HTTPBasicAuth()
file_data = All_Data()
# パスワード判定
@auth.verify_password
def verify_password(username, password):
    permission = permit(1,file_data.data)
    return permission.Check(username, password)

# ルートアクセス時
@app.route('/')
def root_pages():
    #Friends = friend(file_data.data["Friends"])
    #Friends.RESET()
    #file_data.save_file()
    print("aa")
    return "ここにはなにもないよ", 404

# Robots.txt
@app.route('/robots.txt')
def robots_pages():
    return app.send_static_file('robots.txt'), 200
# 更新履歴
@app.route('/whatsnew')
def whatsnew_pages():
    return app.send_static_file('Whatsnew.html'), 200



#############################################
################LazyLoad関連#################
############################################
# ニュース欄
@app.route('/news')
def News_func():
    return News(file_data.data["news"]).get_data()
# 参加者一覧の内容
@app.route('/party')
def part():
    Schedule = Schedular(file_data.data["Schedule"])
    res = requests.get("https://weather.tsukumijima.net/api/forecast/city/080010")
    json_data = res.json()
    forecast_data = [json_data["forecasts"][i]["image"]["url"]
                     for i in range(0, 3, 1)]
    return render_template('party.html',
                           data=Schedule.All_lists(),
                           forecast_data=forecast_data), 200

# メンバー一覧（要Auth）
@app.route('/lazy', methods=['get'])
def lazy_load():
    if not(Lazy(file_data.data["lazy"]).check_data(request.headers.get("Auth_Key"))):

        file_data.save_file()
        abort(403)
    else:
        file_data.save_file()
        Friends = friend(file_data.data["Friends"])
        mana = Manager(file_data.data["manager"]).read()
        Friends_data = list(set(Friends.member) - set(mana))
        print("~~~~~~~~~")
        print(Friends_data)
        j=1
        for i in Friends_data:
            try:
                print(j)
                print(i)
                print(line_bot_api.get_profile(i).display_name)
                j=j+1
            except:
                print("!!!")
                j=j+1
        Members_data = [[line_bot_api.get_profile(i).display_name, i]
                          for i in Friends_data]

        Mana_data = [[line_bot_api.get_profile(i).display_name, i]
                            for i in mana]
        return render_template('lazy_loads.html',
                               Mana_data=Mana_data,
                               Members_data=Members_data), 200


#############################################
###############GASのスケジュール##############
############################################
# 月移行動作
@app.route("/nextmonth", methods=['GET'])
def month():
    friends = friend(file_data.data["Friends"]).LIST()
    # 友達それぞれに対してプッシュメッセージを送信
    for username in friends:
        line_bot_api.push_message(username,
                                  messages=FlexSendMessage(
                                            alt_text='今月の日程を入力してください',
                                            contents=Flax().DIC(username)
                                        )
                                    )
    return 'OK', 200

# 日々の確認
@app.route("/checkdate", methods=['POST'])
def checker():
    # ----------------------------------------
    # 1週間以内に3人以上参加できる日があるかの確認
    # ----------------------------------------
    Schedule = Schedular(file_data.data["Schedule"])
    Notify = notify(file_data.data["notify"])
    Historys = History(file_data.data["history"])
    for i in range(1, 8, 1):
        # 現日付+1~8日
        current_dt = datetime.datetime.now(
                            datetime.timezone(datetime.timedelta(hours=9))
                        ) + datetime.timedelta(days=i)
        string = current_dt.strftime('%Y/%m/%d')  # 上を文字列へ
        no = Schedule.count_part(string)  # 参加可能メンバーの人数が
        # 3人以上で且つ通知をしていなかったら
        if (int(no) > 2) and (string not in Notify.data):
            # 通知履歴の追加と保存
            Notify.Add(string)
            # HP用ホームページの追加
            Historys.Add(string)
            # メッセージの生成
            message = '' + string + 'に' + str(no) + '人が参加可能です'
            # 送信！
            line_bot_api.push_message(Group_ID, TextSendMessage(text=message))
            print("通知完了")
    # ----------------------------------------
    # しばらく通知が行われなかったとき
    # ----------------------------------------
    if True:
        # 現日付
        current_dt = datetime.datetime.now(
                            datetime.timezone(datetime.timedelta(hours=9))
                        )
        # 最後の通知日をdatetimeオブジェクトに変形して
        buf = datetime.datetime.strptime(Historys.get_last(), '%Y/%m/%d')
        # タイムゾーンつけて
        buf = buf.replace(
                    tzinfo=datetime.timezone(datetime.timedelta(hours=9))
                )
        # 時間差を得て
        dt = current_dt - buf
        print("前回の通知からの日数:", dt.days)
        # 前回の計画から4週間以上たった一週間ごと
        if ((dt.days % 7 == 0) and dt.days>27):
            message = "ライドが"+str(int(dt.days/7))+"週間行われていません。\nそろそろライドを計画しませんか？"
            line_bot_api.push_message(Group_ID, TextSendMessage(text=message))
            print("しばらくライドが行われなかった。")
    # ----------------------------------------
    # メール転送
    # ----------------------------------------
    # POSTの中身があるときだけ
    if request.data.decode():
        query = json.loads(request.data.decode())
        # 通知すべきメールがあるとき
        if query != []:
            # メッセージリストの作成
            send_list = [TextSendMessage(text="[メール通知]")]
            for i in query:
                text = ("<" + i["title"] + ">\n" + i["body"])
                send_list.append(TextSendMessage(text=text))
            # メッセージをマネージャーに送信
            manage = Manager(file_data.data["manager"])
            for i in manage.read():
                line_bot_api.push_message(i, send_list)
    else:
        # POSTの中身がないとき
        abort(403)
    file_data.save_file()
    return 'OK', 200


#############################################
#################管理画面関連#################
############################################
# 管理者の追加
@app.route('/signup', methods=["get"])
def signget():
    # Staticを実装するのが面倒だったと供述しており
    return render_template('signup.html')

#管理者の追加のPOST
@app.route('/signup', methods=["post"])
def signpost():
    if request.form.get('user', None) and request.form.get('pass', None):
        permit(3,file_data.data).Apply(request.form['user'], request.form['pass'])
    file_data.save_file()
    # Staticを実装するのが面倒だったと供述しており
    return "すでに管理者の人から許可されるのをお待ち下さい", 200

#管理者ページ
@app.route('/management', methods=['get'])
@auth.login_required
def managers():
    Now_manage, Now_req = permit(3,file_data.data).User_lists()
    buff=Lazy(file_data.data["lazy"]).New()
    print(id(file_data.data["lazy"]))
    print(buff)

    file_data.save_file()
    # News().get_data()
    return render_template('management.html',
                                Now_manage=Now_manage,
                                Now_req=Now_req,
                                Version=versions,
                                token_data=buff)
#管理者ページ2
@app.route('/management2', methods=['get'])
@auth.login_required
def managers2():
    Now_manage, Now_req = permit(3,file_data.data).User_lists()
    buff=Lazy(file_data.data["lazy"]).New()
    print(id(file_data.data["lazy"]))
    print(buff)

    file_data.save_file()
    # News().get_data()
    return render_template('management2.html',
                                Now_manage=Now_manage,
                                Now_req=Now_req,
                                Version=versions,
                                token_data=buff)

#管理者ページのPOST
@app.route('/management', methods=['post'])
@auth.login_required
def posts_data():
    # エラー（タイプが無かったとき）
    if not(request.form.get('data_type', None)):
        return 'Forbidden', 403
    # Historyに追加
    elif request.form.get('data_type', None) == "Add_history":
        string = request.form.get('Add_date', None).replace("-", "/")
        if re.fullmatch(r"^\d{4}/\d{2}/\d{1,2}$", string):
            History(file_data.data["history"]).Add(string)
        else:
            return "正規表現不一致", 400
    # Historyから削除
    elif request.form.get('data_type', None) == "Del_history":
        string = request.form.get('Del_date', None).replace("-", "/")
        if re.fullmatch(r"^\d{4}/\d{2}/\d{1,2}$", string):
            History(file_data.data["history"]).Del(string)
        else:
            return "正規表現不一致", 400
    #ニュース欄の書き換え
    elif request.form.get('data_type', None) == "News":
        if request.form.get('naiyo', None):
            News(file_data.data["news"]).Change(request.form['naiyo'])
    # ブロードキャスト
    elif request.form.get('data_type', None) == "broad_cast":
        if request.form.get('message', None) != "":
            messages = TextSendMessage(text=request.form.get('message', None))
            line_bot_api.broadcast(messages=messages)
    #管理者の削除
    elif request.form.get('data_type', None) == "del_mana":
        if request.form.get('delete', None) != "":
            permit(3,file_data.data).Del(request.form.get('delete', None))
    #管理者の許可
    elif request.form.get('data_type', None) == "permit_mana":
        if request.form.get('permit', None) != "":
            permit(3,file_data.data).Allow(request.form.get('permit', None))
    #どれでもなかった
    else:
        return managers()
    file_data.save_file()
    return "送信完了しましたブラウザバックしてください", 200


#############################################
##################メインページ################
############################################
# 日程アンケート
@app.route("/questionaire")
def question():
    # UIDのクエリ引数を取る
    req = request.args
    req_user_id = req.get("UID")
    if req_user_id == None:
        abort(401)
    return render_template('questionaire.html',
                                userdata=Schedular(file_data.data["Schedule"]).Schedule_list(req_user_id)
                                )

# アンケート受付
@app.route("/postdata", methods=['POST'])
def post():
    Schedule = Schedular(file_data.data["Schedule"])
    data = json.loads(request.data)
    data['data'].insert(0, data['name'])
    Schedule.add(data['UID'], data['data'])
    Schedule.save()
    file_data.save_file()
    return "Accepted", 202

# 日程送信完了
@app.route('/end')
def end():
    return app.send_static_file('end.html'), 200

# 参加者一覧
@app.route('/participants')
def participants():
    return app.send_static_file('participants.html'), 200


#############################################
##################LINEAPI関連################
############################################
# APIに応答
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # Webhook bodyをハンドル
    try:
        handle.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# メッセージが送られたら
@handle.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Friends = friend(file_data.data["Friends"])
    if event.message.text == 'version':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=versions))
    if event.message.text == 'Members':
        message = "メンバー一覧:"
        for i in Friends.member:
            print(i)
            profile = line_bot_api.get_profile(i)
            message += '\n'
            message += profile.display_name
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))

    if event.message.text == '明日の天気':
        res = requests.get(
            "https://weather.tsukumijima.net/api/forecast/city/080010")
        data = res.json()
        message = "【明日の天気】\n天気:" + data["forecasts"][1]["telop"] + "\n最低気温:" + data["forecasts"][1]["temperature"]["min"]["celsius"] + "℃\n最高気温:" + data["forecasts"][1]["temperature"]["max"]["celsius"] + "℃\n\n降水確率\n" + " 0~6時:" + \
            data["forecasts"][1]['chanceOfRain']["T00_06"] + "\n 6~12時:" + data["forecasts"][1]['chanceOfRain']["T06_12"] + \
            "\n 12~18時:" + data["forecasts"][1]['chanceOfRain']["T12_18"] + \
            "\n 18~24時:" + data["forecasts"][1]['chanceOfRain']["T18_24"]

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
    return

# フォローEvent
@handle.add(FollowEvent)
def handle_follow(event):
    Flaxes = Flax()
    Friends = friend(file_data.data["Friends"])
    Friends.add(event.source.user_id)
    file_data.save_file()
    # Flaxメッセージに変えて
    container_obj = FlexSendMessage(
                            alt_text='ご参加ありがとうございます。',
                            contents=Flaxes.DIC(event.source.user_id)
                        )

    # プッシュメッセージを送信(リプライのほうがよくね)
    line_bot_api.reply_message(event.reply_token,
                                container_obj)
    return

# 新たに参加した方
@handle.add(MemberJoinedEvent)
def handle_joined(event):
    Flaxes = Flax()
    message2 = "サークルの共有事項等は、ノートに記載しておりますので、ご確認ください。"
    JSON_DIC = Flaxes.DIC2()
    # Flaxメッセージに変えて
    container_obj = FlexSendMessage(
        alt_text='ご参加ありがとうございます。', contents=JSON_DIC)
    # プッシュメッセージを送信
    line_bot_api.reply_message(event.reply_token,
                                [container_obj,
                                TextSendMessage(text=message2)])
    return

# フォロー解除Event
@handle.add(UnfollowEvent)
def handle_unfollow(event):
    friend(file_data.data["Friends"]).remove(event.source.user_id)
    file_data.save_file()
    return


print("main.py is Loaded...")

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)
