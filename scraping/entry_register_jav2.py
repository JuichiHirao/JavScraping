import urllib.request
import re
import sys
import iso8601
from datetime import datetime
from bs4 import BeautifulSoup
from javcore import db
from javcore import data


class EntryRegisterJav2:

    def __init__(self):

        self.main_url = 'http://javarchive.com/'

        self.jav_dao = db.jav.JavDao()
        self.jav2_dao = db.jav2.Jav2Dao()
        self.exist_max = 30
        self.exist_cnt = 0

    def main3(self):

        idx = start = 1
        end = start + 50
        self.exist_cnt = 0

        self.main_url = 'https://www.hd-auto.com/'
        # sub_urls = ['category/mosaic/', 'category/avi/']
        sub_urls = ['']
        for sub_url in sub_urls:
            for idx in range(start, end):

                if idx == 1:
                    url = self.main_url + sub_url
                else:
                    url = self.main_url + sub_url + 'page/' + str(idx)
                print('')
                print(url)
                print('')

                self.register_download_url3(url, sub_url)

                if self.exist_cnt > self.exist_max:
                    print('page exist_max [' + str(self.exist_max) + ']  over')
                    return

    def main2(self):

        idx = start = 1
        end = start + 30
        self.exist_cnt = 0

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

                self.register_download_url2(url, sub_url)

                if self.exist_cnt > self.exist_max:
                    print('page exist_max [' + str(self.exist_max) + ']  over')
                    return

    def main(self):

        idx = start = 1
        end = start + 30

        self.main_url = 'http://javarchive.com/'
        sub_urls = ['category/av-censored/', 'category/av-uncensored/', 'category/av-idols/']
        for sub_url in sub_urls:
            self.exist_cnt = 0
            # sub_url = 'category/av-idols/'
            for idx in range(start, end):

                if idx == 1:
                    url = self.main_url + sub_url
                else:
                    url = self.main_url + sub_url + 'page/' + str(idx)
                print('')
                print(url)
                print('')

                self.register_download_url(url, sub_url)

                if self.exist_cnt > self.exist_max:
                    print('page exist_max [' + str(self.exist_max) + ']  over')
                    break

    def register_download_url3(self, main_url, sub_url):

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        with urllib.request.urlopen(main_url) as response:
            html = response.read()
            html_soup = BeautifulSoup(html, "html.parser")
            # entrys = html_soup.find_all('div', class_='hentry')
            # entrys = html_soup.find_all('div', class_='archive-content')
            article_list = html_soup.find_all('article')
            # for idx, entry in enumerate(entrys):
            for idx, article in enumerate(article_list):
                jav2_data = data.Jav2Data()
                for class_name in article.attrs['class']:
                    if 'category-' in class_name:
                        jav2_data.kind = class_name

                entry = article.find('div', class_='archive-content')
                a_link = entry.find('a')
                if 'href' in a_link.attrs:
                    jav2_data.url = a_link.attrs['href']

                # if len(jav2_data.url) <= 0:
                #     continue

                h2 = entry.find('h2', class_='entry-title')
                jav2_data.title = h2.find('a').text

                if self.exist_cnt > self.exist_max:
                    print('exist_max [' + str(self.exist_max) + ']  over')
                    return

                if self.jav2_dao.is_exist(jav2_data.title, jav2_data.kind):
                    print('title exists [' + jav2_data.title + '] kind [' + jav2_data.kind)
                    self.exist_cnt = self.exist_cnt + 1
                    continue

                print(jav2_data.title)
                print('  ' + jav2_data.url)

                with urllib.request.urlopen(jav2_data.url) as response:
                    html_sub = response.read()
                    html_soup_sub = BeautifulSoup(html_sub, "html.parser")

                    # <time class="entry-date" datetime="2018-07-07T08:21:46+00:00">2018-07-07</time>
                    time = html_soup_sub.find('time', class_='entry-date')
                    iso_str = time.attrs['datetime']
                    jav2_data.postDate = iso8601.parse_date(iso_str)

                    post_content = html_soup_sub.find('div', class_="entry-content")
                    outline = []
                    p_list = post_content.find_all('p')
                    for p in p_list:
                        p_text = p.text
                        if jav2_data.title == p_text.strip():
                            continue
                        lines = p_text.splitlines()
                        for line in lines:
                            arr_detail = line.split('：')
                            if len(arr_detail) >= 1:
                                if 'Preview:' in arr_detail[0] or 'Btafile:' in arr_detail[0]:
                                    break
                                if len(arr_detail) == 1:
                                    line = arr_detail[0].strip()
                                elif len(arr_detail) >= 2:
                                    line = arr_detail[0].strip() + ':' + arr_detail[1].strip()
                            print('    ' + line)
                            if len(line.strip()) <= 0:
                                continue
                            outline.append(line)
                    jav2_data.detail = '、'.join(outline)

                    pkg_src = post_content.find('img')
                    jav2_data.package = pkg_src.attrs['src']

                    # site_main = html_soup_sub.find_all('div', class_='site-main')
                    a_links = html_soup_sub.find_all('a')
                    # a_links = site_main.find_all('a')
                    link_list = []
                    files_list = []
                    thumbnail_list = []
                    for idx, link in enumerate(a_links):
                        content_link = link.attrs['href']
                        if 'btafile.com' in content_link:
                            link_list.append(content_link)
                            files_list.append(link.text)
                            # print(content_link)
                            print('    ' + link.text + ' <-- ' + content_link)
                        if 'pixhost.to' in content_link:
                            thumbnail_list.append(content_link)

                    jav2_data.downloadLinks = ' '.join(link_list)
                    jav2_data.filesInfo = '、'.join(files_list)
                    jav2_data.thumbnail = ' '.join(thumbnail_list)
                    jav2_data.print()

                self.jav2_dao.export(jav2_data)

            return False

    def register_download_url2(self, main_url, sub_url):

        with urllib.request.urlopen(main_url) as response:
            html = response.read()
            html_soup = BeautifulSoup(html, "html.parser")
            entrys = html_soup.find_all('div', class_='hentry')
            for idx, entry in enumerate(entrys):
                thumbnail_link = entry.find('a', class_='thumbnail-link')
                jav2_data = data.Jav2Data()
                if 'href' in thumbnail_link.attrs:
                    jav2_data.url = thumbnail_link.attrs['href']

                if len(jav2_data.url) <= 0:
                    continue

                h2 = entry.find('h2', class_='entry-title')
                jav2_data.title = h2.find('a').text
                print(jav2_data.title)
                jav2_data.kind = sub_url

                if self.exist_cnt > self.exist_max:
                    print('exist_max [' + str(self.exist_max) + ']  over')
                    return

                if self.jav2_dao.is_exist(jav2_data.title, jav2_data.kind):
                    print('title exists [' + jav2_data.title + '] kind [' + jav2_data.kind)
                    self.exist_cnt = self.exist_cnt + 1
                    continue

                print('  ' + sub_url + '  ' + jav2_data.url)
                with urllib.request.urlopen(jav2_data.url) as response:
                    content_html = response.read()
                    content_html_soup = BeautifulSoup(content_html, "html.parser")
                    post_content = content_html_soup.find('div', class_="entry-content")
                    content_links = post_content.find_all('a')

                    outline = []
                    lines = post_content.find('p').text.splitlines()
                    for line in lines:
                        if len(line.strip()) <= 0:
                            continue
                        outline.append(line)
                    jav2_data.detail = '  '.join(outline)
                    link_list = []
                    file_list = []
                    for content in content_links:
                        href = content.attrs['href']
                        uploaded_match = re.search('.*extmatrix.*', href)
                        if uploaded_match:
                            link_list.append(content.attrs['href'])

                            with urllib.request.urlopen(content.attrs['href']) as response:
                                html_sub = response.read()
                                html_soup_sub = BeautifulSoup(html_sub, "html.parser")
                                h1_list = html_soup_sub.find_all('h1')
                                for h1 in h1_list:
                                    if 'Get Premium' in h1.text:
                                        continue
                                    file_list.append(h1.text)

                    jav2_data.filesInfo = '、'.join(file_list)

                    if len(link_list) > 0:
                        jav2_data.downloadLinks = ' '.join(link_list)

                    # print('  ' + jav2_data.downloadLinks)
                    jav2_data.print()

                self.jav2_dao.export(jav2_data)

            return False

    def register_download_url(self, main_url, sub_url):

        with urllib.request.urlopen(main_url) as response:
            html = response.read()
            html_soup = BeautifulSoup(html, "html.parser")
            entrys = html_soup.find_all('div', class_=re.compile('post-meta'))
            for idx, entry in enumerate(entrys):
                jav2_data = data.Jav2Data()
                jav2_data.kind = sub_url
                a_links = entry.find_all('a')
                for a_link in a_links:
                    print(a_link)

                    if 'href' in a_link.attrs:
                        print(a_link.attrs['href'])
                        jav2_data.title = a_link.attrs['title']

                        if 'ENCODE720P' in jav2_data.title:
                            continue

                        if self.exist_cnt > self.exist_max:
                            print('exist_max [' + str(self.exist_max) + ']  over')
                            return

                        if self.jav2_dao.is_exist(jav2_data.title):
                            print('title exists [' + jav2_data.title + ']')
                            self.exist_cnt = self.exist_cnt + 1
                            continue

                        jav2_data.url = a_link.attrs['href']
                        print(jav2_data.title)
                        with urllib.request.urlopen(a_link.attrs['href']) as response:
                            content_html = response.read()
                            content_html_soup = BeautifulSoup(content_html, "html.parser")
                            post_content = content_html_soup.find('div', class_="post-content")
                            content_links = post_content.find_all('a')

                            # Posted by noname on January 6th, 2019 12:26 PM | AV Censored 
                            post_date = content_html_soup.find('div', class_='post-date')
                            # m_post_date = re.search('.*Posted by noname on (?P<match_str>[a-zA-Z0-9\s]*) |.*', post_date.text)
                            m_post_date = re.search('on (?P<match_str>[a-zA-Z0-9:,\s]*)\s\|', post_date.text)
                            # m_post_date = re.search('Posted .*', post_date.text)
                            # print('  2 post-date : ' + post_date.text)
                            # m_post_date = re.search('.*Posted by noname on (?P<match_str>[a-zA-Z0-9 ]* |).*', post_date.text)
                            if m_post_date:
                                str_post_date = re.sub('(th|rd|nd),', ',', m_post_date.group('match_str'))
                                print('  m_post_date [' + str_post_date + ']')
                                # print('  m_post_date [' + str(m_post_date.group()) + ']')
                                try:
                                    m_post = re.search('[0-9][a-z]{2}, ', str_post_date)
                                    if m_post:
                                        str_post_date = str_post_date.replace(m_post.group(), ', ')
                                    jav2_data.postDate = datetime.strptime(str_post_date, '%B %d, %Y %I:%M %p')
                                except ValueError as ve:
                                    print(sys.exc_info())


                            # str_datetime = str_date + ' ' + str_time

                            outline = []
                            p_list = post_content.find_all('p')
                            for p in p_list:
                                p_text = p.text
                                if jav2_data.title == p_text.strip():
                                    continue
                                lines = p_text.splitlines()
                                for line in lines:
                                    if len(line.strip()) <= 0:
                                        continue
                                    if 'https://' in line:
                                        break

                                    outline.append(line)

                            jav2_data.detail = '、'.join(outline)

                            link_list = []
                            file_list = []
                            for content in content_links:
                                href = content.attrs['href']
                                img_match = re.search('.*img\.javstore\.net.*', href)
                                uploaded_match = re.search('.*uploaded.*', href)
                                if uploaded_match:
                                    # link_list.append(content.attrs['href'])
                                    print(content.attrs['href'])

                                    link_list.append(content.attrs['href'])

                                    try:
                                        with urllib.request.urlopen(content.attrs['href']) as response:
                                            html_sub = response.read()
                                            html_soup_sub = BeautifulSoup(html_sub, "html.parser")
                                            div_title = html_soup_sub.find('div', class_="title")
                                            h1_title = div_title.find('h1')
                                            a_title = h1_title.find('a')
                                            small_title = h1_title.find('small')
                                            file_list.append(a_title.text + ' - ' + small_title.text)
                                            # if 'Get Premium' in h1.text:
                                            #     continue
                                    except urllib.error.HTTPError as e:
                                        print('HTTPError' + str(e))
                                elif img_match:
                                    jav2_data.thumbnail = content.attrs['href']


                            jav2_data.filesInfo = '、'.join(file_list)

                            if len(link_list) > 0:
                                jav2_data.downloadLinks = ' '.join(link_list)

                        jav2_data.print()

                    self.jav2_dao.export(jav2_data)
                    break

            return False


if __name__ == '__main__':
    jav2 = EntryRegisterJav2()
    jav2.main()
    jav2.main2()
    jav2.main3()

