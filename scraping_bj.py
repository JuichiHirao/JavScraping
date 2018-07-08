# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import yaml

options = Options()
options.add_argument('--headless')

# ブラウザをheadlessで開く。
driver = webdriver.Chrome(chrome_options=options)

start = idx = 1

main_url = ''
with open('site_bj.yml') as file:
    obj = yaml.load(file)
    main_url = obj['site_url']

if len(main_url) <= 0:
    print('no yaml')
    exit(-1)

end = start + 2
current_url = ''
for idx in range(start, end):
    if idx <= 1:
        driver.get(main_url)
    else:
        page_url = current_url + "/page/" + str(idx) + "/"
        driver.get(page_url)

    if idx == start:
        sleep(5)

    current_url = driver.current_url
    print(current_url)
    for entry in driver.find_elements_by_css_selector('.hentry'):

        # <time class="entry-date" datetime="2018-07-07T08:21:46+00:00">2018-07-07</time>
        for h2 in entry.find_elements_by_tag_name('h2'):
            for a in h2.find_elements_by_tag_name('a'):
                title_url = a.get_attribute('href')
            print(h2.text + ' ' + title_url)
            break

        # <img class="alignnone size-full wp-image-49866 aligncenter" src="http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-2018070610.jpg" alt="" width="1004" height="680" srcset="http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-2018070610.jpg 1004w, http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-2018070610-300x203.jpg 300w, http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-2018070610-768x520.jpg 768w" sizes="(max-width: 1004px) 100vw, 1004px">
        # <img class="alignnone size-full wp-image-49867 aligncenter" src="http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-20180706102.jpg" alt="" width="992" height="682" srcset="http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-20180706102.jpg 992w, http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-20180706102-300x206.jpg 300w, http://www.cam18.top/wp-content/uploads/2018/07/KOREAN-BJ-20180706102-768x528.jpg 768w" sizes="(max-width: 992px) 100vw, 992px">
        for time in entry.find_elements_by_tag_name('time'):
            post_date = time.get_attribute('datetime')
            print("post_date " + post_date)

        for a in entry.find_elements_by_tag_name('a'):
            contents_link = a.get_attribute('href')
            if re.search('uploadgig.com', contents_link):
                print(contents_link)

        for a in entry.find_elements_by_tag_name('img'):
            contents_link = a.get_attribute('src')
            if re.match('.*jpg$', contents_link):
                print("img " + contents_link)

        try:
            for footer in entry.find_elements_by_tag_name('footer'):
                for a in footer.find_elements_by_tag_name('a'):
                    print("POSTED IN " + a.text)
        except:
            print("exept")

    idx = idx + 1
