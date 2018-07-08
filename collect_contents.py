# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import urllib.request
import re
import jav_data
import db
import os

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

link_text = []
start = idx = 1

path = "http://maddawgjav.net/"
jpeg_path = "/Users/juichihirao/jav-jpeg"
# print(locale.getlocale(locale.LC_TIME))
# locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

db = db.DbMysql()

javs = db.get_url_javs()

idx = 0
for jav in javs:
    print(jav.url)
    driver.get(str(jav.url))
    sleep(5)

    if idx == start:
        sleep(5)

    idx = idx + 1

    for e in driver.find_elements_by_css_selector('.entry'):

        img_url = e.find_element_by_css_selector('.alignnone').get_attribute('src')
        print("img " + img_url)
        filename = img_url[img_url.rfind("/") + 1:]
        pathname = os.path.join(jpeg_path, filename)
        urllib.request.urlretrieve(e.find_element_by_css_selector('.alignnone').get_attribute('src'), pathname)
        jav.package = filename
        # print('a tag ' + e.find_element_by_tag_name('a').text)

        movie_links = ''
        for a in e.find_elements_by_tag_name('a'):
            contents_link = a.get_attribute('href')
            if re.match('.*jpg$', contents_link):
                continue
            movie_links = movie_links + ' ' + contents_link
            # print('movie tag ' + contents_link)
        jav.downloadLinks = movie_links.strip()
        print('movie tag ' + jav.downloadLinks)

        for a in e.find_elements_by_tag_name('a'):
            contents_link = a.get_attribute('href')

            if re.match('.*jpg$', contents_link):
                # img20.pixhost.to
                # dst = contents_link.replace('pixhost.to', 'img20.pixhost.to')
                print('jpg tag ' + contents_link)
                driver.get(contents_link)
                sleep(2)
                # <a style="color: blue; font-size: 40px; text-decoration: underline; cursor: pointer;" class="continue">Continue to your image</a>
                try:
                    continue_e = driver.find_element_by_class_name('continue').click()
                    sleep(5)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()  # 遷移先のウィンドウを閉じる。特に必要なければ記述の必要なし
                    sleep(2)
                    allHandles = driver.window_handles
                    for win in allHandles:
                        print('win ' + str(win))
                        driver.switch_to.window(win)
                        sleep(2)
                        img_th_url = driver.find_element_by_id('image').get_attribute('src')
                        print('img ' + img_th_url)
                        filename_th = img_th_url[img_th_url.rfind("/") + 1:]
                        pathname_th = os.path.join(jpeg_path, filename_th)
                        jav.thumbnail = filename_th
                        urllib.request.urlretrieve(img_th_url, pathname_th)
                        break
                except:
                    img_th_url = ''
                    try:
                        img_th_url = driver.find_element_by_id('image').get_attribute('src')
                        print('except')

                        filename_th = img_th_url[img_th_url.rfind("/") + 1:]
                        pathname_th = os.path.join(jpeg_path, filename_th)
                        jav.thumbnail = filename_th
                        print('img_th ' + filename_th + " " + img_th_url)
                        urllib.request.urlretrieve(img_th_url, pathname_th)

                    except:
                        print('except not found')

            db.update_jav(jav)
            break
    # print('movie tag ' + movie_links)

# print(entrys[0])
# print(str(link_text[0]))

# 検索語として「selenium」と入力し、Enterキーを押す。
# driver.find_element_by_id("lst-ib").send_keys("selenium")
# driver.find_element_by_id("lst-ib").send_keys(Keys.ENTER)
# タイトルに「Selenium - Web Browser Automation」と一致するリンクをクリックする。
# driver.find_element_by_link_text("Selenium - Web Browser Automation").click()
# ブラウザを終了する。
driver.close()
