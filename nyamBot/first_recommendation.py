# -*- coding: utf-8 -*-
import random
import re
import urllib.request
from string import punctuation

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slack.web.classes import extract_json
from slack.web.classes.blocks import ImageBlock, SectionBlock
from slackeventsapi import SlackEventAdapter


def first_recom(text):
    blocks = []
    if '메뉴' in text:
        food_and_location = text.split()[2:]
        blocks.append(SectionBlock(text="오늘은 이 메뉴 어떠냠 주변 식당 알고 싶으면 `~<메뉴이름> <위치>`, 별로면 `~다시추천`, "
                                   "고르고 싶다면 `~선택`이라고 입력해보겠냠"))
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
        if len(text.split()) < 3 or text.split()[2]=="":
            blocks.append(SectionBlock(text="`~날씨 <키워드>` 형식으로 입력해보겠냠 키워드는 "))
        else:
            blocks.append(SectionBlock(text="날씨 띄어쓰기 하, "
                                            "고르고 싶다면 `~선택`이라고 입력해보겠냠"))
    elif '분위기' in text:
        if len(text.split()) < 3 or text.split()[2]=="":
            blocks.append(SectionBlock(text="`~분위기 <키워드>` 형식으로 입력해보겠냠 키워드는 "))
        else:
            blocks.append(SectionBlock(text="날씨 띄어쓰기 하, "
                                            "고르고 싶다면 `~선택`이라고 입력해보겠냠"))

    elif '방문목적' in text:
        if len(text.split()) < 3 or text.split()[2]=="":
            blocks.append(SectionBlock(text="`~방문목적 <키워드>` 형식으로 입력해보겠냠 키워드는 "))
        else:
            blocks.append(SectionBlock(text="날씨 띄어쓰기 하, "
                                            "고르고 싶다면 `~선택`이라고 입력해보겠냠"))

    elif '편의시설' in text:
        if len(text.split()) < 3 or text.split()[2]=="":
            blocks.append(SectionBlock(text="`~편의시설 <키워드>` 형식으로 입력해보겠냠 키워드는 "))
        else:
            blocks.append(SectionBlock(text="날씨 띄어쓰기 하, "
                                            "고르고 싶다면 `~선택`이라고 입력해보겠냠"))

    elif '인싸맛집' in text:
        if len(text.split()) < 3 or text.split()[2]=="":
            blocks.append(SectionBlock(text="`~인싸맛집 <키워드>` 형식으로 입력해보겠냠 키워드는 "))
        else:
            blocks.append(SectionBlock(text="날씨 띄어쓰기 하, "
                                            "고르고 싶다면 `~선택`이라고 입력해보겠냠"))
    else:
        blocks.append(SectionBlock(text="오늘은 이 메뉴 어떠냠 주변 식당 알고 싶으면 `~<메뉴이름> <위치>`, 별로면 `~다시추천`, "
                                        "고르고 싶다면 `~선택`이라고 입력해보겠냠"))

    return blocks


