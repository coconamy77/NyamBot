# -*- coding: utf-8 -*-
import random
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

#
# def _crawl_food_best(query):
#
#     url = 'https://www.diningcode.com/list.php?query=' + parse.quote(query)
#     soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
#     name = []
#     menu = []
#     address = []
#     pics = []
#     keywords = []
#
#     for ul_tag in soup.find_all("ul", class_="list"):
#
#         for span_tag in ul_tag.find_all("span", class_="btxt"):  # 가게 이름
#             name.append(span_tag.get_text())
#         for span_tag in ul_tag.find_all("span", class_="stxt"):  # 종류
#             menu.append(span_tag.get_text())
#         for span_tag in ul_tag.find_all("span", class_="ctxt"):  # 주소
#             address.append(span_tag.get_text())
#         for idx in soup.find_all("span", class_="img"):
#             pics.append(idx["style"].split("'")[1])
#
#     print(name)
#     if "검색결과가 없습니다" in name[0]:
#         return ["검색결과가 없다냠... 다시 해보겠냠... "]
#
#     else:
#         blocks = []
#         for i in range(0, 3):
#             print(pics[i])
#             block1 = ImageBlock(image_url=pics[i], alt_text="이미지가 안뜬다냠... ㅠㅠ미안하다냠...")
#             keywords.append(name[i] + '\n' + menu[i] + '\n' + address[2 * i + 1] + '\n')
#             block2 = SectionBlock(text=keywords[i])
#             blocks.append(block1)
#             blocks.append(block2)
#
#         return blocks

def crawl_three_restaurant(query):

    url = 'https://www.diningcode.com/list.php?query=' + parse.quote(query)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    name = []
    menu = []
    address = []
    pics = []

    for ul_tag in soup.find_all("ul", class_="list"):
        for span_tag in ul_tag.find_all("span", class_="btxt"):  # 가게 이름
            name.append(span_tag.get_text().split('.')[1])
        for span_tag in ul_tag.find_all("span", class_="stxt"):  # 종류
            menu.append(span_tag.get_text())
        for span_tag in ul_tag.find_all("span", class_="ctxt"):  # 주소
            address.append(span_tag.get_text())

        for idx in soup.find_all("span", class_="img"):
            pics.append(idx["style"].split("'")[1])


    else:
        for idx in range(0,3):
            keywords = []
            blocks = []
            block1 = ImageBlock(image_url=pics[idx], alt_text="이미지가 안뜬다냠... ㅠㅠ미안하다냠...")
            keywords.append(name[idx] + '\n' + menu[idx] + '\n' + address[2 * idx + 1] + '\n')
            block2 = SectionBlock(text=keywords[idx])
            blocks.append(block1)
            blocks.append(block2)

    return blocks




def crawl_one_restaurant(query):
    print(query)
    url = 'https://www.diningcode.com/list.php?query=' + parse.quote(query)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    name = []
    menu = []
    address = []
    pics = []
    i = 0

    for ul_tag in soup.find_all("ul", class_="list"):
        for span_tag in ul_tag.find_all("span", class_="btxt"):  # 가게 이름
            name.append(span_tag.get_text().split('.')[1])
        for span_tag in ul_tag.find_all("span", class_="stxt"):  # 종류
            menu.append(span_tag.get_text())
        for span_tag in ul_tag.find_all("span", class_="ctxt"):  # 주소
            address.append(span_tag.get_text())

        for idx in soup.find_all("span", class_="img"):
            pics.append(idx["style"].split("'")[1])


    else:

        blocks = []
        block1 = ImageBlock(image_url=pics[0], alt_text="이미지가 안뜬다냠... ㅠㅠ미안하다냠...")
        keywords = name[0] + '\n' + menu[0] + '\n' + address[2 * 0 + 1] + '\n'
        block2 = SectionBlock(text=keywords)
        blocks.append(block1)
        blocks.append(block2)

    return blocks
