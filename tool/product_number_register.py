from db import mysql_control
import re


class ProductNumberRegister:

    def __init__(self):
        self.makers = []

        self.db = mysql_control.DbMysql()
        self.makers = self.db.get_movie_maker()

    def parse(self, title):
        match = re.search('[0-9A-Za-z]*-[0-9A-Za-z]* ', title)

        p_number = ''
        if match:
            p_number = match.group().strip()
        else:
            for maker in self.makers:
                if len(maker.matchStr) <= 0:
                    continue

                if re.search(maker.matchStr, title):
                    m = re.search(maker.matchProductNumber, title)
                    if m:
                        p_number = m.group()
                if re.search('FC2 ', title):
                    m = re.search('[0-9]{6}', title)
                    if m:
                        p_number = m.group()

        # print(p_number + ' ' + title)

        return p_number

    def batch(self):

        javs = self.db.get_javs_nothing_product_number()
        for jav in javs:

            p_number = self.parse(jav.title)

            if len(p_number) > 0:
                self.db.update_jav_product_number(jav.id, p_number)


if __name__ == '__main__':
    p_register = ProductNumberRegister()
    p_register.batch()
