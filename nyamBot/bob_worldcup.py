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





