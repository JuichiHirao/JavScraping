from time import sleep
from datetime import datetime
from javcore import db
from javcore import data
from javcore import tool
from javcore import common


class EntryRegisterJav:

    def __init__(self):

        self.env = common.Environment()
        self.driver = self.env.get_driver()

        self.main_url = "http://maddawgjav.net/"

        self.jav_dao = db.jav.JavDao()

        self.err_list = []

    def register_page(self):

        p_number_tool = tool.p_number.ProductNumber()
        start = idx = 1
        end = start + 50
        exist_cnt = 0

        is_exist = False

        for idx in range(start, end):
            if idx <= 1:
                self.driver.get(self.main_url)
            else:
                self.driver.get(self.main_url + 'page/' + str(idx) + "/")

            if idx == start:
                sleep(8)

            is_exist = False
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

                jav.productNumber, match_maker, jav.isParse2 = p_number_tool.parse(jav, True)
                if jav.isParse2 < 0:
                    self.err_list.append('  ' + str(jav.isParse2) + ' [' + jav.productNumber + '] ' + jav.title)

                if match_maker is not None:
                    jav.makersId = match_maker.id

                self.jav_dao.export(jav)

            if is_exist:
                print('exist title ' + jav.title)
                exist_cnt = exist_cnt + 1

            if exist_cnt >= 20:
                break

            idx = idx + 1

        self.driver.close()

        for error in self.err_list:
            print(error)


if __name__ == '__main__':
    entry_register = EntryRegisterJav()
    entry_register.register_page()
