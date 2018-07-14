# coding:utf-8
import urllib.request
import db
import os

jpeg_path = "/Users/juichihirao/bj-jpeg"

db = db.DbMysql()

bjs = db.get_url_bjs()

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

for bj in bjs:
    print(bj.url)
    # driver.get(str(jav.url))

    thumbnail_list = bj.thumbnails.split(' ')
    for thumbnail in thumbnail_list:

        print(thumbnail)
        filename = thumbnail[thumbnail.rfind("/") + 1:]
        pathname = os.path.join(jpeg_path, filename)
        result = urllib.request.urlretrieve(thumbnail, pathname)
        print(str(result))

    bj.isDownloads = 1
    db.update_bj(bj)
