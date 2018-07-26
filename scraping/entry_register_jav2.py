from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from db import mysql_control
import urllib.request
import re
from data import site_data
from bs4 import BeautifulSoup


class EntryRegisterJav2:

    def __init__(self):

        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.main_url = 'http://javarchive.com/'
        # self.main_url = 'http://javarchive.com/category/av-censored/'

        self.db = mysql_control.DbMysql()

    def main2(self):

        idx = start = 1
        end = start + 10

        self.main_url = 'https://javfree.me/'
        # sub_urls = ['category/mosaic/', 'category/avi/']
        sub_urls = ['category/mosaic/']
        for sub_url in sub_urls:
            for idx in range(start, end):

                if idx == 1:
                    url = self.main_url + sub_url
                else:
                    url = self.main_url + sub_url + 'page/' + str(idx)
                print('')
                print(url)
                print('')

                is_exist = self.register_download_url2(url, sub_url)

                if is_exist:
                    print('is_exist ' + str(idx))
                    return

                idx = idx + 1

    def main(self):

        idx = start = 1
        end = start + 30

        self.main_url = 'http://javarchive.com/'
        sub_urls = ['category/av-censored/', 'category/av-uncensored/', 'category/av-idols/']
        for sub_url in sub_urls:
            # sub_url = 'category/av-idols/'
            for idx in range(start, end):

                if idx == 1:
                    url = self.main_url + sub_url
                else:
                    url = self.main_url + sub_url + 'page/' + str(idx)
                print('')
                print(url)
                print('')

                is_exist = self.register_download_url(url, sub_url)

                if is_exist:
                    print('is_exist ' + str(idx))
                    break

                idx = idx + 1

    def register_download_url2(self, main_url, sub_url):

        with urllib.request.urlopen(main_url) as response:
            html = response.read()
            html_soup = BeautifulSoup(html, "html.parser")
            entrys = html_soup.find_all('div', class_='hentry')
            for idx, entry in enumerate(entrys):
                thumbnail_link = entry.find('a', class_='thumbnail-link')
                jav2_data = site_data.Jav2Data
                if 'href' in thumbnail_link.attrs:
                    jav2_data.url = thumbnail_link.attrs['href']

                if len(jav2_data.url) <= 0:
                    continue

                h2 = entry.find('h2', class_='entry-title')
                jav2_data.title = h2.find('a').text
                print(jav2_data.title)
                jav2_data.kind = sub_url

                if self.db.exist_title_and_kind(jav2_data.title, jav2_data.kind, 'jav2'):
                    print('title exists [' + jav2_data.title + ']')
                    return True

                print('  ' + sub_url + '  ' + jav2_data.url)
                with urllib.request.urlopen(jav2_data.url) as response:
                    content_html = response.read()
                    content_html_soup = BeautifulSoup(content_html, "html.parser")
                    post_content = content_html_soup.find('div', class_="entry-content")
                    content_links = post_content.find_all('a')
                    outline = []
                    lines = post_content.find('p').text.splitlines()
                    for line in post_content.find('p').text.splitlines():
                        if len(line.strip()) <= 0:
                            continue
                        outline.append(line)
                    jav2_data.detail = '  '.join(outline)
                    link_list = []
                    for content in content_links:
                        href = content.attrs['href']
                        uploaded_match = re.search('.*extmatrix.*', href)
                        if uploaded_match:
                            link_list.append(content.attrs['href'])
                    if len(link_list) > 0:
                        jav2_data.downloadLinks = ' '.join(link_list)

                    print('  ' + jav2_data.downloadLinks)

                self.db.export_jav2(jav2_data)

            return False

    def register_download_url(self, main_url, sub_url):

        with urllib.request.urlopen(main_url) as response:
            html = response.read()
            html_soup = BeautifulSoup(html, "html.parser")
            # entrys = html_soup.find_all('div', class_="post-meta")
            entrys = html_soup.find_all('div', class_=re.compile('post-meta'))
            for idx, entry in enumerate(entrys):
                jav2_data = site_data.Jav2Data
                jav2_data.kind = sub_url
                a_links = entry.find_all('a')
                for a_link in a_links:
                    print(a_link)

                    if 'href' in a_link.attrs:
                        print(a_link.attrs['href'])
                        jav2_data.title = a_link.attrs['title']

                        if self.db.exist_title(jav2_data.title, 'jav2'):
                            print('title exists [' + jav2_data.title + ']')
                            return True

                        jav2_data.url = a_link.attrs['href']
                        print(jav2_data.title)
                        with urllib.request.urlopen(a_link.attrs['href']) as response:
                            content_html = response.read()
                            content_html_soup = BeautifulSoup(content_html, "html.parser")
                            post_content = content_html_soup.find('div', class_="post-content")
                            content_links = post_content.find_all('a')

                            outline = []
                            lines = post_content.find('p').text.splitlines()
                            for line in lines:
                                if len(line.strip()) <= 0:
                                    continue
                                if re.search('http://', line):
                                    continue
                                outline.append(line)
                            jav2_data.detail = '  '.join(outline)

                            link_list = []
                            for content in content_links:
                                href = content.attrs['href']
                                uploaded_match = re.search('.*uploaded.*', href)
                                if uploaded_match:
                                    link_list.append(content.attrs['href'])
                                    print(content.attrs['href'])
                            if len(link_list) > 0:
                                jav2_data.downloadLinks = ' '.join(link_list)

                    # jav2_data.detail = '  '.join(outline)
                    self.db.export_jav2(jav2_data)
                    break

            return False


if __name__ == '__main__':
    jav2 = EntryRegisterJav2()
    jav2.main2()
    jav2.main()
