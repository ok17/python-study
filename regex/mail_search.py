import os
import re


class ExtractRegex:

    def __init__(self):
        self.name_patter = re.compile(r"((.)?(氏(\s*)名|名(\s*)前|名)(\W*)(.*))", re.VERBOSE)
        self.station_patter = re.compile(r"(((.)?(最(\s*)寄(.)?(駅)?)(\W*)(.*)))", re.VERBOSE)
        self.skill_patter = re.compile(r"((.)?(ス(\s*)キ(\s*)ル)(\W*)(.*))", re.VERBOSE)
        self.cost_patter = re.compile(r"((.)?(単(\s*)金|単(\s*)価|金(\s*)額)(\W*)(.*))", re.VERBOSE)
        self.belongs_patter = re.compile(r"((.)?(所(\s*)属)(\W*)(.*))", re.VERBOSE)

    """
    項目ごとにカスタマイズする可能性考慮
    """

    def name(self, line):
        match = self.name_patter.search(line)

        if match is not None:
            _name = match.group(7)
            return _name

        return False

    def station(self, line):
        match = self.station_patter.search(line)

        if match is not None:
            _station = match.group(9)
            return _station

        return False

    def skill(self, line):
        match = self.skill_patter.search(line)

        if match is not None:
            _skill = match.group(7)
            return _skill

        return False

    def cost(self, line):
        match = self.cost_patter.search(line)

        if match is not None:
            _cost = match.group(8)
            return _cost

        return False

    def belongs(self, line):
        match = self.belongs_patter.search(line)

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
            if not _name:
                _name = ext.name(l)

            if not _station:
                _station = ext.station(l)

            if not _skill:
                _skill = ext.skill(l)

            if not _cost:
                _cost = ext.cost(l)

            if not _belongs:
                _belongs = ext.belongs(l)

                # 複数できない項目があった場合はエラーで通知しておくか

        print(_name)
        print(_station)
        print(_skill)
        print(_cost)
        print(_belongs)

