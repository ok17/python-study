from selenium import webdriver

USER = "JS-TESTER"
PASS = "ipCU12ySxI"

browser = webdriver.PhantomJS()
browser.implicitly_wait(3)

url_login = "http://uta.pw/sakusibbs/users.php?action=login"
browser.get(url_login)

print("ログインページにアクセス")

e = browser.find_element_by_id("user")
e.clear()
e.send_keys(USER)


e = browser.find_element_by_id("pass")
e.clear()
e.send_keys(PASS)

form = browser.find_element_by_css_selector("#loginForm form")
form.submit()

# マイページ
a = browser.find_element_by_css_selector(".islogin > a")
url_mypage = a.get_attribute('href')
print("マイページ", url_mypage)

browser.get(url_mypage)

links = browser.find_elements_by_css_selector("#favlist li > a")
for l in links:
    href = l.get_attribute('href')
    title = l.text
    print("-", title, ">", href)


