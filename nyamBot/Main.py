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

SLACK_TOKEN = ?
SLACK_SIGNING_SECRET = ?

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
        cat1 = {}
        with open("src/category1.txt") as cat1:
            for line in cat1:
                pass

        blocks = []
        if '이상밥월드컵' in text:
            food_and_location = text.split()[2:]
            blocks.append(SectionBlock(text="오늘은 이 메뉴 어떠냠 주변 식당 알고 싶으면 `~<메뉴이름> <위치>`, 별로면 `~다시추천`, "
                                            "고르고 싶다면 `~선택`이라고 입력해보겠냠"))
        else:
            block = SectionBlock(text="선택을 선택했구냠!! 너의 취향에 따라 메뉴를 추천해줄테니 골라보겠느냠!\n"
                                      "먼저 기준을 골라보겠냠?\n"
                                      "`~날씨` : 오늘 날씨에 딱 맞는 메뉴를 추천해주겠다냠!\n"
                                      "`~분위기` : 예쁜, 가성비, 깔끔 등 다양한 키워드로 특별한 날을 기념해 보는건 어떠냠?\n"
                                      "`~방문목적` 데이트, 회식, 혼술, 가족외식 등 목적에 따라 추천도 해주겠다냠!!\n"
                                      "`~편의시설` 강아지, 주차, 24시간 등 특별한 상황도 추천해주겠다냠!!\n"
                                      "`~인싸맛집` : 방송에 나온 핫한 식당을 가서 핵인싸로 거듭나는건 어떠냠!!\n"
                                      "위에 코드 중 하나를 선택해서 설명을 들어라냠!")
            blocks.append(block)

    else:
        if '메뉴' in text:
            if len(text.split())>4:
                food = text.split()[2] + text.split()[3]
                blocks=crawl_three_restaurant(food)
        elif '선택' in text:
            block = SectionBlock(text="선택을 선택했구냠!! 너의 취향에 따라 메뉴를 추천해줄테니 골라보겠느냠!\n"
                                      "먼저 기준을 골라보겠냠?\n"
                                      "`~날씨` : 오늘 날씨에 딱 맞는 메뉴를 추천해주겠다냠!\n"
                                      "`~분위기` : 예쁜, 가성비, 깔끔 등 다양한 키워드로 특별한 날을 기념해 보는건 어떠냠?\n"
                                      "`~방문목적` 데이트, 회식, 혼술, 가족외식 등 목적에 따라 추천도 해주겠다냠!!\n"
                                      "`~편의시설` 강아지, 주차, 24시간 등 특별한 상황도 추천해주겠다냠!!\n"
                                      "`~인싸맛집` : 방송에 나온 핫한 식당을 가서 핵인싸로 거듭나는건 어떠냠!!\n"
                                      "위에 코드 중 하나를 선택해서 설명을 들어라냠!")
            blocks.append(block)
        elif '날씨' in text:
            if len(text.split()) < 3 or text.split()[2] == "":
                blocks.append(SectionBlock(text="`~날씨 <키워드>` 형식으로 입력해보겠냠 키워드는 *비오는 날, 여름, 겨울 등*으로 해보겠냠"))
            else:
                food = text.split()[2]
                blocks=crawl_three_restaurant(food+"역삼")

        elif '분위기' in text:
            if len(text.split()) < 3 or text.split()[2] == "":
                blocks.append(SectionBlock(text="`~분위기 <키워드>` 형식으로 입력해보겠냠 키워드는 *고급, 조용한, 예쁜 등*으로 해보겠냠"))
            else:
                food = text.split()[2]
                blocks=crawl_three_restaurant(food+"역삼")

        elif '방문목적' in text:
            if len(text.split()) < 3 or text.split()[2] == "":
                blocks.append(SectionBlock(text="`~방문목적 <키워드>` 형식으로 입력해보겠냠 키워드는 *회식, 데이트, 가족외식, 기념일 등*으로 해보겠냠"))
            else:
                food = text.split()[2]
                blocks=crawl_three_restaurant(food+"역삼")

        elif '편의시설' in text:
            if len(text.split()) < 3 or text.split()[2] == "":
                blocks.append(SectionBlock(text="`~편의시설 <키워드>` 형식으로 입력해보겠냠 키워드는 *무료주차, 발렛주차, 24시간 등*으로 해보겠냠"))
            else:
                food = text.split()[2]
                blocks=crawl_three_restaurant(food+"역삼")

        elif '인싸맛집' in text:
            if len(text.split()) < 3 or text.split()[2] == "":
                blocks.append(SectionBlock(text="`~인싸맛집 <키워드>` 형식으로 입력해보겠냠 키워드는 *수요미식회, 백종원의3대천왕, 생활의달인 등*으로 해보겠냠"))
            else:
                food = text.split()[2]
                blocks=crawl_three_restaurant(food+"역삼")
        else:

            blocks.append(SectionBlock(text="`@<봇이름> 냠냠`으로 시작하면 안되냠. 이유는 없다 그냥 귀엽지않냠"))

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
