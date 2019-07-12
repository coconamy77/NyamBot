# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.web.classes import extract_json
from slack.web.classes.blocks import ImageBlock, SectionBlock

from urllib import parse
import urllib

SLACK_TOKEN = 'xoxb-689744994544-678334094690-fhg3ggwc8nobnNtsqnrxqCHw'
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
    query = text

    url = 'https://www.diningcode.com/list.php?query=' + parse.quote(query)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    region = []
    menu = []
    address = []
    keywords = []
    pics = []

    for ul_tag in soup.find_all("ul", class_="list"):
        for span_tag in ul_tag.find_all("span", class_="btxt"): #가게 이름
            region.append(span_tag.get_text())
        for span_tag in ul_tag.find_all("span", class_="stxt"): #종류
            menu.append(span_tag.get_text())
        for span_tag in ul_tag.find_all("span", class_="ctxt"): #주소
            address.append(span_tag.get_text())
        for i in soup.find_all("span", class_="img"):
            pics.append(i["style"].split("'")[1])

    blocks=[]
    for i in range(0,3):
        block1 = ImageBlock(image_url=pics[i], alt_text="이미지가안뜰때보이는문구")
        keywords.append(region[i] + '\n' + menu[i] + '\n' + address[2 * i + 1] + '\n')
        block2 = SectionBlock(text=keywords[i])
        blocks.append(block1)
        blocks.append(block2)

    return blocks

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    message_blocks = []
    message_blocks = _crawl_food_best(text)

    slack_web_client.chat_postMessage(
        channel=channel,
        # text=message
        blocks=extract_json(message_blocks)
    )


# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
