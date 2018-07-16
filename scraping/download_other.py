from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from db import mysql_control
import urllib.request
import re
import os


class EntryRegisterBj:

    def __init__(self):

        abc = 'http://javarchive.com/'
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)

        with open('site_bj.yml') as file:
            obj = yaml.load(file)
            self.main_url = obj['site_url']
            self.stop_title = obj['stop_title']

        self.db = mysql_control.DbMysql()

