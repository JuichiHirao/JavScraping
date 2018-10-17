# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
from javcore import db
from javcore import data
from javcore import tool


class EntryRegisterJav:

    def __init__(self):

        # http://maddawgjav.net/
        # http://maddawgjav.net/page/2/
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='c:\\SHARE\\chromedriver.exe')

        self.main_url = "http://maddawgjav.net/"

        self.jav_dao = db.jav.JavDao()

    def register_page(self):

        p_number_tool = tool.p_number.ProductNumber()
        start = idx = 1
        end = start + 50

        is_exist = False

        for idx in range(start, end):
            if idx <= 1:
                self.driver.get(self.main_url)
            else:
                self.driver.get(self.main_url + 'page/' + str(idx) + "/")

            if idx == start:
                sleep(8)

            for entry in self.driver.find_elements_by_css_selector('.hentry'):

                jav = data.JavData()
                for h2 in entry.find_elements_by_tag_name('h2'):
                    jav.title = h2.text
                    for a in h2.find_elements_by_tag_name('a'):
                        jav.url = a.get_attribute('href')
                    # print(jav.url)
                    break

                title_exist = self.jav_dao.is_exist(jav.title)

                if title_exist:
                    is_exist = True
                    print('title exist ' + h2.text)

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

                for span in entry.find_elements_by_css_selector('.post-info-top'):
                    str_date = span.find_element_by_tag_name('a').text
                    str_time = span.find_element_by_tag_name('a').get_attribute('title')
                    # June 29, 2018 7:42 am
                    str_datetime = str_date + ' ' + str_time
                    jav.postDate = datetime.strptime(str_datetime, '%B %d, %Y %I:%M %p')
                    # print(post_date)

                jav.productNumber, seller, sell_date, match_maker, is_parse2 = p_number_tool.parse_and_fc2(jav, True)
                if seller is not None and len(seller) > 0:
                    jav.label = seller
                    jav.sellDate = sell_date
                if match_maker is not None:
                    jav.makersId = match_maker.id
                jav.isParse2 = is_parse2
                jav.print()

                self.jav_dao.export(jav)

            if is_exist:
                print('end2 page ' + str(idx))
                break

            idx = idx + 1

        self.driver.close()


if __name__ == '__main__':
    entry_register = EntryRegisterJav()
    entry_register.register_page()
