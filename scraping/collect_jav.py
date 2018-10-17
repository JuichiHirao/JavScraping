# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.request
import re
import os
from javcore import db


class PageData:

    def __init__(self):
        self.package_links = []
        self.thumbnail_links = []
        self.movie_links = []

    def get_package_links(self):
        join_link = ''
        for idx, link in enumerate(self.package_links):
            if idx == 0:
                join_link = link[link.rfind("/") + 1:]
            else:
                join_link = join_link + ' ' + link[link.rfind("/") + 1:]

        return join_link

    def get_thumbnail_links(self):
        join_link = ''
        for idx, link in enumerate(self.thumbnail_links):
            if idx == 0:
                join_link = link[link.rfind("/") + 1:]
            else:
                join_link = join_link + ' ' + link[link.rfind("/") + 1:]

        return join_link

    def print(self):
        if len(self.package_links) >= 1:
            print('package')
            for link in self.package_links:
                print('  [' + link + ']')
        if len(self.thumbnail_links) >= 1:
            print('thumbnail')
            for link in self.thumbnail_links:
                print('  [' + link + ']')
        if len(self.movie_links) >= 1:
            print('movie')
            for link in self.movie_links:
                print('  [' + link + ']')


class CollectJav:

    def __init__(self):

        # http://maddawgjav.net/
        # http://maddawgjav.net/page/2/
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='c:\\SHARE\\chromedriver.exe')
        # self.driver = webdriver.Chrome(chrome_options=options)

        self.path = "http://maddawgjav.net/"
        self.store_path = "D:\DATA\jav-save"

        self.jav_dao = db.jav.JavDao()

    def get_images(self):

        start = idx = 1

        javs = self.jav_dao.get_where_agreement('WHERE package IS NULL AND download_links IS NULL ORDER BY post_date')

        for jav in javs:
            print(str(idx) + '/' + str(len(javs)) + ' ' + jav.url + jav.productNumber)
            self.driver.get(str(jav.url))

            if idx == start:
                sleep(8)

            self.execute_info(jav, self.driver)

            idx = idx + 1

        self.driver.close()

    def execute_info(self, jav, driver):

        for e in driver.find_elements_by_css_selector('.entry'):
            page_data = self.__parse_links(e)

            if self.__download_package(page_data.package_links):
                jav.package = page_data.get_package_links()
            else:
                print('  package image error')

            if self.__download_thumbnails(page_data.thumbnail_links):
                jav.thumbnail = page_data.get_thumbnail_links()
            else:
                print('  thumbnail image error')

            jav.downloadLinks = ' '.join(page_data.movie_links)

            self.jav_dao.update_collect_info(jav)

    def __parse_links(self, entry):

        page_data = PageData()

        # aタグは、downloadのリンクとthumbnailのリンクを取得
        is_hlink = False
        for a in entry.find_elements_by_tag_name('a'):
            contents_link = a.get_attribute('href')
            if re.match('.*jpg$', contents_link):
                page_data.thumbnail_links.append(contents_link)
            if re.match('.*rapid.*', contents_link):
                page_data.movie_links.append(contents_link)
            if re.match('.*hlink.*', contents_link):
                is_hlink = True

        # imgタグは、packageのリンク
        img_url = ''
        try:
            img_url = entry.find_element_by_css_selector('.alignnone').get_attribute('src')
        except:
            try:
                img_url = entry.find_element_by_css_selector('.aligncenter').get_attribute('src')
            except:
                try:
                    img_url = entry.find_element_by_tag_name('img').get_attribute('src')
                except:
                    print('except!!')

        if len(img_url) > 0:
            page_data.package_links.append(img_url)

        if is_hlink:
            self.driver.get(str(contents_link))
            for a in self.driver.find_elements_by_tag_name('a'):
                contents_link = a.get_attribute('href')
                if re.match('.*rapid.*', contents_link):
                    page_data.movie_links.append(contents_link)

        page_data.print()

        return page_data

    def __download_package(self, links):

        is_download = False

        for link in links:
            filename = link[link.rfind("/") + 1:]
            pathname = os.path.join(self.store_path, filename)
            try:
                urllib.request.urlretrieve(link, pathname)
                is_download = True
            except:
                print('except error')

        return is_download

    def __download_thumbnails(self, links):

        for link in links:
            self.driver.get(link)

            # <a style="color: blue; font-size: 40px; text-decoration: underline; cursor: pointer;" class="continue">Continue to your image</a>
            try:
                self.driver.find_element_by_class_name('continue').click()
                sleep(1)

                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.close()  # 遷移先のウィンドウを閉じる。特に必要なければ記述の必要なし

                all_handles = self.driver.window_handles

                for win in all_handles:
                    print('  win ' + str(win))
                    self.driver.switch_to.window(win)
                    self.__download_image(self.driver, link)

                    break

            except:
                try:
                    print('  not popup page')
                    self.__download_image(self.driver, link)

                except:
                    print('  except thumbnail file 404 not found')

        is_download = True

        for link in links:
            filename_th = link[link.rfind("/") + 1:]
            pathname_th = os.path.join(self.store_path, filename_th)
            if not os.path.exists(pathname_th):
                is_download = False
                break

        return is_download

    def __download_image(self, driver, link):
        thumbnail_url = driver.find_element_by_id('image').get_attribute('src')

        filename = link[link.rfind("/") + 1:]
        pathname = os.path.join(self.store_path, filename)
        print('    img_th ' + filename + ' ' + thumbnail_url)
        urllib.request.urlretrieve(thumbnail_url, pathname)


if __name__ == '__main__':
    collect_jav = CollectJav()
    collect_jav.get_images()
