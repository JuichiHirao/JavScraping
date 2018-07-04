# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import urllib.request
import re
import locale

options = Options()
options.add_argument('--headless')

# http://maddawgjav.net/
# ブラウザを開く。
driver = webdriver.Chrome()
# Googleの検索TOP画面を開く。
# driver.get("http://maddawgjav.net/")
# http://maddawgjav.net/page/2/
# driver.get("https://www.google.co.jp/")

# 5秒間待機してみる。
# sleep(5)

link_text = []
start = idx = 2

path = "http://maddawgjav.net/"
# print(locale.getlocale(locale.LC_TIME))
# locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
for idx in range(start, start+1):
    if idx <= 1:
        driver.get("http://maddawgjav.net/")
    else:
        driver.get("http://maddawgjav.net/page/" + str(idx) + "/")

    if idx == start:
        sleep(5)

    for entry in driver.find_elements_by_css_selector('.hentry'):

        for h2 in entry.find_elements_by_tag_name('h2'):
            print('h2 ' + h2.text)
            break

        lines = entry.text.splitlines()
        sell_date = ''
        actress = ''
        maker = ''
        label = ''
        for one in lines:
            if len(one.strip()) <= 0:
                continue
            if "発売日" in one:
                arr = one.split("：")
                if len(arr) >= 2:
                    sell_date = arr[1].strip()
            if "出演者" in one:
                arr = one.split("：")
                if len(arr) >= 2:
                    actress = arr[1].strip()
            if "メーカー" in one:
                arr = one.split("：")
                if len(arr) >= 2:
                    maker = arr[1].strip()
            if "レーベル" in one:
                arr = one.split("：")
                if len(arr) >= 2:
                    label = arr[1].strip()

        print("date [" + str(sell_date) + "] actress [" + actress + "] maker [" + maker + "]  label [" + label + "]")

        for span in entry.find_elements_by_css_selector('.post-info-top'):
            str_date = span.find_element_by_tag_name('a').text
            str_time = span.find_element_by_tag_name('a').get_attribute('title')
            # June 29, 2018 7:42 am
            str_datetime = str_date + ' ' + str_time
            post_date = datetime.strptime(str_datetime, '%B %d, %Y %I:%M %p')
            print(post_date)
        for a in entry.find_elements_by_css_selector('.more-link'):
            # link_text.append(driver.find_element_by_tag_name('a'))
            link_text.append(a.get_attribute('href'))

    idx = idx + 1
exit(0)

for link in link_text:
    print(link)
    driver.get(str(link))

    for e in driver.find_elements_by_css_selector('.entry'):

        img_url = e.find_element_by_css_selector('.alignnone').get_attribute('src')
        print("img " + img_url)
        filename = img_url[img_url.rfind("/") + 1:]
        urllib.request.urlretrieve(e.find_element_by_css_selector('.alignnone').get_attribute('src'), filename)
        # print('a tag ' + e.find_element_by_tag_name('a').text)
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
                    contenue_e = driver.find_element_by_class_name('continue').click()
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
                        urllib.request.urlretrieve(img_th_url, filename_th)
                        break
                except:
                    print('except')
                    img_th_url = driver.find_element_by_id('image').get_attribute('src')
                    filename_th = img_th_url[img_th_url.rfind("/") + 1:]
                    print('img_th ' + filename_th + " " + img_th_url)
                    urllib.request.urlretrieve(img_th_url, filename_th)
                    break
            else:
                print('movie tag ' + contents_link)
            break

    # break
# print(entrys[0])
# print(str(link_text[0]))

# 検索語として「selenium」と入力し、Enterキーを押す。
# driver.find_element_by_id("lst-ib").send_keys("selenium")
# driver.find_element_by_id("lst-ib").send_keys(Keys.ENTER)
# タイトルに「Selenium - Web Browser Automation」と一致するリンクをクリックする。
# driver.find_element_by_link_text("Selenium - Web Browser Automation").click()
# ブラウザを終了する。
driver.close()
