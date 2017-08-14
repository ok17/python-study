import os
import re
import mojimoji


class ExtractRegex:

    delimiter = r"([ -\/:-@\[-`\{-\~])"
    # delimiter = "([ -\/:-@\[-`\{-\~])"
    character = "(.*)"


    def __init__(self):
        # self.name_patter = re.compile(r"((.)?(氏(\s*)名|名(\s*)前|名)(\W*)(.*))", re.VERBOSE)


        # self.name_patter = re.compile(r"((.)?(氏(\s*)名|名(\s*)前|名)([ -\/:-@\[-`\{-\~])+(.*))", re.VERBOSE)
        # self._name_patter = re.compile("{}{}+{}".format(self.name_patter, self.delimiter, self.character))

        self.__name = None
        self.__skill = None
        self.__cost = None
        self.__belongs = None
        self.__station = None
        # self.name = re.compile("{}{}+{}".format(self.name_patter, self.delimiter, self.character))


        # print(self._name_patter)
        #
        # print("1234\n567890")
        # print("1234\\n567890")
        # print(r"1234\n567890")
        self.create_pattern()
        #
        # print("iaaaa\gaga\ag")
        # exit()
        # self.station_patter = re.compile(r"(((.)?(最(\s*)寄(.)?(駅)?)(\W*)(.*)))", re.VERBOSE)
        #self.skill_patter = re.compile(r"((.)?(ス(\s*)キ(\s*)ル)(\W*)(.*))", re.VERBOSE)
        # self.cost_patter = re.compile(r"((.)?(単(\s*)金|単(\s*)価|金(\s*)額)(\W*)(.*))", re.VERBOSE)
        # self.belongs_patter = re.compile(r"((.)?(所(\s*)属)(\W*)(.*))", re.VERBOSE)
        # self.gender_patter = re.compile(r"'((.)?(性(\s*)別)'+delimiter+'(.*))'", re.VERBOSE)

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

    def create_pattern(self):
        name_patter = r"((.)?(氏(\s*)名|名(\s*)前|名))"
        skill_patter = r"((.)?(ス(\s*)キ(\s*)ル))"
        cost_patter = r"((.)?(単(\s*)金|単(\s*)価|金(\s*)額))"
        belongs_patter = r"((.)?(所(\s*)属))"
        station_patter = r"(((.)?(最(\s*)寄(.)?(駅)?)))"

        self.name = re.compile("{}{}+{}".format(name_patter, self.delimiter, self.character))
        self.skill = re.compile("{}{}+{}".format(skill_patter, self.delimiter, self.character))
        self.cost = re.compile("{}{}+{}".format(cost_patter, self.delimiter, self.character))
        self.belongs = re.compile("{}{}+{}".format(belongs_patter, self.delimiter, self.character))
        self.station = re.compile("{}{}+{}".format(station_patter, self.delimiter, self.character))

    """
    項目ごとにカスタマイズする可能性考慮
    """

    def re_name(self, line):
        match = self.name.search(line)

        if match is not None:
            _name = match.group(7)
            return _name

        return False

    def re_station(self, line):
        match = self.station.search(line)

        if match is not None:
            _station = match.group(9)
            return _station

        return False

    def re_skill(self, line):
        match = self.skill.search(line)

        if match is not None:
            _skill = match.group(7)
            return _skill

        return False

    def re_cost(self, line):
        match = self.cost.search(line)

        if match is not None:
            _cost = match.group(8)
            return _cost

        return False

    def re_belongs(self, line):
        match = self.belongs.search(line)

        if match is not None:
            _belongs = match.group(6)
            return _belongs

        return False

DIRPATH = "../mail/emails/"

dir_list = os.listdir(DIRPATH)

for txt in dir_list:
    with open(DIRPATH + txt, "r", encoding="utf-8") as fp:
        line = fp.read()

        lines = line.split('\n')
        ext = ExtractRegex()

        _name = ""
        _station = ""
        _skill = ""
        _cost = ""
        _belongs = ""
        for l in lines:
            # 全角から半角へ変換
            l_to_han = mojimoji.zen_to_han(l, kana=False)
            if not _name:
                # print("name:", l_to_han)
                _name = ext.re_name(l_to_han)

            if not _station:
                # print("station:", l_to_han)
                _station = ext.re_station(l_to_han)

            if not _skill:
                # print("skill:", l_to_han)
                _skill = ext.re_skill(l_to_han)

            if not _cost:
                # print("cost:", l_to_han)
                _cost = ext.re_cost(l_to_han)

            if not _belongs:
                # print("belongs:", l_to_han)
                _belongs = ext.re_belongs(l_to_han)

                # 複数できない項目があった場合はエラーで通知しておくか

        print(_name)
        print(_station)
        print(_skill)
        print(_cost)
        print(_belongs)

