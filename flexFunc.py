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
    if mtext == '@彈性配置':
        sendFlex(event)

    elif mtext[:3] == '###' and len(mtext) > 3:
         manageForm(event, mtext)
# 彈性配置
def sendFlex(event):
    try:
        bubble = BubbleContainer(
            direction='ltr', # 左->右
            # 主要標題
            header=BoxComponent( 
                layout='vertical',
                contents=[
                    TextComponent(text='Tourist attraction', weight='bold', size='xxl'),
                ]
            ),
            # 主要圖片
            hero=ImageComponent(
                url='https://i.imgur.com/OhSWWsW.jpg',
                size='full',
                aspect_ratio='3024:4032',  # 長寬比例
                aspect_mode='cover',
            ),
            # 主要內容
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Blue sky', size='md'),
                    BoxComponent(
                        layout='baseline',  # 水平排列
                        margin='md',
                        contents=[
                            IconComponent(size='lg', url='https://i.imgur.com/GsWCrIx.png'),
                            TextComponent(text='98   ', size='sm', color='#999999', flex=0),
                            IconComponent(size='lg', url='https://i.imgur.com/sJPhtB3.png'),
                            TextComponent(text='100', size='sm', color='#999999', flex=0),
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='Located:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='Taiwan Changhua', color='#666666', size='sm', flex=5)
                                ],
                            ),
                            SeparatorComponent(color='#C0C0C0'),
                            BoxComponent(
                                layout='baseline',
                                margin='sm',
                                contents=[
                                    TextComponent(text='Time:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="2022/08", color='#666666', size='sm', flex=5),
                                ],
                            ),
                        ],
                    ),
                    BoxComponent(  
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(label='Cellphone', uri='tel:0987654321'),
                            ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='Website', uri="https://tourism.chcg.gov.tw/")
                            )
                        ]
                    )
                ],
            ),
            footer=BoxComponent(  #底部版權宣告
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@gmail.com', color='#888888', size='sm', align='center'),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="Flexible configuration", contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='ERROR'))

if __name__ == '__main__':
    app.run(debug=False)
