# coding:utf-8
import urllib.request
from db import mysql_control
import os


class CollectImageBj:

    def __init__(self):

        self.store_path = "/Users/juichihirao/bj-jpeg"

        self.db = mysql_control.DbMysql()

        self.bjs = self.db.get_url_bjs()

    def get_images(self):

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        for bj in self.bjs:
            print(bj.url)

            thumbnail_list = bj.thumbnails.split(' ')
            for thumbnail in thumbnail_list:

                print(thumbnail)
                filename = thumbnail[thumbnail.rfind("/") + 1:]
                pathname = os.path.join(self.store_path, filename)
                result = urllib.request.urlretrieve(thumbnail, pathname)
                print(str(result))

            bj.isDownloads = 1
            self.db.update_bj(bj)


if __name__ == '__main__':
    collect_bj = CollectImageBj()
    collect_bj.get_images()
