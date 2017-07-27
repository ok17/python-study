from selenium import webdriver
url = "http://www.aozora.gr.jp/cards/000081/files/46268_23911.html"

browser = webdriver.PhantomJS()
browser.implicitly_wait(3)
browser.get(url)

browser.save_screenshot("web.png")

browser.quit()

