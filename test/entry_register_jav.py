# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
from db import mysql_control
from data import site_data
from tool import product_number_register


class TestEntryRegisterJav:

    def __init__(self):

        # options = Options()
        # options.add_argument('--headless')
        # self.driver = webdriver.Chrome(chrome_options=options)

        # self.main_url = "http://maddawgjav.net/"

        self.db = mysql_control.DbMysql()
        # self.is_check = True
        self.is_check = False

    def test_parse_product_number(self):
        # javs = self.db.get_javs_nothing_product_number()
        javs = self.db.get_javs_all()

        product_number_tool = product_number_register.ProductNumberRegister()
        idx = 0
        for jav in javs:

            if jav.isSite > 0 or jav.isParse2 > 0:
                continue
            before_p = jav.productNumber
            jav.productNumber, seller, sell_date, match_maker = product_number_tool.parse2(jav, self.is_check)

            if jav.isSite == 0 and len(seller) > 0:
                sellDate = datetime.strptime(sell_date, '%Y/%m/%d')
                if not self.is_check:
                    self.db.update_jav_label_selldate(seller, sellDate, jav)
                print('update [' + str(jav.id) + '] label [' + seller + ']  sell_date [' + sell_date + '] ' + str(self.is_check))

            if before_p == jav.productNumber:
                continue

            if len(jav.productNumber) <= 0:
                continue

            # print(str(before_p) + ' -> ' + str(jav.productNumber.strip()) + '    ' + jav.title)

            # if len(jav.productNumber) <= 0:
            #     filename = jav.downloadLinks.split(' ')[0].split('/')[-1]
            #     print('    ' + filename)

            if not self.is_check:
                self.db.update_jav2(jav)

            print('update [' + str(jav.id) + '] p_number [' + str(before_p) + ']  --> [' + jav.productNumber + '] ' + str(self.is_check))

            idx = idx + 1

            if idx > 50:
                break

    def test_parse_product_number_retry_error(self):

        javs = self.db.get_javs_all()

        product_number_tool = product_number_register.ProductNumberRegister()
        idx = 0
        for jav in javs:

            if not (jav.isSelection == 1 and jav.isParse2 < 0):
                continue

            jav.productNumber, seller, sell_date, match_maker, ng_reason = product_number_tool.parse2(jav, self.is_check)

            if jav.isSite == 0 and len(seller) > 0:
                sellDate = datetime.strptime(sell_date, '%Y/%m/%d')
                if not self.is_check:
                    self.db.update_jav_label_selldate(seller, sellDate, jav)
                print('update [' + str(jav.id) + '] label [' + seller + ']  sell_date [' + sell_date + '] ' + str(self.is_check))

            # print('update [' + str(jav.id) + '] p_number [' + str(before_p) + ']  --> [' + jav.productNumber + '] ' + str(self.is_check))
            if not self.is_check:
                self.db.update_jav2(jav)

            idx = idx + 1

            if idx > 5:
                break

    def get_single(self):

        jav = self.db.get_jav_by_id(3276)
        jav.print()
        product_number_tool = product_number_register.ProductNumberRegister()

        jav.productNumber = product_number_tool.parse(jav.title)
        print(jav.productNumber)
        if not self.is_check:
            self.db.update_jav2(jav)

    def get_single_from_import(self):

        import_id = 89
        product_number_tool = product_number_register.ProductNumberRegister()
        jav = site_data.JavData()
        match_maker = site_data.MovieMakerData()
        jav.title = self.db.get_import_copytext_by_id(import_id)

        jav.productNumber, seller, sell_date, match_maker = product_number_tool.parse2(jav, self.is_check)
        print(jav.productNumber + ' title [' + jav.title + ']')
        if match_maker is None:
            print('no match maker '  ' title [' + jav.title + ']')

        # if not self.is_check:
        self.db.update_import_by_id(import_id, jav.productNumber, match_maker)


if __name__ == '__main__':
    entry_register = TestEntryRegisterJav()
    # entry_register.test_parse_product_number()
    entry_register.test_parse_product_number_retry_error()
    # entry_register.get_single_from_import()

