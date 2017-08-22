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


class FileProps(IntEnum):
    FILE = 0
    MIME_TYPE = 1
    NAME = 2


class MailProps(IntEnum):
    SUBJECT = 1
    SEND_DATE = 2
    SENDER = 3
    FILE_COUNT = 4

HUMAN_PROPERTIES_MATCH_GROUP = 2
HUMAN_PROPERTIES = {
    Property.NAME: ".?(氏\s*名|名\s*前|名(?!刺))",
    Property.GENDER: ".?(性\s*別)",
    Property.SKILL: ".?(ス\s*キ\s*ル(?!アップ))",
    Property.COST: ".?(単\s*金|単\s*価|金\s*額)",
    Property.BELONGS: ".?(所\s*属)",
    Property.STATION: ".?(最\s*寄.?駅?|駅)",
}

MAIL_PROPERTIES = r"Subject:\[partner:.*\](.*)\nSender:(.*)\nSendDate:(.*)"
FILE_PROPERTIES = r"(.*)\[MimeType:(.+)FileName:(.+)\]"
FILE_COUNT = r"FileCount:(\d)"
MAIL_ADDRESS = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})"


CHARACTER = "(.*)"

# TODO 改行されて項目がある場合。。。
DELIMITER = "[ -\/:-@\[-`\{-\~\n 】：]"
# DELIMITER = "\W*"

# 文脈に文字がでてきたときに除外するため助詞を定義
PARTICLE = "(?!(が|の|を|に|へ|と|から|より|で|や))"


class MailRegex:
    END_TO_HEADER = "__end_mail_header__"
    START_TO_HEADER = "__start_mail_header__"

    def __init__(self):

        self.checked = {}

        for index in range(len(HUMAN_PROPERTIES)):
            self.checked[index + 1] = False

        # Human property
        # 複数人がいることも想定してリスト形式で定義
        self.__name = []
        self.__skill = []
        self.__cost = []
        self.__belongs = []
        self.__station = []
        self.__gender = []

        # mail property
        self.__subject = None
        self.__send_date = None
        self.__sender = None
        self.__mail_address = None
        self.__file_count = 0
        self.__file_mime_type = []
        self.__file_name = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        self.__name.append(val)
        # self.__name = val

    @name.deleter
    def name(self):
        del self.__name

    @property
    def skill(self):
        return self.__skill

    @skill.setter
    def skill(self, val):
        self.__skill.append(val)
        # self.__skill = val

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, val):
        # self.__cost = val
        self.__cost.append(val)

    @property
    def belongs(self):
        return self.__belongs

    @belongs.setter
    def belongs(self, val):
        # self.__belongs = val
        self.__belongs.append(val)

    @property
    def station(self):
        return self.__station

    @station.setter
    def station(self, val):
        # self.__station = val
        self.__station.append(val)

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, val):
        # self.__gender = val
        self.__gender.append(val)

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
    def mail_address(self):
        return self.__mail_address

    @mail_address.setter
    def mail_address(self):
        if self.sender is not None:
            _mail_address_match = re.compile(MAIL_ADDRESS).search(self.sender)
            self.__mail_address = _mail_address_match[1]
        return self.__mail_address

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

    def mail_patter(self, mail_headers):

        _headers = mail_headers.split('\n\n', MailProps.SEND_DATE)

        _mail_match = re.compile(MAIL_PROPERTIES).search(_headers[0])

        if _mail_match is not None:
            self.subject = _mail_match.group(MailProps.SUBJECT)
            self.sender = _mail_match.group(MailProps.SENDER)
            self.send_date = _mail_match.group(MailProps.SEND_DATE)

        if len(_headers) > 1:
            # Fileあり
            _file_match = re.compile(FILE_COUNT).search(_headers[1])
            if _file_match is not None:
                self.file_count = _file_match.group(1)

            _file_props_match = re.compile(FILE_PROPERTIES).findall(_headers[1])
            if len(_file_props_match) is not 0:
                for val in _file_props_match:
                    self.file_mime_type = val[FileProps.MIME_TYPE]
                    self.file_name = val[FileProps.NAME]

    def check_patter(self, line):
        """

        :type line: string
        """
        for props in HUMAN_PROPERTIES:
            # 複数人の場合も想定してこのチェックは外す
            # if self.__is_checked(props) is True:
            #     continue

            patter = re.compile(fr"{HUMAN_PROPERTIES[props]}{DELIMITER}{PARTICLE}{CHARACTER}")

            # TODO 複数人も想定して対応する
            match = patter.findall(line)

            if len(match) is not 0:
                for v in match:
                    _character = v[HUMAN_PROPERTIES_MATCH_GROUP]
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

        elif Property.BELONGS is props:
            self.belongs = character


def main():
    DIRPATH = "../mail/emails/"

    dir_list = os.listdir(DIRPATH)

    for txt in dir_list:
        print("--------------初め-------------------\n")
        with open(DIRPATH + txt, "r", encoding="utf-8") as fp:

            mail_regex = MailRegex()

            # メールヘッダー読み込み
            line_header = ""
            while True:
                line = fp.readline()
                # print(line)
                if line.find(MailRegex.START_TO_HEADER) > -1:
                    continue

                if line.find(MailRegex.END_TO_HEADER) > -1:
                    break

                line_header += line

            to_han_header = mojimoji.zen_to_han(line_header, kana=False)
            mail_regex.mail_patter(to_han_header)

            # メールヘッダー以降を読み込み
            body = fp.read()
            to_han_body = mojimoji.zen_to_han(body, kana=False)
            mail_regex.check_patter(to_han_body)

            # 複数できない項目があった場合はエラーで通知しておくか

            print(mail_regex.name)
            print(mail_regex.station)
            print(mail_regex.skill)
            print(mail_regex.cost)
            print(mail_regex.belongs)
            print(mail_regex.subject)
            print(mail_regex.send_date)
            print(mail_regex.sender)
            print(mail_regex.file_count)
            print(mail_regex.file_name)
            print(mail_regex.file_mime_type)
            print(mail_regex.checked)
        print("-------------終わり-------------------\n")


if __name__ == "__main__":
    main()
