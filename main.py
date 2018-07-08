# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import urllib.request
import re
import jav_data
import db
import locale

options = Options()
options.add_argument('--headless')

# http://maddawgjav.net/
# ブラウザを開く。
driver = webdriver.Chrome(chrome_options=options)
# Googleの検索TOP画面を開く。
# driver.get("http://maddawgjav.net/")
# http://maddawgjav.net/page/2/
# driver.get("https://www.google.co.jp/")

# 5秒間待機してみる。
# sleep(5)

link_text = []
start = idx = 1

path = "http://maddawgjav.net/"
# print(locale.getlocale(locale.LC_TIME))
# locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

db = db.DbMysql()

end = start + 20
is_exist = False
for idx in range(start, end):
    if idx <= 1:
        driver.get("http://maddawgjav.net/")
    else:
        driver.get("http://maddawgjav.net/page/" + str(idx) + "/")

    if idx == start:
        sleep(5)

    for entry in driver.find_elements_by_css_selector('.hentry'):

        jav = jav_data.JavData()
        for h2 in entry.find_elements_by_tag_name('h2'):
            jav.title = h2.text
            break

        title_exist = db.exist_title(jav.title)

        if title_exist:
            is_exist = True
            print('title exist ' + h2.text)
            continue

        if is_exist:
            print('end title exist ' + h2.text)
            break

        if bool("[VR3K]" in jav.title) or bool("[VR]" in jav.title):
            continue

        lines = entry.text.splitlines()

        for one in lines:
            if len(one.strip()) <= 0:
                continue

            if "発売日" in one:
                str_date = jav.get_date(one)
                if len(str_date) > 0:
                    jav.sellDate = jav.get_date(one)

            if "出演者" in one:
                jav.actress = jav.get_text(one)
            if "メーカー" in one:
                jav.maker = jav.get_text(one)
            if "レーベル" in one:
                jav.label = jav.get_text(one)

        # print("date [" + str(sell_date) + "] actress [" + actress + "] maker [" + maker + "]  label [" + label + "]")

        for span in entry.find_elements_by_css_selector('.post-info-top'):
            str_date = span.find_element_by_tag_name('a').text
            str_time = span.find_element_by_tag_name('a').get_attribute('title')
            # June 29, 2018 7:42 am
            str_datetime = str_date + ' ' + str_time
            jav.postDate = datetime.strptime(str_datetime, '%B %d, %Y %I:%M %p')
            # print(post_date)
        for a in entry.find_elements_by_css_selector('.more-link'):
            # link_text.append(a.get_attribute('href'))
            jav.url = a.get_attribute('href')

        jav.print()

        db.export_jav(jav)

    if is_exist:
        print('end2 title exist ' + h2.text)
        break

    idx = idx + 1

driver.close()
