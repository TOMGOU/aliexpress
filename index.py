from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os 

# service = Service('/Users/Application/chromedriver')

# options = webdriver.ChromeOptions()
# options.add_experimental_option('detach', True)
# driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome(service=service)

# driver.get('https://python-selenium-zh.readthedocs.io/zh_CN/latest/1.%E5%AE%89%E8%A3%85/')

# driver.execute_script("window.scrollTo(0, 500);")

# time.sleep(20)

def file_name(file_dir):   
    L={'file_name': [], 'url_name': []}  
    for root, dirs, files in os.walk(file_dir):
      for file in files:  
        if os.path.splitext(file)[1] == '.jpg':  
          L['url_name'].append(os.path.join(root, file))
          L['file_name'].append(os.path.splitext(file)[0])           
    return L


print(file_name('./imgs'))
