from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

service = Service('/Users/Application/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument(r'user-data-dir=/Users/dsc/Library/Application Support/Google/Chrome')
# options.add_experimental_option("useAutomationExtension", False)
# options.add_argument("--start-maximized")
# options.add_argument("disable-extensions")
# options.add_argument("--start-maximized")
# options.add_argument("--remote-debugging-port=9222")
# options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://login.aliexpress.com/seller_new.htm?return_url=https://gsp.aliexpress.com/')

time.sleep(10)
