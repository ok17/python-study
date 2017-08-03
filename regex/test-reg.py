import re
# import sys


pattern = "(氏名|名前|名)"
itttern = "(\w)"




with open("name.txt", "r", encoding="utf-8") as fp:
    txt = fp.read()

    lines = txt.split('\n')

    for line in lines:
        # patter = re.compile(r"((.)?(最寄|名(\s*)前|名)(\W*)(.*))", re.VERBOSE)
        # patter = re.compile(r"(((.)?(最(\s*)寄(.)?(駅)?)(\W*)(.*)))", re.VERBOSE)
        # patter = re.compile(r"((.)?(ス(\s*)キ(\s*)ル)(\W*)(.*))", re.VERBOSE)
        patter = re.compile(r"((.)?(所(\s*)属)(\W*)(.*))", re.VERBOSE)
        mo = patter.search(line)
        # print(mo)

        if mo is not None:
            print("agagg", mo.group(6))
            print("agagg", mo.group(6))



