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
        self.is_check = True

    def test_parse_product_number(self):
        # javs = self.db.get_javs_nothing_product_number()
        javs = self.db.get_javs_all()

        product_number_tool = product_number_register.ProductNumberRegister()
        for jav in javs:
            before_p = jav.productNumber
            # jav.productNumber = product_number_tool.parse(jav.title)
            jav.productNumber = product_number_tool.parse2(jav)

            if before_p == jav.productNumber:
                continue

            # print(str(before_p) + ' -> ' + str(jav.productNumber.strip()) + '    ' + jav.title)

            # if len(jav.productNumber) <= 0:
            #     filename = jav.downloadLinks.split(' ')[0].split('/')[-1]
            #     print('    ' + filename)

            if not self.is_check:
                self.db.update_jav2(jav)

    def get_single(self):

        jav = self.db.get_jav_by_id(3276)
        jav.print()
        product_number_tool = product_number_register.ProductNumberRegister()

        jav.productNumber = product_number_tool.parse(jav.title)
        print(jav.productNumber)
        if not self.is_check:
            self.db.update_jav2(jav)


if __name__ == '__main__':
    entry_register = TestEntryRegisterJav()
    entry_register.test_parse_product_number()
    # entry_register.get_single()

