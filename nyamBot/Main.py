# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slack.web.classes import extract_json
from slack.web.classes.blocks import ImageBlock, SectionBlock
from slackeventsapi import SlackEventAdapter

# SLACK_TOKEN = 'xoxb-684597766369-679535522738-CmmCvgpli7d3Xk1jufU1dcsa'
# SLACK_SIGNING_SECRET = '0f919d227261d7679b226f85db3e39b7'

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


# 크롤링 함수 구현하기
def main_question(text):
    if '냠냠' in text:
        block1 = ImageBlock(image_url="https://mp-seoul-image-production-s3.mangoplate.com/46971_1429020571192?fit=around|359:240&crop=359:240;*,*&output-format=jpg&output-quality=80",alt_text="이미지가안뜰때보이는문구")
        block2 = SectionBlock(text = "오늘은 이 메뉴 어떠냠 주변 식당 알고 싶으면 `~<메뉴이름> <위치>`, 별로면 `~다시추천`,\n"
                                     "고르고 싶다면 `~선택`이라고 입력해보겠냠")
        return [block1, block2]

    else:
        block2 = SectionBlock(text="오늘은 이 메뉴 어떠냠 주변 식당 알고 싶으면 `~<메뉴이름> <위치>`, 별로면 `~다시추천`,\n"
                                   "고르고 싶다면 `~선택`이라고 입력해보겠냠")
        return [block2]


@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    if not '냠냠' in text:
        if '~' in text:
            message_blocks = []
            message_blocks = main_question(text)
            slack_web_client.chat_postMessage(
                channel=channel,
                blocks=extract_json(message_blocks)
            )
        else:
            slack_web_client.chat_postMessage(
                channel=channel,
                text="`@<봇이름> 냠냠`으로 시작하면 안되냠. 이유는 없다 그냥 귀엽지않냠"
            )
    else:
        message_blocks = []
        message_blocks = main_question(text)
        slack_web_client.chat_postMessage(
            channel=channel,
            blocks=extract_json(message_blocks)
        )





# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
