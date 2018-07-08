import yaml
import mysql.connector
import jav_data
import time

class DbMysql:

    def __init__(self, table_name=''):
        self.max_time = 0
        self.user = ''
        self.password = ''
        self.hostname = ''
        self.dbname = ''
        self.cursor = None

        self.conn = self.get_conn()

        # テーブル名が指定されていた場合は取得済みの回数を設定
        if len(table_name) > 0:
            self.table_name = table_name
            max_time = self.db.prepare("SELECT max(times) FROM " + table_name)
            for row in max_time():
                self.max_time = int(row[0])

        self.cursor = self.conn.cursor()

    def get_conn(self):

        with open('credentials.yml') as file:
            obj = yaml.load(file)
            self.user = obj['user']
            self.password = obj['password']
            self.hostname = obj['hostname']
            self.dbname = obj['dbname']

        return mysql.connector.connect(user=self.user, password=self.password,
                                            host=self.hostname, database=self.dbname)

    def exist_title(self, title, table_name):
        sql = 'SELECT title FROM ' + table_name + ' WHERE title = %s '

        self.cursor.execute(sql, (title, ))
        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        exist_flag = False

        if rs is not None:
            for row in rs:
                exist_flag = True
                break

        self.conn.commit()

        return exist_flag

    def get_url_javs(self):

        sql = 'SELECT id, url FROM jav WHERE package IS NULL AND download_links IS NULL ORDER BY post_date'

        self.cursor.execute(sql)

        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        javs = []
        for row in rs:
            jav = jav_data.JavData()
            jav.id = row[0]
            jav.url = row[1]
            javs.append(jav)

        self.conn.commit()

        return javs

    def update_jav(self, javData):

        sql = 'UPDATE jav ' \
                '  SET package = %s ' \
                '    , thumbnail = %s ' \
                '    , download_links = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (javData.package, javData.thumbnail, javData.downloadLinks, javData.id))
        print("jav update id [" + str(javData.id) + "]")

        self.conn.commit()

    def export_jav(self, javData):

        sql = 'INSERT INTO jav (title, post_date ' \
                ', sell_date, actress, maker, label, url) ' \
                ' VALUES(%s, %s, %s, %s, %s, %s, %s)'

        self.cursor.execute(sql, (javData.title, javData.postDate
                            , javData.sellDate, javData.actress
                            , javData.maker, javData.label
                            , javData.url))

        self.conn.commit()

    def export_bj(self, bjData):

        sql = 'INSERT INTO bj(title, post_date ' \
                ', thumbnails, thumbnails_count, download_link, url, posted_in) ' \
                ' VALUES(%s, %s, %s, %s, %s, %s, %s)'

        self.cursor.execute(sql, (bjData.title, bjData.postDate
                            , bjData.thumbnails, bjData.thumbnailsCount
                            , bjData.downloadLink, bjData.url
                            , bjData.postedIn))

        self.conn.commit()
