# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from urllib import parse
import urllib

SLACK_TOKEN = 'xoxb-689744994544-678334094690-NsGBSeGf3BNIzuzvgdbHYarp'
SLACK_SIGNING_SECRET = '5d5a1aa7f91b12a5ae347cc364eaf78d'

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


#command Books
#def _crawl_food_best(text, user):
def _crawl_food_best(text):
    # data = pd.read_csv(LOCLOG)
    # if user in data["id_code"].values:
    #     index = data[data["id_code"]==user].index[0]
    #     location = data.loc[index,"location"]
    # else:
    #     location = "강남역"

    # location = "강남역"

    # query = location + ' ' + food
    # food = text
    query = text

    url = 'https://www.mangoplate.com/search/' + parse.quote(query)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    region = []
    menu = []
    score = []
    keywords = []
    for i in soup.find_all("ul", class_="list-restaurants"):
        for j in i.find_all("h2", class_="title"): #가게 이름
            region.append(j.get_text())
        for j in i.find_all("p", class_="etc"): #종류
            menu.append(j.get_text())
        for j in i.find_all("strong", class_="point search_point"): #점수
            score.append(j.get_text())

    for i in range(0, len(region)):
        keywords.append(region[i]+'\n'+menu[i]+'\n'+score[i]+'\n')
    keywords= keywords[:3]

    print(keywords)
   # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
   #  return u'\n'.join(keywords), location
    return u'\n'.join(keywords)


# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    # message = _crawl_music_chart(text)
    message = _crawl_food_best(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        text=message
    )


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
