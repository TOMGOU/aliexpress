from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# service = Service('/Users/Application/chromedriver')
# options = webdriver.ChromeOptions()
# options.add_argument(r'user-data-dir=/Users/dsc/Library/Application Support/Google/Chrome')
# options.add_experimental_option("useAutomationExtension", False)
# options.add_argument("--start-maximized")
# options.add_argument("disable-extensions")
# options.add_argument("--start-maximized")
# options.add_argument("--remote-debugging-port=9222")
# options.add_argument('--no-sandbox')
# driver = webdriver.Chrome(service=service, options=options)

# driver.get('https://login.aliexpress.com/seller_new.htm?return_url=https://gsp.aliexpress.com/')

# time.sleep(10)

# my_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# filtered_array = my_array[:6]
# print(filtered_array)

my_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered_array = [x for x in my_array if x <= 6]
print(filtered_array)

