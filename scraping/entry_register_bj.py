# coding:utf-8
from time import sleep
import iso8601
import re
import yaml
from javcore import db
from javcore import data
from javcore import common


class EntryRegisterBj:

    def __init__(self):

        self.env = common.Environment()
        self.driver = self.env.get_driver()

        with open('site_bj.yml') as file:
            obj = yaml.load(file)
            self.main_url = obj['site_url']
            self.stop_title = obj['stop_title']

        self.bj_dao = db.bj.BjDao()

    def register_page(self):

        if len(self.main_url) <= 0:
            print('no yaml')
            exit(-1)

        start = idx = 1
        exist_count = 1

        end = start + 10
        current_url = ''
        page_url = ''
        is_stop = False
        for idx in range(start, end):
            if idx <= 1:
                self.driver.get(self.main_url)
            else:
                page_url = current_url + "/page/" + str(idx) + "/"
                print(page_url)
                self.driver.get(page_url)

            if idx == start:
                sleep(5)

            if len(current_url) <= 0:
                current_url = self.driver.current_url

            for entry in self.driver.find_elements_by_css_selector('.hentry'):

                bj = data.BjData()

                for h2 in entry.find_elements_by_tag_name('h2'):
                    for a in h2.find_elements_by_tag_name('a'):
                        bj.url = a.get_attribute('href')
                    bj.title = h2.text
                    break

                title_exist = self.bj_dao.is_exist(bj.title)

                if title_exist:
                    exist_count = exist_count + 1
                    if exist_count > 100:
                        is_stop = True
                    print('title exist ' + bj.title)
                    continue
                    # break

                if h2.text == self.stop_title:
                    is_stop = True
                    break

                # <time class="entry-date" datetime="2018-07-07T08:21:46+00:00">2018-07-07</time>
                for time in entry.find_elements_by_tag_name('time'):
                    iso_str = time.get_attribute('datetime')
                    bj.postDate = iso8601.parse_date(iso_str)

                for a in entry.find_elements_by_tag_name('a'):
                    contents_link = a.get_attribute('href')
                    if re.search('uploadgig.com', contents_link):
                        bj.downloadLink = contents_link

                img_links = []
                for img in entry.find_elements_by_tag_name('img'):
                    img_link = img.get_attribute('src')
                    if re.match('.*jpg$', img_link):
                        img_links.append(img_link)

                if len(img_links) > 0:
                    bj.thumbnails = ' '.join(img_links)
                    bj.thumbnailsCount = len(img_links)

                try:
                    for footer in entry.find_elements_by_tag_name('footer'):
                        for a in footer.find_elements_by_tag_name('a'):
                            bj.postedIn = a.text
                except:
                    print("except")

                bj.print()

                self.bj_dao.export(bj)

            if is_stop:
                print('is stop True' + page_url)
                break

            idx = idx + 1


if __name__ == '__main__':
    entry_register = EntryRegisterBj()
    entry_register.register_page()
