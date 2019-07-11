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
        food_and_location = text.split()[1:]
        blocks.append(SectionBlock(text="오늘은 이 메뉴 어떠냠 주변 식당 알고 싶으면 `~<메뉴이름> <위치>`, 별로면 `~다시추천`, "
                                   "고르고 싶다면 `~선택`이라고 입력해보겠냠"))

    return blocks


