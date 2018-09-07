# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from db import mysql_control
from data import site_data
import re


class AutoMakerRegister:

    def __init__(self):

        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options, executable_path='c:\\SHARE\\chromedriver.exe')

        # self.main_url = "http://maddawgjav.net/"

        self.db = mysql_control.DbMysql()
        self.is_check = True
        self.target_max = 1;

    def register(self):

        javs = self.db.get_javs_all()

        idx = 0
        for jav in javs:

            if not (jav.isParse2 == -3 or jav.isParse2 == -4):
                continue

            print('[' + str(jav.id) + ']' + jav.title)

            if idx < 0 or idx > self.target_max:
                break

            '''
              '  , name, match_name, label, kind ' \
              '  , match_str, match_product_number, site_kind, replace_words ' \
              '  , p_number_gen, registered_by ' \
            '''

            m_p = re.search('[A-Z0-9]{3,5}-[A-Z0-9]{3,4}', jav.title, re.IGNORECASE)
            match_str = ''
            if m_p:
                p_number = m_p.group()
                match_str = p_number.split('-')[0]

            maker = site_data.MovieMakerData()

            maker.name = jav.maker
            maker.matchName = jav.maker
            maker.label = jav.label
            maker.kind = 1
            maker.matchStr = match_str.upper()
            maker.registeredBy = 'AUTO ' + datetime.now().strftime('%Y-%m-%d')
            maker.print()

            if not self.is_check:
                self.db.export_maker(maker)

            idx = idx + 1


if __name__ == '__main__':
    auto_maker_register = AutoMakerRegister()
    auto_maker_register.register()
