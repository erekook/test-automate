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
driver.get('https://www.baidu.com/')

# print the website's title
print(driver.title)
#print(driver.page_source)

# find the element that's class name  is s_ipt (the baidu search box)
inputElement = driver.find_element_by_class_name("s_ipt")

# type in the search
inputElement.send_keys("123")

# submit the form
inputElement.submit()


try:
    # we have to wait the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 5).until(EC.title_contains("hello"))
    
    # you can see the  "hello" title
    print(driver.title)
except TimeoutException:
    print("timeout sorry!")
finally:
    # close the browser
    # driver.quit()
    print("over")
