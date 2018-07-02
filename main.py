# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.request
import re

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
start = idx = 20

path = "http://maddawgjav.net/"
for idx in range(start, start+1):
    if idx <= 1:
        driver.get("http://maddawgjav.net/")
    else:
        driver.get("http://maddawgjav.net/page/" + str(idx) + "/")

    if idx == start:
        sleep(5)

    for entry in driver.find_elements_by_css_selector('.entry'):

        '''
        l = entry.text.splitlines()
        if "チーム木村" in l[0]:
            print("Match!!!!" + str(idx) + " : " + str(l[0]))
            break
        else:
            print(str(l[0]))
        '''
        for a in entry.find_elements_by_css_selector('.more-link'):
            # link_text.append(driver.find_element_by_tag_name('a'))
            link_text.append(a.get_attribute('href'))

    idx = idx + 1

# exit()

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
