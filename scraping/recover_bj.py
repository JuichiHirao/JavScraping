# coding:utf-8
from time import sleep
import urllib.request
import os
import re
import yaml
from javcore import db
from javcore import data
from javcore import common


class EntryRegisterBj:

    def __init__(self):

        self.store_path = "C:\\mydata\\bj-jpeg"

        self.env = common.Environment()
        self.driver = self.env.get_driver()
        self.is_checked = False
        # self.is_checked = True

        with open('site_bj.yml') as file:
            obj = yaml.load(file)
            self.main_url = obj['site_url']
            self.stop_title = obj['stop_title']

        self.bj_dao = db.bj.BjDao()

    def __download_image(self, url: str = '', bj_data: data.BjData = None, filename_suffix: str = ''):

        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        _, ext = os.path.splitext(url)
        basename = os.path.basename(url).replace(ext, '')

        # root => http://www.example.com/foo/bat/test
        # ext => .txt
        pathname = os.path.join(self.store_path, basename)

        # kbj19100101.rar の kbj19100101部分を取得
        basename_link = os.path.basename(bj_data.downloadLink)
        _, link_ext = os.path.splitext(bj_data.downloadLink)
        bj_basename = basename_link.replace(link_ext, '')
        # print(filename_suffix)

        if len(filename_suffix) > 0:
            bj_image_filename = '{}_{}_{}{}'.format(bj_basename, basename, filename_suffix, ext)
        else:
            bj_image_filename = '{}_{}{}'.format(bj_basename, basename, ext)

        try:
            pathname = os.path.join(self.store_path, bj_image_filename)
            sleep(1)
            print('start urlretrieve {}'.format(url))
            result = urllib.request.urlretrieve(url, pathname)
            print('end urlretrieve')
        except:
            print('error [{}]')
            sleep(10)
            with urllib.request.urlopen(url) as response:
                html = response.read()
            result = urllib.request.urlretrieve(url, pathname)

        return bj_image_filename

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
        bj_list = self.bj_dao.get_where_agreement('WHERE length(thumbnails) <= 0')
        for bj in bj_list:
            self.driver.get(bj.url)

            entry = self.driver.find_element_by_id('main')

            img_link_list = []
            for img in entry.find_elements_by_tag_name('img'):
                # print(str(img.get_attribute('src')))
                img_link = img.get_attribute('src')
                if re.match('(.*jpg$|.*gif$)', img_link):
                    img_link_list.append(img_link)

            filename_list = []
            if len(img_link_list) > 1:
                for idx, img_link in enumerate(img_link_list):
                    filename_list.append(self.__download_image(img_link, bj, str(idx+1)))
            elif len(img_link_list) == 1:
                filename_list.append(self.__download_image(img_link_list[0], bj))

            print('{}'.format(filename_list))

            filenames = ' '.join(filename_list)
            if len(filenames.strip()) > 0:
                if not self.is_checked:
                    self.bj_dao.update_thumbnails_info(bj.id, ' '.join(img_link_list), filenames, len(img_link_list))


if __name__ == '__main__':
    entry_register = EntryRegisterBj()
    entry_register.register_page()
