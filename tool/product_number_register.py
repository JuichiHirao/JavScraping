from db import mysql_control
import re


class ProductNumberRegister:

    def __init__(self):
        self.makers = []

        self.db = mysql_control.DbMysql()
        self.makers = self.db.get_movie_maker()

    def parse2(self, jav):

        p_number = ''
        # match = re.search('[0-9A-Za-z]*-[0-9A-Za-z]*', jav.title)
        if len(jav.maker.strip()) > 0:
            find_filter_maker = filter(lambda maker: maker.name == jav.maker, self.makers)
            find_list_maker = list(find_filter_maker)
            if len(find_list_maker) == 1:
                print('bingo maker match [' + jav.maker + ']' + find_list_maker[0].name)
            elif len(find_list_maker) > 1:
                find_filter_label = filter(lambda maker: maker.label == jav.label, find_list_maker)
                find_list_label = list(find_filter_label)
                len_label = len(find_list_label)
                if len_label == 1:
                    print('m and label match jav [' + jav.maker + ':' + jav.label + '] ' + find_list_label[0].name + ':' + find_list_label[0].label)
                elif len_label > 1:
                    print('many m and label match [' + jav.maker + '] ' + find_list_maker[0].name)
                # print(str(len(find_list_maker)) + ' ' + jav.maker)
        else:
            find_filter_maker = filter(lambda maker: len(maker.matchProductNumber.strip()) > 0 and re.search(maker.matchStr, jav.title) and re.search(maker.matchProductNumber, jav.title, flags=re.IGNORECASE), self.makers)
            find_list_maker = list(find_filter_maker)
            if len(find_list_maker) == 1:
                m = re.search(find_list_maker[0].matchProductNumber, jav.title, flags=re.IGNORECASE)
                p_number = m.group().strip()
                print(str(len(find_list_maker)) + ' [' + p_number + ']   ' + jav.title)
            elif len(find_list_maker) > 1:
                print(str(len(find_list_maker)) + ' many match ' + jav.title)
            elif len(find_list_maker) <= 0:
                print(str(len(find_list_maker)) + ' no match ' + jav.title)
                # if len(find_list_maker) == 14:
                #     print(str(len(find_list_maker)) + ' ' + jav.title)
                #     for maker in find_list_maker:
                #         print('    ' + maker.name + ':' + maker.label + '  【' + maker.matchProductNumber + '】' + jav.title)
                # else:
                #     print(str(len(find_list_maker)) + ' ' + jav.title)

        '''
        if match:
            p_number = match.group().strip()
        else:
            for maker in self.makers:
                if len(maker.matchStr) <= 0:
                    continue

                if re.search(maker.matchStr, jav.title):
                    # print('match ' + p_number + ' ' + maker.name + ' ' + maker.matchStr)
                    m = re.search(maker.matchProductNumber, title, flags=re.IGNORECASE)
                    if m:
                        if len(str(m.group())) > 0:
                            p_number = m.group()
                if re.search('FC2 ', title):
                    m = re.search('[0-9]{6}', title)
                    if m:
                        p_number = m.group()

        # print('[' + p_number + '] ' + title)
        '''

        return p_number

    def parse(self, title):
        match = re.search('[0-9A-Za-z]*-[0-9A-Za-z]*', title)

        p_number = ''

        if match:
            p_number = match.group().strip()
        else:
            for maker in self.makers:
                if len(maker.matchStr) <= 0:
                    continue

                if re.search(maker.matchStr, title):
                    # print('match ' + p_number + ' ' + maker.name + ' ' + maker.matchStr)
                    m = re.search(maker.matchProductNumber, title, flags=re.IGNORECASE)
                    if m:
                        if len(str(m.group())) > 0:
                            p_number = m.group()
                if re.search('FC2 ', title):
                    m = re.search('[0-9]{6}', title)
                    if m:
                        p_number = m.group()

        # print('[' + p_number + '] ' + title)

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
