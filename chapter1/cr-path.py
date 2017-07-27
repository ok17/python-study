from urllib.parse import urljoin

base = "http://example.com/html/a.html"

print(urljoin(base, "b.html"))
print(urljoin(base, "http://hoge.com/test"))


list = ["a", "a", "b"]

