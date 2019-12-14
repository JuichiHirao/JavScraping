# coding:utf-8
import urllib.request
import os
from time import sleep
from javcore import db


class CollectImageBj:

    def __init__(self):

        self.store_path = "C:\\mydata\\bj-jpeg"

        self.bj_dao = db.bj.BjDao()
        self.bjs = self.bj_dao.get_where_agreement('WHERE is_downloads IS NULL OR is_downloads = 0 ORDER BY post_date')

    def get_images(self):

        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        for bj in self.bjs:
            print(bj.url)

            thumbnail_list = bj.thumbnails.split(' ')
            for thumbnail in thumbnail_list:
                if len(thumbnail.strip()) <= 0:
                    print('thumbnailの設定なし id [{}]'.format(bj.id))
                    continue

                print(thumbnail)
                try:
                    filename = thumbnail[thumbnail.rfind("/") + 1:]
                    pathname = os.path.join(self.store_path, filename)
                    sleep(1)
                    print('start urlretrieve')
                    result = urllib.request.urlretrieve(thumbnail, pathname)
                    print('end urlretrieve')
                except:
                    print('error [' + thumbnail + ']')
                    sleep(10)
                    with urllib.request.urlopen(thumbnail) as response:
                        html = response.read()
                    result = urllib.request.urlretrieve(thumbnail, pathname)
                print(str(result))

            self.bj_dao.update_is_download(bj.id, 1)


if __name__ == '__main__':
    collect_bj = CollectImageBj()
    collect_bj.get_images()
