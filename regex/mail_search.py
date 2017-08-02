import os
import re


class ExtractRegex:

    NAMEPATTERN = r"氏名|名|名前"
    STATIONPATTERN = r"最寄り駅|最寄駅｜最寄"
    SKILLPATTERN = r"スキル"
    COSTPATTERN = r"単価"

    def __init__(self):
        self.name_patter = re.compile(self.NAMEPATTERN)
        self.station_patter = re.compile(self.STATIONPATTERN)
        self.skill_patter = re.compile(self.SKILLPATTERN)
        self.cost_patter = re.compile(self.COSTPATTERN)

    """
    項目ごとにカスタマイズする可能性考慮
    """

    def name(self, line):
        match = self.name_patter.search(line)

        if match is not None:
            end = match.end()
            _str = line[end + 1:]
            str = _str.strip()

            return str

        return False

    def station(self, line):
        match = self.station_patter.search(line)

        if match is not None:
            end = match.end()
            return line[end + 1:]

        return False

    def skill(self, line):
        match = self.skill_patter.search(line)

        if match is not None:
            return line[match.end() + 1:]

        return False

    def cost(self, line):
        match = self.cost_patter.search(line)

        if match is not None:
            span = match.span()
            return line[span[1] + 1:]

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
        for l in lines:
            if not _name:
                _name = ext.name(l)

            if not _station:
                _station = ext.station(l)

            if not _skill:
                _skill = ext.skill(l)

            if not _cost:
                _cost = ext.cost(l)

                # 複数できない項目があった場合はエラーで通知しておくか

        print(_name)
        print(_station)
        print(_skill)
        print(_cost)

# fp = open("name.txt", "r", encoding="utf-8")
# line = fp.read()
# fp.close()
#
# lines = line.split('\n')
#
# ext = ExtractRegex()
#
# _name = ""
# _station = ""
# _skill = ""
# _cost = ""
#
# for l in lines:
#     if not _name:
#         _name = ext.name(l)
#
#     if not _station:
#         _station = ext.station(l)
#
#     if not _skill:
#         _skill = ext.skill(l)
#
#     if not _cost:
#         _cost = ext.cost(l)
#
#
#     # 複数できない項目があった場合はエラーで通知しておくか
#
# print(_name)
# print(_station)
# print(_skill)
# print(_cost)
#


