import os
class Flax:
    def DIC(self,IDS):
        url = os.environ["MY_URL"]
        touroku = url+'/questionaire?UID=' + IDS
        check = url+"/participants"
        Payload = {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "下のボタンを押して",
        "align": "center"
      },
      {
        "type": "text",
        "text": "ライドに参加できる日を",
        "align": "center"
      },
      {
        "type": "text",
        "text": "登録してください",
        "align": "center"
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "uri": touroku,
          "label": "日程を登録する"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label":"他の人の日程を確認する" ,
          "uri": check
        },
        "style": "primary",
        "margin": "md"
      }
    ]
  }
}
        return Payload
    def DIC2(self):
        Payload={
        "type": "bubble",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
            "type": "text",
            "text": "ご参加ありがとうございます！",
            "weight": "bold",
            "size": "md",
            "align": "center"
            },
            {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "”CIRC BOT” を友だち追加して、\n日程を登録しましょう！",
                "wrap": true,
                "align": "center"
                },
                {
                "type": "button",
                "action": {
                "type": "uri",
                "label": "友だち追加！",
                "uri": "https://line.me/R/ti/p/@929wpjcj"
                },
                "style": "primary",
                "margin": "30px"
                }
                ],
                "margin": "20px"
                }
                ]
                }
                }
        return Payload
