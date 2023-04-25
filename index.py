# import win_unicode_console
# win_unicode_console.enable()
import sys,os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate, QDateTime
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QDateTimeEdit, QApplication, QFileDialog)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import openpyxl
import time

class Upload(QWidget):
  def __init__(self):
    super(Upload, self).__init__()
    self.switch = True
    self.initUI()

  def initUI(self):
    # 账号输入框和提示
    self.gapLabel = QLabel(self)
    self.gapLabel.move(30, 30)
    self.gapLabel.resize(100,30)
    self.gapLabel.setText("账号：")
    self.gap_user = QLineEdit('2116491679@qq.com', self)
    self.gap_user.move(120,30)
    self.gap_user.resize(250, 30)

    # 密码输入框和提示
    self.gapLabel = QLabel(self)
    self.gapLabel.move(30, 75)
    self.gapLabel.resize(100,30)
    self.gapLabel.setText("密码：")
    self.gap_pw = QLineEdit('FuJuAn666666', self)
    self.gap_pw.move(120,75)
    self.gap_pw.resize(250, 30)

    # 图片文件夹选择按钮和选择编辑框
    self.source_btn = QPushButton('图片文件夹', self)
    self.source_btn.move(15, 120)
    self.source_btn.resize(100,30)
    self.source_btn.clicked.connect(self.select_source)
    self.source_imgs = QLineEdit('/Users/dsc/Study/05_selenium/aliexpress/imgs', self)
    self.source_imgs.move(120, 120)
    self.source_imgs.resize(250,30)

    # Excel 文件选择按钮和选择编辑框
    self.source_btn = QPushButton('Excel 文件', self)
    self.source_btn.move(15, 165)
    self.source_btn.resize(100,30)
    self.source_btn.clicked.connect(self.select_file)
    self.source_excel = QLineEdit('/Users/dsc/Study/05_selenium/aliexpress/example.xlsx', self)
    self.source_excel.move(120, 165)
    self.source_excel.resize(250,30)

    # 上传按钮
    self.save_btn = QPushButton('开始上传',self)
    self.save_btn.move(200, 220)
    self.save_btn.resize(140, 30)
    self.save_btn.clicked.connect(self.kick)

    # 用户提示区
    self.result_le = QLabel('请输入后点击开始上传', self)
    self.result_le.move(30, 270)
    self.result_le.resize(340, 30)
    self.result_le.setStyleSheet('color: blue;')

    # 整体界面设置
    self.resize(400, 400)
    self.center()
    self.setWindowTitle('速卖通商品自动化上传')#设置界面标题名
    self.show()
  
  # 窗口居中函数
  def center(self):
    screen = QtWidgets.QDesktopWidget().screenGeometry()#获取屏幕分辨率
    size = self.geometry()#获取窗口尺寸
    self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))#利用move函数窗口居中

  # 打开的视频文件名称
  def select_source(self):
    dir_path = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "C:/")
    self.source_imgs.setText(str(dir_path))

  def select_file(self):
    dir_path = QFileDialog.getOpenFileName(self, "请选择文件路径", "C:/")
    self.source_excel.setText(str(dir_path[0]))

  def set_label_func(self, text):
    self.result_le.setText(text)
  
  def onLanFromActivated(self, text):
    self.cat_form = text

  def switch_func(self, bools):
    self.switch = bools

  def kick(self):
    user = self.gap_user.text().strip()
    password = self.gap_pw.text().strip()
    imgs = self.source_imgs.text().strip()
    excel = self.source_excel.text().strip()
    if self.switch and user != '' and password != '' and imgs != '' and excel != '':
      self.switch = False
      self.set_label_func('请耐心等待，正在打开浏览器！')
      self.my_thread = MyThread(user, password, imgs, excel, self.set_label_func)#实例化线程对象
      self.my_thread.start()#启动线程
      self.my_thread.my_signal.connect(self.switch_func)

