# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN = 'xoxb-684597766369-679535522738-hH2EbE8yTt6jTD0JCNi5RBfJ'
SLACK_SIGNING_SECRET = '0f919d227261d7679b226f85db3e39b7'

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


# 크롤링 함수 구현하기
def _crawl_music_chart(text):
    if not "music" in text:
        return "`@<봇이름> music` 과 같이 멘션해주세요."

    # 여기에 함수를 구현해봅시다.

    url = "https://music.bugs.co.kr/chart"
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    # 여기에 함수를 구현해봅시다.
    title, artist = [], []
    message = 'Bugs 실시간 음악 차트 Top 10\n'
    for tag in soup.find_all("p", class_="title"):
        title.append(tag.get_text().strip())
        # title.append(str(i)+"위:"+title+"/"+artist)

    for tag in soup.find_all("p", class_="artist"):
        artist.append(tag.get_text().strip())

    # 키워드 리스트를 문자열로 만듭니다.
    for i in range(1, 11):
        if '\n' in artist[i - 1]:
            artist[i - 1] = artist[i - 1].split('\n')[0]
        message += '\n ' + str(i) + '위 : ' + title[i - 1] + ' / ' + artist[i - 1]

    return message


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    message = _crawl_music_chart(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        text=message
    )


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
