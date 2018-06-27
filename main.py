# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

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
idx = 0
driver.get("http://maddawgjav.net/")
sleep(5)
for entry in driver.find_elements_by_css_selector('.entry'):

    print(entry.text)
    idx = idx + 1
    print(str(idx))
    break
    '''
    for a in entry.find_elements_by_css_selector('.more-link'):
        # link_text.append(driver.find_element_by_tag_name('a'))
        link_text.append(a.get_attribute('href'))
    '''

exit()

for link in link_text:
    print(link)
    driver.get(str(link))

    for e in driver.find_elements_by_css_selector('.entry'):

        print("img " + str(e.find_element_by_css_selector('.alignnone').get_attribute('src')))
        # print('a tag ' + e.find_element_by_tag_name('a').text)
        for a in e.find_elements_by_tag_name('a'):
            print('a tag ' + a.get_attribute('href'))
        break
    break

# print(entrys[0])
# print(str(link_text[0]))

# 検索語として「selenium」と入力し、Enterキーを押す。
# driver.find_element_by_id("lst-ib").send_keys("selenium")
# driver.find_element_by_id("lst-ib").send_keys(Keys.ENTER)
# タイトルに「Selenium - Web Browser Automation」と一致するリンクをクリックする。
# driver.find_element_by_link_text("Selenium - Web Browser Automation").click()
# ブラウザを終了する。
driver.close()
