from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

service = Service('/Users/tangyong/Application/chromedriver')
options = webdriver.ChromeOptions()
# options.add_argument("user-data-dir=~/Library/'Application Support'/Google/Chrome/")
options.add_argument("~/Library/Caches/Google/Chrome/")

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://login.aliexpress.com/seller_new.htm?return_url=https://gsp.aliexpress.com/')

time.sleep(10)
