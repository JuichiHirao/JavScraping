import re


class JavData:

    def __init__(self):
        self.id = -1
        self.url = ''
        self.title = ''
        self.postDate = None
        self.package = ''
        self.thumbnail = ''
        self.sellDate = None
        self.actress = ''
        self.maker = ''
        self.label = ''
        self.downloadLinks = ''
        self.createdAt = None
        self.updatedAt = None

    def get_date(self, line=''):
        arr = line.split('：')
        if len(arr) >= 2:
            result = re.search(".*[/-].*/.*", arr[1].strip())
            if result:
                return arr[1].strip()

        return ''

    def get_text(self, line=''):
        arr = line.split('：')
        if len(arr) >= 2:
            return arr[1].strip()

        return ''

    def print(self):
        print('【' + self.title + '】')
        print('  date    [' + str(self.sellDate) + ']')
        print('  actress [' + self.actress + ']')
        print('  maker   [' + self.maker + ']')
        print('  label   [' + self.label + ']')
        print('  post    [' + str(self.postDate) + ']')
        print('  url     [' + self.url + ']')
        print(' ')


class Jav2Data:

    def __init__(self):
        self.id = -1
        self.title = ''
        self.downloadLinks = ''
        self.kind = ''
        self.createdAt = None
        self.updatedAt = None


class BjData:

    def __init__(self):
        self.id = -1
        self.title = ''
        self.postDate = None
        self.thumbnails = ''
        self.thumbnailsCount = 0
        self.downloadLink = ''
        self.url = ''
        self.postedIn = ''
        self.isDownloads = 0
        self.isSelection = 0
        self.createdAt = None
        self.updatedAt = None

    def print(self):
        print('【' + self.title + '】')
        print('  post_data     [' + str(self.postDate) + ']')
        print('  th count      [' + str(self.thumbnailsCount) + '] ' + self.thumbnails)
        print('  download_link [' + self.downloadLink + ']')
        print('  posted_in     [' + self.postedIn + ']')
        print('  url           [' + self.url + ']')
        print(' ')

