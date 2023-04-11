from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import openpyxl
import os 

def isElementExist(driver, element):
  flag=True
  try:
    # browser.find_element_by_css_selector(element)
    driver.find_element(By.CSS_SELECTOR, element)
    return flag
  except:
    flag=False
    return flag

def file_name(file_dir):   
  L={'file_name': [], 'url_name': []}  
  for root, dirs, files in os.walk(file_dir):
    for file in files:  
      if os.path.splitext(file)[1] == '.jpg':  
        L['url_name'].append(os.path.join(root, file))
        L['file_name'].append(os.path.splitext(file)[0])           
  return L

def fetchData(url):
  # 打开文件
  workbook = openpyxl.load_workbook(url)

  # 选择工作表
  worksheet = workbook['Sheet1']

  # 第一行分析
  # first = []
  # for index, cell in enumerate(worksheet['A1:A40']):
  #   print(cell[0].value, end="\n")
  #   if cell[0].value:
  #     first.append(index + 1)

  # 读取标题
  title = worksheet['B1'].value

  # 适用机型
  models = worksheet['B2'].value

  # 读取颜色
  colors = []
  for index, cell in enumerate(worksheet['B3:B10']):
    colors.append(cell[0].value)

  # 读取材质
  materials = []
  for index, cell in enumerate(worksheet['B11:B34']):
    materials.append(cell[0].value)

  # 读取价格
  price = worksheet['B35'].value

  # 读取库存
  inventory = worksheet['B36'].value

  # 读取SKU
  sku = worksheet['B37'].value

  # 读取详描标题
  detail_title = worksheet['B38'].value

  return {
    'title': title,
    'models': models,
    'colors': colors,
    'materials': materials,
    'price': price,
    'inventory': inventory,
    'sku': sku,
    'detail_title': detail_title,
  }

def login():
  username = driver.find_element(By.ID,'fm-login-id')
  password = driver.find_element(By.ID,'fm-login-password')
  username.send_keys('2116491679@qq.com')
  password.send_keys('FuJuAn666666')
  # password.send_keys(Keys.RETURN)

  sign_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div/div/button[2]')
  sign_in.click()


  iframe = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'baxia-dialog-content')))
  driver.switch_to.frame(iframe)
  sliderBg = driver.find_element(By.ID, 'nc_1_n1t')
  slider = driver.find_element(By.ID, 'nc_1_n1z')
  action_chains = ActionChains(driver)
  action_chains.click_and_hold(slider).move_by_offset(sliderBg.size['width'], 0).release().perform()
  driver.switch_to.default_content()

service = Service('/Users/Application/chromedriver')

# options = webdriver.ChromeOptions()
# options.add_experimental_option('detach', True)
# driver = webdriver.Chrome(service=service, options=options)

driver = webdriver.Chrome(service=service)

driver.get('https://login.aliexpress.com/seller_new.htm?return_url=https://gsp.aliexpress.com/')

login()

# try:
#   goods = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-layout-root"]/section[2]/div[1]/div/div/ul/li[2]/div/div/span/span/div/span')))
# except:
#   login()

goods = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-layout-root"]/section[2]/div[1]/div/div/ul/li[2]/div/div/span/span/div/span')))

if isElementExist(driver, 'ae-layout-dialog-close'):
  close1 = driver.find_element(By.CLASS_NAME, 'ae-layout-dialog-close')
  close1.click()
if isElementExist(driver, 'next-dialog-close'):
  close2 = driver.find_element(By.CLASS_NAME, 'next-dialog-close')
  close2.click()

goods.click()

goodsUpload = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-layout-root"]/section[2]/div[1]/div/div/ul/li[2]/ul/li[1]/div/span/a')))
goodsUpload.click()

handles = driver.window_handles
driver.switch_to.window(handles[-1])

data = fetchData('./example.xlsx')

title = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'title')))
title.send_keys(data['title'])

category = driver.find_element(By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/span/span/span[1]/span/span/input')
category.click()

category1 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[1]/span/input')))
category1.send_keys('电话和通讯')

result1 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/ul/li')))
result1.click()

category1 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/span/input')))
category1.send_keys('手机配件')

result2 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/ul/li/p/span[4]')))
result2.click()

category1 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[3]/div[1]/span/input')))
category1.send_keys('手机包/手机壳')

result3 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[3]/div[2]/ul/li/p/span[6]')))
result3.click()

confirm = driver.find_element(By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/button[1]')
confirm.click()

driver.maximize_window()

title_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-title"]/div/div[1]/label')))
add_icon = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-mainImage"]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div')))
# driver.execute_script("window.focus();document.body.style.zoom='100%';window.scrollTo(0, 2000);")
driver.execute_script("arguments[0].scrollIntoView();", title_element)
# ActionChains(driver).move_by_offset(0, 1000).perform()
# time.sleep(5)
add_icon.click()

upload_imgs = file_name('/Users/dsc/Study/05_selenium/aliexpress/imgs')

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='material-center-upload-inner']")))
driver.execute_script("document.evaluate(`//*[@class='material-center-upload-inner']`, document).iterateNext().getElementsByTagName('input')[0].style.display = 'block'")
upload_icon = driver.find_element(By.XPATH, "//*[@class='material-center-upload-inner']/input")
upload_icon.send_keys('\n'.join(upload_imgs['url_name']))

# upload_confirm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"确认上传") and @class="material-center-btn-helper"]')))
upload_confirm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="material-center-upload-footer"]/button[1]')))
while True:
  if upload_confirm.is_enabled():
    upload_confirm.click()
    break

time.sleep(30)
driver.quit()
