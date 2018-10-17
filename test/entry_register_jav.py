# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
from javcore import db
from javcore import tool
from javcore import data
from scraping import collect_jav


class TestEntryRegisterJav:

    def __init__(self):

        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='c:\\SHARE\\chromedriver.exe')

        # self.main_url = "http://maddawgjav.net/"

        self.jav_dao = db.jav.JavDao()
        self.import_dao = db.import_dao.ImportDao()
        # self.is_check = True
        self.is_check = False
        self.target_max = 50;

    def test_parse_product_number(self):

        javs = self.jav_dao.get_all()

        p_number_tool = tool.p_number.ProductNumber()
        idx = 0
        for jav in javs:

            if jav.isSite > 0 or jav.isParse2 > 0:
                continue
            if not jav.isSelection == 1:
                continue

            before_p = jav.productNumber
            jav.productNumber, seller, sell_date, match_maker, ng_reason = p_number_tool.parse_and_fc2(jav, self.is_check)

            idx = idx + 1

            if idx < 0 or idx > self.target_max:
                break

            if jav.isSite == 0 and len(seller) > 0:
                sell_date = datetime.strptime(sell_date, '%Y/%m/%d')
                if not self.is_check:
                    self.jav_dao.update_site_info(seller, sell_date, jav.id)
                print('update [' + str(jav.id) + '] label [' + seller + ']  sell_date [' + str(sell_date) + '] ' + str(self.is_check))

            if before_p == jav.productNumber:
                continue

            if len(jav.productNumber) <= 0:
                continue

            if not self.is_check:
                self.jav_dao.update_product_number(jav.id, jav.productNumber)

            print('update [' + str(jav.id) + '] p_number [' + str(before_p) + ']  --> [' + jav.productNumber + '] ' + str(self.is_check))

    def test_update_download_link(self):

        javs = self.db.get_url_jav(805)

        c_jav = collect_jav.CollectJav()
        for jav in javs:
            self.driver.get(str(jav.url))

            sleep(8)

            c_jav.execute_info(jav, self.driver)

    def test_parse_product_number_retry_error(self):

        where = ' WHERE is_selection = 1 ORDER BY post_date '
        javs = self.db.get_jav_where_agreement(where)

        p_number_tool = tool.p_number.ProductNumber()
        idx = 0
        for jav in javs:

            if jav.isParse2 > 0:
                continue

            jav.productNumber, seller, sell_date, match_maker, ng_reason = p_number_tool.parse_and_fc2(jav, self.is_check)

            if jav.isSite == 0 and len(seller) > 0:
                sell_date = datetime.strptime(sell_date, '%Y/%m/%d')
                if not self.is_check:
                    self.jav_dao.update_site_info(seller, sell_date, jav.id)
                print('update [' + str(jav.id) + '] label [' + seller + ']  sell_date [' + sell_date + '] ' + str(self.is_check))

            # print('update [' + str(jav.id) + '] p_number [' + str(before_p) + ']  --> [' + jav.productNumber + '] ' + str(self.is_check))
            if not self.is_check:
                self.jav_dao.update_product_number(jav.id, jav.productNumber)

            idx = idx + 1

            if idx < 0 or idx > self.target_max:
                break

    def get_hey(self):

        p_number_tool = tool.p_number.ProductNumber()
        javs = self.jav_dao.get_where_agreement('WHERE title like "%-PPV%" ')
        # javs = self.db.get_jav_hey()

        for jav in javs:
            # jav.print()

            before_p = jav.productNumber
            jav.productNumber, seller, sell_date, match_maker, ng_reason = p_number_tool.parse_and_fc2(jav, self.is_check)
            print('  ' + jav.productNumber + ' <-- ' + before_p)
            print('')

            if jav.isSite == 0 and len(seller) > 0:
                sell_date = datetime.strptime(sell_date, '%Y/%m/%d')
                if not self.is_check:
                    self.jav_dao.update_site_info(seller, sell_date, jav.id)
                print('update [' + str(jav.id) + '] label [' + seller + ']  sell_date [' + sell_date + '] ' + str(self.is_check))

            if not self.is_check:
                self.jav_dao.update_product_number(jav.id, jav.productNumber)

    def get_jav_where_agreement(self):

        # where = '  where product_number is null or product_number = \'\''
        # where = '  where id in (5755, 5723, 5721, 5720, 5719, 6395, 6394, 6393, 6392, 6391)'
        where = '  where id in (1947)'
        javs = self.db.get_jav_where_agreement(where)

        p_number_tool = tool.p_number.ProductNumber()
        for jav in javs:
            # jav.title = jav.title + ' ' + jav.package
            # jav = self.db.get_jav_by_id(313)
            jav.print()

            jav.productNumber, seller, sell_date, match_maker, ng_reason = p_number_tool.parse_and_fc2(jav, self.is_check)

            if jav.isSite == 0 and len(seller) > 0:
                sell_date = datetime.strptime(sell_date, '%Y/%m/%d')
                if not self.is_check:
                    self.jav_dao.update_site_info(seller, sell_date, jav.id)
                print('update [' + str(jav.id) + '] label [' + seller + ']  sell_date [' + sell_date + '] ' + str(self.is_check))

            # jav.productNumber = product_number_tool.parse2(jav.title)
            print('  p_num [' + jav.productNumber + ']')
            if not self.is_check:
                self.jav_dao.update_product_number(jav.id, jav.productNumber)

    def get_single(self):

        jav = self.db.get_jav_by_id(1372)
        # jav.title = jav.title + ' ' + jav.package
        # jav = self.db.get_jav_by_id(313)
        jav.print()
        p_number_tool = tool.p_number.ProductNumber()

        jav.productNumber, seller, sell_date, match_maker, ng_reason = p_number_tool.parse_and_fc2(jav, self.is_check)

        if jav.isSite == 0 and len(seller) > 0:
            sell_date = datetime.strptime(sell_date, '%Y/%m/%d')
            if not self.is_check:
                self.jav_dao.update_site_info(seller, sell_date, jav.id)
            print('update [' + str(jav.id) + '] label [' + seller + ']  sell_date [' + sell_date + '] ' + str(self.is_check))

        print(jav.productNumber)
        if not self.is_check:
            self.jav_dao.update_product_number(jav.id, jav.productNumber)

    def get_single_from_import(self):

        import_id = 89
        p_number_tool = tool.p_number.ProductNumber()
        jav = data.JavData()
        match_maker = data.MakerData()
        jav.title = self.db.get_import_copytext_by_id(import_id)

        jav.productNumber, seller, sell_date, match_maker, ng_reason = p_number_tool.parse_and_fc2(jav, self.is_check)
        print(jav.productNumber + ' title [' + jav.title + ']')
        if match_maker is None:
            print('no match maker '  ' title [' + jav.title + ']')
            return

        if not self.is_check:
            self.import_dao.update_p_number_info(import_id, jav.productNumber, match_maker)


if __name__ == '__main__':
    entry_register = TestEntryRegisterJav()
    # entry_register.get_single()
    # entry_register.get_jav_where_agreement()
    # entry_register.get_hey()
    entry_register.test_parse_product_number()
    # entry_register.test_parse_product_number_retry_error()
    # entry_register.test_update_download_link()
    # entry_register.get_single_from_import()

