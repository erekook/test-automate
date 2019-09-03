from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 解决在root下无法打开chrome的问题
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# fetching a page
driver.get('https://www.baidu.com/')

# Locating UI Elements(WebElements)

# By ID
element = driver.find_element_by_id("id")
# or
element = driver.find_element(by=By.ID, value="id")


# By Class Name
cheeses = driver.find_elements_by_class_name("cheese")
# or
cheeses = driver.find_elements(By.CLASS_NAME, "cheese")

# By Tag Name
frame = driver.find_element_by_tag_name("iframe")
# or
frame = driver.find_element(By.TAG_NAME, "iframe")

# By Name
# <input name="cheese" type="text" />
cheese = driver.find_element_by_name("cheese")
# or
cheese = driver.find_element(By.NAME, "cheese")

# By Link Text
# <a href="http://www.google.com/search?q=cheese">cheese</a>
cheese = driver.find_element_by_link_text("cheese")
# or
cheese = driver.find_element(By.LINK_TEXT, "cheese")

# By Partial Link text
# <a href="http://www.google.com/search?q=cheese">search for cheese</a>
cheese = driver.find_element_by_partial_link_text("cheese")
# or
cheese = driver.find_element(By.PARTIAL_LINK_TEXT, "cheese")


# By CSS
# <div id="food"><span class="dairy">milk</span><span class="dairy aged">cheese</span></div>
cheese = driver.find_element_by_css_selector("#food span.dairy.aged")
# or
cheese = driver.find_element(By.CSS_SELECTOR, "#food span.dairy.aged")

# By XPath
inputs = driver.find_elements_by_xpath("//input")
# or
inputs = driver.find_elements("//input")
