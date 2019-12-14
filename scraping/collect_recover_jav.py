from time import sleep
from datetime import datetime
import urllib.request
import re
import os
import sys
import selenium.common.exceptions
from bs4 import BeautifulSoup
from javcore import db
from javcore import common


class PageData:

    def __init__(self):
        self.package_links = []
        self.thumbnail_links = []
        self.movie_links = []

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

        self.env = common.Environment()
        self.driver = self.env.get_driver()

        self.path = "http://maddawgjav.net/"
        self.store_path = self.env.get_image_path()

        self.jav_dao = db.jav.JavDao()

    def get_images(self):

        start = idx = 1

        # javs = self.jav_dao.get_where_agreement('WHERE package IS NULL AND download_links IS NULL ORDER BY post_date')
        # javs = self.jav_dao.get_where_agreement('WHERE (package = \'\' or thumbnail = \'\') and created_at >= \'2019-12-01\' ORDER BY post_date')
        # javs = self.jav_dao.get_where_agreement('WHERE id = 46078')
        javs = self.jav_dao.get_where_agreement('WHERE thumbnail not like "%jpg%" and created_at >= "2019-10-01" and length(thumbnail) > 0')
        # javs = self.jav_dao.get_where_agreement('WHERE ( post_date > "2019-11-04 13:41:00" and post_date <="2019-11-05 17:28:01") and is_selection >= 0 ')

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

            if len(jav.package.strip()) <= 0:
                jav.package = self.__download_package(page_data.package_links)
                if len(jav.package) <= 0:
                    print('  package image error')

            # if len(jav.thumbnail.strip()) <= 0:
            jav.thumbnail = self.__download_thumbnails(page_data.thumbnail_links)
            if len(jav.thumbnail) <= 0:
                print('  thumbnail image error')

            if jav.downloadLinks is not None and len(jav.downloadLinks.strip()) <= 0:
                file_info_list = []
                for movie_link in page_data.movie_links:
                    with urllib.request.urlopen(movie_link) as response:
                        html = response.read()
                        html_soup = BeautifulSoup(html, "html.parser")
                        file_div = html_soup.find('div', class_='btm')
                        strong_list = file_div.find_all('strong')
                        file_size = ''
                        for data in strong_list:
                            if re.search('[0-9\.]{1,10}[\sMGB]*', data.text):
                                file_size = data.text
                                break

                        filename = file_div.find('a').text.strip()

                        file_info_list.append(filename + ' - ' + file_size)
                        # print(file_size + ' ' + filename + ' ' + movie_link)

                jav.filesInfo = '、'.join(file_info_list)
                print('file_info')
                print('  【' + str(jav.filesInfo) + '】')
                jav.downloadLinks = ' '.join(page_data.movie_links)

            self.jav_dao.update_collect_info(jav)
            break

    def __parse_links(self, entry):

        page_data = PageData()

        # aタグは、downloadのリンクとthumbnailのリンクを取得
        is_hlink = False
        for a in entry.find_elements_by_tag_name('a'):
            contents_link = a.get_attribute('href')

            if re.match('.*jpg$|.*jpeg$|.*imagebam.*', contents_link):
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

        arr_dl_files = []
        for link in links:
            filename = link[link.rfind("/") + 1:]
            pathname = os.path.join(self.store_path, filename)
            if os.path.isfile(pathname):
                now_date = datetime.now().strftime('%Y-%m-%d-%H%M%S')
                pathname = os.path.join(self.store_path, now_date + '_' + filename)
            try:
                urllib.request.urlretrieve(link, pathname)
                is_download = True
            except:
                is_download = False
                print('except error')
                break
            arr_dl_files.append(filename)

        dl_filenames = ''
        if is_download:
            dl_filenames = ' '.join(arr_dl_files)

        return dl_filenames

    def __download_thumbnails(self, links):

        arr_dl_files = []
        for link in links:
            self.driver.get(link)

            m_imagebam = re.match('.*imagebam.*', link)
            # <a style="color: blue; font-size: 40px; text-decoration: underline; cursor: pointer;" class="continue">Continue to your image</a>
            try:
                if m_imagebam:
                    a_links = self.driver.find_elements_by_tag_name('a')
                    for a in a_links:
                        if 'ontinue' in a.text:
                            a.click()
                            break
                else:
                    self.driver.find_element_by_class_name('continue').click()

                sleep(1)

                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.close()  # 遷移先のウィンドウを閉じる。特に必要なければ記述の必要なし

                all_handles = self.driver.window_handles

                for win in all_handles:
                    print('  win ' + str(win))
                    self.driver.switch_to.window(win)
                    if m_imagebam:
                        dl_filename = self.__download_image_imgbam(self.driver, link)
                    else:
                        dl_filename = self.__download_image(self.driver, link)
                    arr_dl_files.append(dl_filename)
                    break

            except:
                print(sys.exc_info())
                try:
                    print('  not popup page   m_imagebam {}'.format(m_imagebam))
                    if m_imagebam:
                        dl_filename = self.__download_image_imgbam(self.driver, link)
                    else:
                        dl_filename = self.__download_image(self.driver, link)
                    # dl_filename = self.__download_image(self.driver, link)
                    arr_dl_files.append(dl_filename)
                    break

                except:
                    print('  except thumbnail file 404 not found')

        is_download = True

        for filename in arr_dl_files:
            pathname = os.path.join(self.store_path, filename)
            if not os.path.exists(pathname):
                is_download = False
                break

        dl_filenames = ''
        if is_download:
            dl_filenames = ' '.join(arr_dl_files)

        return dl_filenames

    def __download_image_imgbam(self, driver, link):

        thumbnail_url = ''
        try:
            image_container = driver.find_element_by_class_name('image-container')
        except selenium.common.exceptions.NoSuchElementException:
            print(sys.exc_info())
            basename = os.path.basename(link)
            image_list = driver.find_elements_by_tag_name('img')
            for img in image_list:
                print('{} {}'.format(basename, str(img)))
                img_src = img.get_attribute('src')
                if basename in img_src:
                    image_id = img
                    break

        if image_container is not None:
            image_id = image_container.find_element_by_tag_name('img')
            thumbnail_url = image_id.get_attribute('src')
        else:
            thumbnail_url = image_id.get_attribute('src')

        filename = link[link.rfind("/") + 1:]
        if not re.match('.*jpg$|.*jpeg$', filename):
            filename = '{}.jpg'.format(filename)
        pathname = os.path.join(self.store_path, filename)
        # if os.path.isfile(pathname):
        #     now_date = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        #     pathname = os.path.join(self.store_path, now_date + '_' + filename)
        print('    imgaebam img_th ' + filename + ' ' + thumbnail_url)
        urllib.request.urlretrieve(thumbnail_url, pathname)

        return filename

    def __download_image(self, driver, link):

        thumbnail_url = ''
        try:
            image_id = driver.find_element_by_id('image')
        except selenium.common.exceptions.NoSuchElementException:
            image_id = driver.find_element_by_tag_name('img')

        if image_id is not None:
            thumbnail_url = image_id.get_attribute('src')

        filename = link[link.rfind("/") + 1:]
        pathname = os.path.join(self.store_path, filename)
        if os.path.isfile(pathname):
            now_date = datetime.now().strftime('%Y-%m-%d-%H%M%S')
            pathname = os.path.join(self.store_path, now_date + '_' + filename)
        print('    img_th ' + filename + ' ' + thumbnail_url)
        urllib.request.urlretrieve(thumbnail_url, pathname)

        return filename


if __name__ == '__main__':
    collect_jav = CollectJav()
    collect_jav.get_images()
