import os
import re
import mojimoji
from enum import IntEnum


class Property(IntEnum):
    NAME = 1
    GENDER = 2
    SKILL = 3
    COST = 4
    BELONGS = 5
    STATION = 6
    SUBJECT = 7
    SEND_DATE = 8
    SENDER = 9
    FILE_COUNT = 10
    FILE_MIME_TYPE = 11
    FILE_NAME = 12


PROPERTY_MATCH_GROUP = 3
HUMAN_PROPERTIES = {
    Property.NAME: ".?(氏\s*名|名\s*前|名(?!刺))",
    Property.GENDER: ".?(性\s*別)",
    Property.SKILL: ".?(ス\s*キ\s*ル)",
    Property.COST: ".?(単\s*金|単\s*価|金\s*額)",
    Property.BELONGS: ".?(所\s*属)",
    Property.STATION: ".?(最\s*寄.?駅?|駅)",
    # Property.SUBJECT: "(Subject:\[partner:.*\])(.*)",
    Property.SUBJECT: "(Subject)",
    Property.SEND_DATE: "(SendDate)",
    Property.SENDER: "(Sender)",
    Property.FILE_COUNT: "(FileCount)",
    Property.FILE_MIME_TYPE: "(MimeType)",
    Property.FILE_NAME: "(FileName)",
}

# MAIL_PROPERTIES = {
#     Property.SUBJECT: "(Subject:\[partner:.*\])(.*)",
#     Property.SEND_DATE: "(SendDate:)(.*)",
#     Property.SENDER: "(Sender:)(.*)",
#     Property.FILE_COUNT: "(FileCount:)(.*)",
#     Property.FILE_MIME_TYPE: "(MimeType:)(.*)",
#     Property.FILE_NAME: "(FileName:)(.*)",
# }

CHARACTER = "(.*)"

# TODO 改行されて項目がある場合。。。
# DELIMITER = "[ -\/:-@\[-`\{-\~\n]"
DELIMITER = "\W*"

# 文脈に文字がでてきたときに除外するため助詞を定義
PARTICLE = "(?!(が|の|を|に|へ|と|から|より|で|や))"


class ExtractRegex:
    def __init__(self):

        # if Property.NAME == 1:
        #     print("jjjjjjjjjj")
        # print("nananana",Property.NAME)
        # print("babab", HUMAN_PROPERTIES[Property.NAME]["patter"])
        # print("babab", HUMAN_PROPERTIES[Property.NAME]["no"])
        # print("count", len(HUMAN_PROPERTIES))
        # print(HUMAN_PROPERTIES[Property.NAME]["patter"])
        # exit()

        self.checked = {}

        for index in range(len(HUMAN_PROPERTIES)):
            self.checked[index + 1] = False

        # Human property
        self.__name = None
        self.__skill = None
        self.__cost = None
        self.__belongs = None
        self.__station = None
        self.__gender = None

        # mail property
        self.__subject = None
        self.__send_date = None
        self.__sender = None
        self.__file_count = None
        self.__file_mime_type = []
        self.__file_name = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        self.__name = val

    @name.deleter
    def name(self):
        del self.__name

    @property
    def skill(self):
        return self.__skill

    @skill.setter
    def skill(self, val):
        self.__skill = val

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, val):
        self.__cost = val

    @property
    def belongs(self):
        return self.__belongs

    @belongs.setter
    def belongs(self, val):
        self.__belongs = val

    @property
    def station(self):
        return self.__station

    @station.setter
    def station(self, val):
        self.__station = val

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, val):
        self.__gender = val

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, val):
        self.__subject = val

    @property
    def send_date(self):
        return self.__send_date

    @send_date.setter
    def send_date(self, val):
        self.__send_date = val

    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, val):
        self.__sender = val

    @property
    def file_count(self):
        return self.__file_count

    @file_count.setter
    def file_count(self, val):
        self.__file_count = val

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, val):
        self.__file_name.append(val)

    @property
    def file_mime_type(self):
        return self.__file_mime_type

    @file_mime_type.setter
    def file_mime_type(self, val):
        self.__file_mime_type.append(val)

    """
    項目ごとにカスタマイズする可能性考慮
    """

    def check_patter(self, line):
        """

        :type line: string
        """
        for props in HUMAN_PROPERTIES:
            if self.__is_checked(props) is True:
                continue

            patter = re.compile(r"{}{}{}{}".format(HUMAN_PROPERTIES[props], DELIMITER, PARTICLE, CHARACTER))

            # print(patter)
            match = patter.search(line)

            if match is not None:
                _character = match.group(PROPERTY_MATCH_GROUP)
                self.__set_val(props, _character)

    def __is_checked(self, props):
        return self.checked[props]

    def __set_val(self, props, character):
        self.checked[props] = True

        if Property.NAME is props:
            self.name = character

        elif Property.SKILL is props:
            self.skill = character

        elif Property.COST is props:
            self.cost = character

        elif Property.STATION is props:
            self.station = character

        elif Property.GENDER is props:
            self.gender = character
            print("gender", character)

        elif Property.BELONGS is props:
            self.belongs = character

        elif Property.SUBJECT is props:
            self.subject = character

        elif Property.SENDER is props:
            self.sender = character

        elif Property.SEND_DATE is props:
            self.send_date = character

        elif Property.FILE_COUNT is props:
            self.file_count = character

        elif Property.FILE_MIME_TYPE is props:
            self.file_mime_type = character

        elif Property.FILE_NAME is props:
            self.file_name = character


if __name__ == "__main__":

    DIRPATH = "../mail/emails/"

    dir_list = os.listdir(DIRPATH)

    for txt in dir_list:
        print("--------------初め-------------------\n")
        with open(DIRPATH + txt, "r", encoding="utf-8") as fp:
            line = fp.read()

            lines = line.split('\n')
            ext = ExtractRegex()

            for l in lines:
                # 全角から半角へ変換
                l_to_han = mojimoji.zen_to_han(l, kana=False)
                ext.check_patter(l_to_han)

                # 複数できない項目があった場合はエラーで通知しておくか

            print(ext.name)
            print(ext.station)
            print(ext.skill)
            print(ext.cost)
            print(ext.belongs)
            print(ext.subject)
            print(ext.send_date)
            print(ext.sender)
            print(ext.file_count)
            print(ext.file_name)
            print(ext.file_mime_type)
            print(ext.checked)
        print("-------------終わり-------------------\n")
