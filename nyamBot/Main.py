# -*- coding: utf-8 -*-
import random
import re
import urllib.request

from string import punctuation

from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask
from slack import WebClient
from slack.web.classes import extract_json
from slack.web.classes.blocks import ImageBlock, SectionBlock
from slackeventsapi import SlackEventAdapter

from nyamBot.bob_worldcup import worldcup
from nyamBot.first_recommendation import first_recom
from nyamBot.search_restaurants import crawl_three_restaurant, crawl_one_restaurant

SLACK_TOKEN = 'xoxb-684597766369-679535522738-0JR0JhzKcHNhVoTzKOm8BbFI'
SLACK_SIGNING_SECRET = '0f919d227261d7679b226f85db3e39b7'

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)



# 크롤링 함수 구현하기
def main_question(text):
    blocks=[]
    if '냠냠' in text:
        food_list = []

        food_line = ""
        with open("food_list.txt", 'rt', encoding='UTF8') as food_file:
            for line in food_file:
                food_line += line.replace("\n", ",")
            food_list=food_line.strip().split(",")[:-1]
        food = food_list[random.randrange(1, len(food_list)-1)]
        blocks = crawl_one_restaurant(food+" 역삼역")

        blocks.append(SectionBlock(text = "오늘은 여기서 *"+food+"* 어떠냠? 별로면 `~다시추천`, \n원하는 메뉴 식당 알고 싶으면 `~메뉴 <메뉴이름> <위치>`, \n"
                                     "*너도 모르는* 너가 원하는 메뉴를 알고 싶다면 `!이상밥월드컵`, \n키워드로 고르고 싶다면 `~선택`이라고 입력해주겠냠"))

    elif '~다시추천' in text:
        food_list = []

        food_line = ""
        with open("food_list.txt", 'rt', encoding='UTF8') as food_file:
            for line in food_file:
                food_line += line.replace("\n", ",")
            food_list=food_line.strip().split(",")[:-1]
        food = food_list[random.randrange(1, len(food_list))]
        blocks = crawl_one_restaurant(food+" 역삼역")

        blocks.append(SectionBlock(text = "오늘은 여기서 *"+food+"* 어떠냠? 별로면 `~다시추천`, \n원하는 메뉴 식당 알고 싶으면 `~메뉴 <메뉴이름> <위치>`, \n"
                                     "*너도 모르는* 너가 원하는 메뉴를 알고 싶다면 `!이상밥월드컵`, \n키워드로 고르고 싶다면 `~선택`이라고 입력해주겠냠"))

    elif '!이상밥월드컵' in text:
        blocks = worldcup(text)

    else:
        blocks = first_recom(text)


    return blocks

def process_main(text,channel):
    message_blocks = []
    if not '냠냠' in text and not '~' in text and not '!이상밥월드컵' in text:
        slack_web_client.chat_postMessage(
            channel=channel,
            text="`@<봇이름> 냠냠`으로 시작하면 안되냠. 이유는 없다 그냥 귀엽지않냠"
        )
        return
    else:
        message_blocks = main_question(text)

    slack_web_client.chat_postMessage(
        channel=channel,
        blocks=extract_json(message_blocks)
    )






@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    Thread(target=process_main, args=(text, channel)).start()






# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)
