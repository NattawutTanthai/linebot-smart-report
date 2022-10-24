import json , os , aiohttp
from fastapi import Request, FastAPI, HTTPException
from linebot import AsyncLineBotApi, WebhookParser
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, 
    TextMessage, 
    TextSendMessage, 
    QuickReply, 
    QuickReplyButton
)

channel_secret = os.getenv('LINE_CHANNEL_SECRET','9433d2b91e6522e1c271aac0d08ba4bc')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'IOGdPaM84/wtqPzo4J1C+SMCnk5ElyaeAEnFgXIGm7tp2/8Po3Hxgm+5hhtgRxLU7f+B94PT/JWpEiB8Usyk5HGZnKbZ+bOHLgXoGqCbKxYXSH+GB5zeECSE7m/addT62gZ6qehEHWqfEO0VQ2u5KwdB04t89/1O/w1cDnyilFU=')

app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(channel_access_token, async_http_client)
parser = WebhookParser(channel_secret)


@app.post("/")
async def Main(request: Request):
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = await request.body()
    body = body.decode()
    print("Body====>",body)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # for event in events:
    #     print("456")
        # if not isinstance(event, MessageEvent):
        #     continue
        # if not isinstance(event.message, TextMessage):
        #     continue

    # print("type====>",events.message.type)
    match events.message.type :
        case "text":
            if events.message.text == "แจ้งปัญหา":
                text_message = TextSendMessage(
                    text='ขอตำแหน่งที่ตั้งหน่อยครับ',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action={
                                    "type": "location",
                                    "label": "Location"
                                }
                            ),
                            QuickReplyButton(
                                action={
                                    "type": "message",
                                    "label": "ยกเลิกการแจ้ง",
                                    "text": "ยกเลิกการแจ้ง"
                                }
                            )
                        ]
                    )
                )
            elif events.message.text == "ยกเลิกการแจ้ง":
                text_message = TextSendMessage("เลือกเมนูได้เลยครับ")
        case "location":
            text_message = TextSendMessage("เลือกเมนูได้เลยครับ")
    print("TextSendMessage====>",text_message)



    await line_bot_api.reply_message(
        events.reply_token,
        text_message
    )

    return 'OK'
