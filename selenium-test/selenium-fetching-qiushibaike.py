from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 解决在root下无法打开chrome的问题
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# fetching a page
driver.get('http://www.qiushibaike.com/text/')

print('begin read the qiushibaike')

# 文章列表
articleBoxs = driver.find_elements_by_class_name("article")

# 第一个文章的作者
author = articleBoxs[0].find_element_by_tag_name("h2")
# 第一个文章的内容
content = articleBoxs[0].find_element_by_tag_name("span")
#print(content.get_attribute('innerHTML'))

# 循环文章列表
for article in articleBoxs:
    author = article.find_element_by_tag_name("h2").text
    content = article.find_element_by_tag_name("span").text
    print("author:\n",author)
    print("content:\n", content)
# 关闭浏览器
#driver.close()
