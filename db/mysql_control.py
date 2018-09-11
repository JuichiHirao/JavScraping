import yaml
import mysql.connector
from data import site_data


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

    def exist_title_and_kind(self, title, kind, table_name):
        sql = 'SELECT title FROM ' + table_name + ' WHERE title = %s and kind = %s'

        self.cursor.execute(sql, (title, kind, ))
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
        # sql = 'SELECT id, url FROM jav WHERE ID = 811 ORDER BY post_date'

        self.cursor.execute(sql)

        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        javs = []
        for row in rs:
            jav = site_data.JavData()
            jav.id = row[0]
            jav.url = row[1]
            javs.append(jav)

        self.conn.commit()

        return javs

    def get_url_jav(self, id):

        sql = 'SELECT id, url FROM jav WHERE ID = %s '

        self.cursor.execute(sql, (id, ))

        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        javs = []
        for row in rs:
            jav = site_data.JavData()
            jav.id = row[0]
            jav.url = row[1]
            javs.append(jav)

        self.conn.commit()

        return javs

    def is_exist_maker(self, match_str):

        if len(match_str) <= 0:
            return False

        sql = 'SELECT id ' \
              '  FROM maker ' \
              '  WHERE match_str = %s '

        self.cursor.execute(sql, (match_str,))

        rs = self.cursor.fetchall()

        if rs:
            return True

        return False

    def get_movie_maker(self):

        sql = 'SELECT id ' \
              '  , name, match_name, label, kind ' \
              '  , match_str, match_product_number, site_kind, replace_words ' \
              '  , p_number_gen, registered_by ' \
              '  , created_at, updated_at ' \
              '  , created_at, updated_at ' \
              '  FROM maker ' \
              '  WHERE deleted = 0 ' \
              '  ORDER BY id'

        self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        makers = []
        for row in rs:
            maker = site_data.MovieMakerData()
            maker.id = row[0]
            maker.name = row[1]
            maker.matchName = row[2]
            maker.label = row[3]
            maker.kind = row[4]
            maker.matchStr = row[5]
            maker.matchProductNumber = row[6]
            maker.siteKind = row[7]
            maker.replaceWords = row[8]
            maker.pNumberGen = row[9]
            maker.registeredBy = row[10]
            maker.createdAt = row[11]
            maker.updatedAt = row[12]
            makers.append(maker)

        self.conn.commit()

        return makers

    def export_maker(self, maker):

        sql = 'INSERT INTO maker ( ' \
              '  name, match_name, label, kind ' \
              '  , match_str, match_product_number, site_kind, replace_words ' \
              '  , p_number_gen, registered_by ' \
              '  ) ' \
              '  VALUES ( ' \
              '  %s, %s, %s, %s ' \
              '  , %s, %s, %s, %s ' \
              '  , %s, %s ' \
              '  ) '

        self.cursor.execute(sql, (maker.name, maker.matchName, maker.label, maker.kind
                                  , maker.matchStr, maker.matchProductNumber, maker.siteKind, maker.replaceWords
                                  , maker.pNumberGen, maker.registeredBy
                                  ))

        self.conn.commit()

    def __get_sql_select(self):
        sql = 'SELECT id, title, post_date, package ' \
                '  , thumbnail, sell_date, actress, maker ' \
                '  , label, download_links, url, is_selection' \
                '  , product_number, rating, is_site ' \
                '  , is_parse2, makers_id ' \
                '  , created_at, updated_at ' \
                '  FROM jav '

        return sql

    def __get_list(self, rs):

        javs = []
        for row in rs:
            jav = site_data.JavData()
            jav.id = row[0]
            jav.title = row[1]
            jav.postDate = row[2]
            jav.package = row[3]
            jav.thumbnail = row[4]
            jav.sellDate = row[5]
            jav.actress = row[6]
            jav.maker = row[7]
            jav.label = row[8]
            jav.downloadLinks = row[9]
            jav.url = row[10]
            jav.isSelection = row[11]
            jav.productNumber = row[12]
            jav.rating = row[13]
            jav.isSite = row[14]
            jav.isParse2 = row[15]
            jav.makersId = row[16]
            jav.createdAt = row[17]
            jav.updatedAt = row[18]
            javs.append(jav)

        return javs

    def get_jav_hey(self):

        sql = self.__get_sql_select()
        sql = sql + '  WHERE title like "%-PPV%" '

        self.cursor.execute(sql)

        rs = self.cursor.fetchall()

        javs = self.__get_list(rs)

        if javs is None or len(javs) <= 0:
            return None

        return javs

    def get_jav_by_id(self, id):

        sql = self.__get_sql_select()
        sql = sql + '  WHERE id = %s '

        self.cursor.execute(sql, (id, ))

        rs = self.cursor.fetchall()

        javs = self.__get_list(rs)

        if javs is None or len(javs) <= 0:
            return None

        return javs[0]

    def get_javs_nothing_product_number(self):

        sql = self.__get_sql_select()
        sql = sql + '  WHERE product_number IS NULL or LENGTH(product_number) <= 0 ' \
                    '  ORDER BY post_date'

        self.cursor.execute(sql)
        rs = self.cursor.fetchall()

        javs = self.__get_list(rs)

        return javs

    def get_javs_all(self):

        sql = self.__get_sql_select()
        sql = sql + '  ORDER BY post_date'

        self.cursor.execute(sql)
        rs = self.cursor.fetchall()

        javs = self.__get_list(rs)

        return javs

    def get_url_bjs(self):

        sql = 'SELECT id, thumbnails FROM bj WHERE is_downloads IS NULL OR is_downloads = 0 ORDER BY post_date'

        self.cursor.execute(sql)

        # rowcountは戻りがあっても、正しい件数を取得出来ない
        # rowcount = self.cursor.rowcount
        rs = self.cursor.fetchall()

        bjs = []
        for row in rs:
            bj = site_data.BjData()
            bj.id = row[0]
            bj.thumbnails = row[1]
            bjs.append(bj)

        self.conn.commit()

        return bjs

    def update_bj(self, bjData):

        sql = 'UPDATE bj ' \
                '  SET is_downloads = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (bjData.isDownloads, bjData.id))
        print("bj isDownloads update id [" + str(bjData.id) + "]")

        self.conn.commit()

    def update_jav_product_number(self, id, product_number):

        sql = 'UPDATE jav ' \
                '  SET product_number = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (product_number, id))
        print("jav update id [" + str(id) + "]")

        self.conn.commit()

    def update_jav_checked_ok(self, is_parse2, makers_id, javData):

        sql = 'UPDATE jav ' \
                '  SET is_parse2 = %s ' \
                '    , scraping.jav.makers_id = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (is_parse2, makers_id, javData.id))
        print("jav update id [" + str(javData.id) + "]")

        self.conn.commit()

    def update_jav(self, javData):

        sql = 'UPDATE jav ' \
                '  SET package = %s ' \
                '    , thumbnail = %s ' \
                '    , download_links = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (javData.package, javData.thumbnail, javData.downloadLinks, javData.id))
        print("jav update id [" + str(javData.id) + "]")

        self.conn.commit()

    def update_jav2(self, javData):

        sql = 'UPDATE jav ' \
                '  SET product_number = %s ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (javData.productNumber, javData.id))
        print("jav update id [" + str(javData.id) + "]")

        self.conn.commit()

    def update_jav_label_selldate(self, label, sellDate, javData):

        sql = 'UPDATE jav ' \
                '  SET label = %s, sell_date = %s, is_site = 1 ' \
                '  WHERE id = %s'

        self.cursor.execute(sql, (label, sellDate, javData.id))
        print("jav update id [" + str(javData.id) + "]")

        self.conn.commit()

    def export_jav(self, javData):

        sql = 'INSERT INTO jav (title, post_date ' \
                '  , sell_date, actress, maker, label' \
                '  , url, product_number, makers_id, is_parse2 ' \
                '  ) ' \
                ' VALUES(%s, %s' \
                '  , %s, %s, %s, %s' \
                '  , %s, %s, %s, %s' \
                ' )'

        self.cursor.execute(sql, (javData.title, javData.postDate
                            , javData.sellDate, javData.actress, javData.maker, javData.label
                            , javData.url, javData.productNumber, javData.makersId, javData.isParse2
                            ))

        self.conn.commit()

    def export_jav2(self, jav2Data):

        sql = 'INSERT INTO jav2 (title, download_links, kind, url, detail)' \
                ' VALUES(%s, %s, %s, %s, %s)'

        self.cursor.execute(sql, (jav2Data.title, jav2Data.downloadLinks, jav2Data.kind, jav2Data.url, jav2Data.detail))

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

    def update_import_by_id(self, id, product_number, match_maker):
        sql = 'UPDATE import ' \
                '  SET kind = %s ' \
                '   , match_product = %s ' \
                '   , product_number = %s ' \
                '   , maker = %s ' \
                '  WHERE id = %s '

        self.cursor.execute(sql, (match_maker.kind, match_maker.matchProductNumber, product_number, match_maker.get_maker(''), id))

        self.conn.commit()

    def get_import_copytext_by_id(self, id):
        sql = 'SELECT copy_text ' \
                '  FROM import ' \
                '  WHERE id = %s '

        self.cursor.execute(sql, (id, ))

        rs = self.cursor.fetchall()

        for row in rs:
            return row[0]

        return ''

