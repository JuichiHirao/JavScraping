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

    def main(self):

        idx = start = 1
        end = start + 3

        # sub_url = 'category/av-censored/'
        # sub_url = 'category/av-uncensored/'
        sub_url = 'category/av-idols/'
        for idx in range(start, end):

            if idx == 1:
                url = self.main_url + sub_url
            else:
                url = self.main_url + sub_url + 'page/' + str(idx)

            self.register_download_url(url, sub_url)

            idx = idx + 1

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
                            break

                        print(jav2_data.title)
                        with urllib.request.urlopen(a_link.attrs['href']) as response:
                            content_html = response.read()
                            content_html_soup = BeautifulSoup(content_html, "html.parser")
                            post_content = content_html_soup.find('div', class_="post-content")
                            content_links = post_content.find_all('a')
                            link_list = []
                            for content in content_links:
                                href = content.attrs['href']
                                uploaded_match = re.search('.*uploaded.*', href)
                                if uploaded_match:
                                    link_list.append(content.attrs['href'])
                                    print(content.attrs['href'])
                            if len(link_list) > 0:
                                jav2_data.downloadLinks = ' '.join(link_list)

                    self.db.export_jav2(jav2_data)
                    break


if __name__ == '__main__':
    jav2 = EntryRegisterJav2()
    jav2.main()
