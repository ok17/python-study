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

HUMAN_PROPERTIES = {
    Property.NAME: {
        "patter": "((.)?(氏(\s*)名|名(\s*)前|名))",
        "no": 7
    },
    Property.GENDER: {
        "patter": "((.)?(性(\s*)別))",
        "no": 6
    },
    Property.SKILL: {
        "patter": "((.)?(ス(\s*)キ(\s*)ル))",
        "no": 7
    },
    Property.COST: {
        "patter": "((.)?(単(\s*)金|単(\s*)価|金(\s*)額))",
        "no": 8
    },
    Property.BELONGS: {
        "patter": "((.)?(所(\s*)属))",
        "no": 6
    },
    Property.STATION: {
        "patter": "(((.)?(最(\s*)寄(.)?(駅)?)))",
        "no": 9
    }
}

CHARACTER = "(.*)"
DELIMITER = "([ -\/:-@\[-`\{-\~])"


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

        self.__name = None
        self.__skill = None
        self.__cost = None
        self.__belongs = None
        self.__station = None
        self.__gender = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, input_name):
        self.__name = input_name

    @name.deleter
    def name(self):
        del self.__name

    @property
    def skill(self):
        return self.__skill

    @skill.setter
    def skill(self, input_skill):
        self.__skill = input_skill

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, input_cost):
        self.__cost = input_cost

    @property
    def belongs(self):
        return self.__belongs

    @belongs.setter
    def belongs(self, input_belongs):
        self.__belongs = input_belongs

    @property
    def station(self):
        return self.__station

    @station.setter
    def station(self, input_station):
        self.__station = input_station

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, input_gender):
        self.__gender = input_gender


    """
    項目ごとにカスタマイズする可能性考慮
    """
    def check_patter(self, line):
        for prop in HUMAN_PROPERTIES:
            if self.__is_checked(prop) is True:
                continue

            patter = re.compile(r"{}{}+{}".format(HUMAN_PROPERTIES[prop]["patter"], DELIMITER, CHARACTER))

            match = patter.search(line)

            if match is not None:
                _character = match.group(HUMAN_PROPERTIES[prop]["no"])
                self.__set_val(prop, _character)

    def __is_checked(self, property):
        return self.checked[property]

    def __set_val(self, property, character):
        self.checked[property] = True

        if Property.NAME is property:
            self.name = character

        elif Property.SKILL is property:
            self.skill = character

        elif Property.COST is property:
            self.cost = character

        elif Property.STATION is property:
            self.station = character

        elif Property.GENDER is property:
            self.gender = character
            print("gender", character)

        elif Property.BELONGS is property:
            self.belongs = character

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
            print(ext.checked)
        print("-------------終わり-------------------\n")

