
class Hoge:
    test1 = 'test1'

    def __init__(self):
        self.test2 = "test2"


hoge = Hoge()

print("test1", hoge.test1)
print("test2", hoge.test2)


hoge.test1 = "__test1"
hoge.test2 = "__test2"

hoge.test1 = "__999jtest1"
print("test1", hoge.test1)
print("test2", hoge.test2)

del hoge.test1

# クラスメンバ変数の場合はdelをしても初期値がのこる
print("test1", hoge.test1)
print("test2", hoge.test2)