class MyThread(QThread):
  my_signal = pyqtSignal(bool)  #自定义信号对象。参数bool就代表这个信号可以传一个布尔值
  def __init__(self, user, password, imgs, excel, set_label_func):
    super(MyThread, self).__init__()
    self.user = user
    self.password = password
    self.imgs = imgs
    self.excel = excel
    self.set_label_func = set_label_func

  def run(self): #线程执行函数
    string = self.fetchData(self.user, self.password, self.imgs, self.excel, self.set_label_func)
    self.set_label_func(string)
    self.my_signal.emit(True)  #释放自定义的信号

  def fetchData(self, user, password, imgs, excel, set_label_func):
    ###  WINDOWS ###
    # option = webdriver.ChromeOptions()
    # option.add_argument(r'user-data-dir=C:\Users\zhuan\AppData\Local\Google\Chrome\User Data')
    # option.add_argument('--ignore-certificate-errors')
    # driver = webdriver.Chrome(options=option)
    ###  MAC ###
    service = Service('/Users/Application/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://login.aliexpress.com/seller_new.htm?return_url=https://gsp.aliexpress.com/')

    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    driver.execute_script(script)

    driver.implicitly_wait(10)

    set_label_func('浏览器已成功打开！！')

    driver.maximize_window()

    time.sleep(0.1)

    self.login(driver, user, password)
    self.slide(driver)
    
    while True:
      try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-layout-root"]/section[2]/div[1]/div/div/ul/li[2]/div/div/span/span/div/span')))
        break
      except:
        self.login(driver, user, password)
    
    wait = WebDriverWait(driver, 20)

    set_label_func('登录完成！！')

    goods = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-layout-root"]/section[2]/div[1]/div/div/ul/li[2]/div/div/span/span/div/span')))

    if self.isElementExist(driver, 'ae-layout-dialog-close'):
      close1 = driver.find_element(By.CLASS_NAME, 'ae-layout-dialog-close')
      close1.click()
    if self.isElementExist(driver, 'next-dialog-close'):
      close2 = driver.find_element(By.CLASS_NAME, 'next-dialog-close')
      close2.click()

    goods.click()

    goodsUpload = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ae-layout-root"]/section[2]/div[1]/div/div/ul/li[2]/ul/li[1]/div/span/a')))
    goodsUpload.click()

    handles = driver.window_handles
    driver.switch_to.window(handles[-1])

    data = self.fetchExcelData(excel)

    title = wait.until(EC.visibility_of_element_located((By.ID, 'title')))
    title.send_keys(data['title'])

    category = driver.find_element(By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/span/span/span[1]/span/span/input')
    category.click()

    category1 = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[1]/span/input')))
    category1.send_keys('电话和通讯')

    result1 = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/ul/li')))
    result1.click()

    category1 = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/span/input')))
    category1.send_keys('手机配件')

    result2 = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/ul/li/p/span[4]')))
    result2.click()

    category1 = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[3]/div[1]/span/input')))
    category1.send_keys('手机包/手机壳')

    result3 = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[3]/div[2]/ul/li/p/span[6]')))
    result3.click()

    confirm = driver.find_element(By.XPATH, '//*[@id="struct-categoryPath"]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/button[1]')
    confirm.click()

    set_label_func('标题和分类填写完成！！')

    ### ----商品图片---- ###
    add_icon = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-mainImage"]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div')))
    title_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-title"]/div/div[1]/label')))
    time.sleep(0.1)
    driver.execute_script("arguments[0].scrollIntoView();", title_element)
    add_icon.click()

    upload_imgs = self.file_name(imgs)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='material-center-upload-inner']")))
    driver.execute_script("document.evaluate(`//*[@class='material-center-upload-inner']`, document).iterateNext().getElementsByTagName('input')[0].style.display = 'block'")
    upload_icon = driver.find_element(By.XPATH, "//*[@class='material-center-upload-inner']/input")
    upload_icon.send_keys('\n'.join(upload_imgs[:6]))

    upload_confirm = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="material-center-upload-footer"]/button[1]')))
    while True:
      if upload_confirm.is_enabled():
        upload_confirm.click()
        break
    
    set_label_func('商品图片上传完成！！')
    ### ----产品属性---- ###
    good_video = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"产品视频") and @class="label"]')))
    driver.execute_script("arguments[0].scrollIntoView();", good_video)

    time.sleep(0.1)

    brand_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-catProperty"]/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div[1]/span/span/span[1]/span/input')))
    brand_input.click()

    brand = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="options-content"]/div/div/div/div[1]')))
    brand.click()

    area = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="struct-catProperty"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/span/span/span[1]/span/input')))
    area.click()

    time.sleep(0.3)
    china_text = "中国大陆(Origin)(Mainland China)"
    china = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[contains(text(),"{china_text}") and @class="options-item"]')))
    china.click()

    phone_type = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-catProperty"]/div/div[2]/div/div[2]/div/div/div[6]/div/div[2]/div[1]/span/span/span[1]/span/input')))
    phone_type.click()

    phone_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="next-overlay-wrapper opened"]/div/div/div[1]/span/input')))
    phone_input.send_keys(data['models'])
    driver.implicitly_wait(1)
    phone_result = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"iPhone(iPhone)") and @class="options-item"]')))
    phone_result.click()

    set_label_func('产品属性填写完成！！')

    ### ----价格与库存---- ###
    origin = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"发货地") and @class="label"]')))
    driver.execute_script("arguments[0].scrollIntoView();", origin)

    material1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="struct-p-10"]/div/div[2]/div/div/div/div/div/div/div[1]/div/label/span[1]/input')))
    material1.click()
    material2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="struct-p-10"]/div/div[2]/div/div/div/div/div/div/div[2]/div/label/span[1]/input')))
    material2.click()

    price = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-sku"]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td[2]/div/div/span/span/span/input')))
    action_chains = ActionChains(driver)
    action_chains.double_click(price).perform()
    action_chains.send_keys(data['price']).send_keys(Keys.ENTER).perform()
    driver.execute_script("document.evaluate(`//*[@id='struct-sku']/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td[2]/div/div/span/span/span/input`, document).iterateNext().setAttribute('value', " + str(data['price']) + ")")

    inventory = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-sku"]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td[3]/div/span/span/span/input')))

    action_chains.double_click(inventory).perform()
    action_chains.send_keys(data['inventory']).send_keys(Keys.ENTER).perform()
    driver.execute_script("document.evaluate(`//*[@id='struct-sku']/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td[3]/div/span/span/span/input`, document).iterateNext().setAttribute('value', " + str(data['inventory']) + ")")

    # code = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-sku"]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[3]/div/table/tbody/tr/td[4]/div/span/span/span/input')))
    # code.click()

    set_label_func('价格与库存填写完成！！')

    ### ----详细描述---- ###
    description = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"详描语言") and @class="label"]')))
    driver.execute_script("arguments[0].scrollIntoView();", description)

    detail_title = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-pcdescription"]/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/p/span[1]/span')))
    detail_title.send_keys(data['detail_title'])

    detail_imgs_upload = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-pcdescription"]/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/span[20]/i')))
    detail_imgs_upload.click()

    imgs_upload_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"上传图片") and @class="material-center-tabs-tab-inner"]')))
    imgs_upload_tab.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='material-center-upload-inner']")))
    driver.execute_script("document.evaluate(`//*[@class='material-center-upload-inner']`, document).iterateNext().getElementsByTagName('input')[0].style.display = 'block'")
    upload_icon = driver.find_element(By.XPATH, "//*[@class='material-center-upload-inner']/input")
    upload_icon.send_keys('\n'.join(upload_imgs))

    upload_confirm = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="material-center-upload-footer"]/button[1]')))
    while True:
      if upload_confirm.is_enabled():
        upload_confirm.click()
        break

    time.sleep(5)

    mobile_edit = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"无线详描编辑") and @class="label"]')))
    driver.execute_script("arguments[0].scrollIntoView();", mobile_edit)

    mobile_import = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="struct-mobiledescription"]/div/div[2]/div/div[2]/div/div/button')))
    mobile_import.click()

    mobile_import_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="preview-dialog-footerBtn"]/button[1]')))
    mobile_import_confirm.click()

    set_label_func('详细描述填写完成！！')

    ### ----包装与物流---- ###
    delivery_date = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="deliveryPeriod"]')))
    delivery_date.send_keys('7')

    delivery_weight = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-logisticsWeight"]/div/div[2]/div/div/div/div/div[1]/span/span[1]/span/input')))
    delivery_weight.send_keys('0.05')

    size_length = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-logisticsSize"]/div/div[2]/div[1]/div/div/div/div/span[1]/input')))
    size_length.send_keys('12')

    size_width = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-logisticsSize"]/div/div[2]/div[1]/div/div/div/div/span[3]/input')))
    size_width.send_keys('10')

    size_height = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-logisticsSize"]/div/div[2]/div[1]/div/div/div/div/span[5]/input')))
    size_height.send_keys('1')

    delivery_date.click()

    delivery_template = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-freightTemplate"]/div/div[2]/div/div/div/div/span[1]')))
    delivery_template.click()

    new_template = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"新手运费模板 (Location: CN)") and @class="options-item"]')))
    new_template.click()

    set_label_func('包装与物流填写完成！！')


    ### ----提交表单---- ###
    # submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="struct-buttons"]/button[1]')))
    # submit.click()

    # time.sleep(30)
    driver.quit()

    set_label_func('done!!!!!!!!!')

    return 'done'
    

  # 元素是否存在判断函数
  def isElementExist(self, driver, element):
    flag=True
    try:
      driver.find_element(By.CSS_SELECTOR, element)
      return flag
    except:
      flag=False
      return flag

  # 文件遍历函数
  def file_name(self, file_dir): 
    img_list=os.listdir(file_dir)
    img_list.sort(key = lambda x: int(x[:-4]))
    img_nums=len(img_list)
    url_name = []
    for i in range(img_nums):
      url_name.append(file_dir + '/' + img_list[i])
    return url_name

  # 获取 excel 中的内容
  def fetchExcelData(self, url):
    # 打开文件
    workbook = openpyxl.load_workbook(url)

    # 选择工作表
    worksheet = workbook['Sheet1']

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

  # 登录
  def login(self, driver, UN, PW):
    driver.implicitly_wait(1)
    username = driver.find_element(By.ID,'fm-login-id')
    password = driver.find_element(By.ID,'fm-login-password')
    
    username.send_keys(UN)
    driver.execute_script(f"document.evaluate(`//*[@id='fm-login-id']`, document).iterateNext().setAttribute('value', '{UN}')")

    password.send_keys(PW)
    driver.execute_script(f"document.evaluate(`//*[@id='fm-login-password']`, document).iterateNext().setAttribute('value', '{PW}')")

    sign_in = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div/div/button[2]')
    sign_in.click()

  # 滑块验证
  def slide(self, driver):
    iframe = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'baxia-dialog-content')))
    driver.switch_to.frame(iframe)
    sliderBg = driver.find_element(By.ID, 'nc_1_n1t')
    slider = driver.find_element(By.ID, 'nc_1_n1z')
    action_chains = ActionChains(driver)
    action_chains.click_and_hold(slider).move_by_offset(sliderBg.size['width'], 0).release().perform()
    driver.switch_to.default_content()

if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = Upload()
  ex.show()
  sys.exit(app.exec_())
