# coding:utf-8
from datetime import datetime
import re
from javcore import db
from javcore import data
from javcore import common


class AutoMakerRegister:

    def __init__(self):

        self.env = common.Environment()
        self.driver = self.env.get_driver()

        self.jav_dao = db.jav.JavDao()
        self.maker_dao = db.maker.MakerDao()
        self.is_check = True
        # self.is_check = False
        self.target_max = 5

    def register(self):

        # where = ' WHERE id = 2512'
        # javs = self.jav_dao.get_where_agreement(where)
        javs = self.jav_dao.get_all()

        idx = 0
        for jav in javs:

            if not (jav.isParse2 == -3 or jav.isParse2 == -4):
                continue
            if not (jav.isSelection == 1 or jav.isSelection == 3):
                continue

            '''
              '  , name, match_name, label, kind ' \
              '  , match_str, match_product_number, site_kind, replace_words ' \
              '  , p_number_gen, registered_by ' \
            '''

            m_p = re.search('[A-Z0-9]{2,5}-[A-Z0-9]{2,4}', jav.title, re.IGNORECASE)
            match_str = ''
            if m_p:
                p_number = m_p.group()
                match_str = p_number.split('-')[0]
            else:
                print('[' + str(jav.id) + '] 対象のmatch_strが存在しません [A-Z0-9]{3,5}-[A-Z0-9]{3,4}の正規表現と一致しません' + jav.title)
                exit(-1)

            if len(match_str) > 0 and self.maker_dao.is_exist(match_str.upper()):
                print('[' + str(jav.id) + '] 発見!! [' + match_str + ']')
                continue

            idx = idx + 1
            if idx < 0 or idx > self.target_max:
                break

            maker = data.MakerData()

            maker.name = jav.maker.replace('/', '／')
            maker.matchName = jav.maker
            if jav.maker == jav.label:
                pass
            else:
                maker.label = jav.label
            maker.kind = 1
            maker.matchStr = match_str.upper()
            maker.registeredBy = 'AUTO ' + datetime.now().strftime('%Y-%m-%d')

            print('[' + str(jav.id) + ']' + jav.title)
            maker.print()

            if not self.is_check:
                self.maker_dao.export(maker)


if __name__ == '__main__':
    auto_maker_register = AutoMakerRegister()
    auto_maker_register.register()
