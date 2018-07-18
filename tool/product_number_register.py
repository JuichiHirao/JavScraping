from db import mysql_control
import re


class ProductNumberRegister:

    def __init__(self):

        self.javs = []
        self.makers = []

        self.db = mysql_control.DbMysql()
        self.javs = self.db.get_range_javs(0, 3000)
        # self.javs = self.db.get_range_javs(1200, 1210)
        self.makers = self.db.get_movie_maker()

        # for idx, maker in enumerate(self.makers):
        #     if idx > 10:
        #         break
        #     print(maker.print())

    def parse(self):

        for jav in self.javs:

            match = re.search('[0-9A-Za-z]*-[0-9A-Za-z]* ', jav.title)

            p_number = ''
            if match:
                p_number = match.group().strip()
            else:
                for maker in self.makers:
                    if len(maker.matchStr) <= 0:
                        continue

                    if re.search(maker.matchStr, jav.title):
                        m = re.search(maker.matchProductNumber, jav.title)
                        if m:
                            p_number = m.group()
                    if re.search('FC2 ', jav.title):
                        m = re.search('[0-9]{6}', jav.title)
                        if m:
                            p_number = m.group()

            print(p_number + ' ' + jav.title)

            if len(p_number) > 0:
                self.db.update_jav_product_number(jav.id, p_number)



if __name__ == '__main__':
    p_register = ProductNumberRegister()
    p_register.parse()
