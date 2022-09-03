from flask import Flask
app = Flask(__name__)

from flask import request, abort, render_template
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, \
TextSendMessage, BubbleContainer, ImageComponent, BoxComponent, \
TextComponent, IconComponent, ButtonComponent, SeparatorComponent, \
FlexSendMessage, URIAction

import initial
DATA = initial.init()
line_bot_api = LineBotApi(DATA.LINEBOT_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(DATA.LINEBOT_CHANNEL_SECRET)
liff_id = DATA.liff_id

# LIFF靜態頁面
@app.route('/form')
def form():
	return render_template('index.html', liffid = liff_id)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext[:3] == '###' and len(mtext) > 3:
         manageForm(event, mtext)

def manageForm(event, mtext):
    try:
        flist = mtext[3:].split('/')
        outcome = 'Name: ' + flist[0] + '\n'
        outcome += 'date: ' + flist[1] + '\n'
        outcome += 'Tourist attraction: ' + flist[2]
        message = TextSendMessage(
            text = outcome
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='ERROR'))

if __name__ == '__main__':
    app.run(debug=True)
