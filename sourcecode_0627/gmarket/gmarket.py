import os
import time
import mysql.connector
import requests
import logging
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.common.exceptions import NoSuchElementException

import dbInfo

MaxWait = 10

class Gmarket:
     def __init__(self, url, login_mode, dbconn, cursor):     #초기화
          self.url = url
          self.login_mode = login_mode
          self.dbconn = dbconn
          self.cursor = cursor
          self.selenimum_mode = 0
          user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
          self.hdr = {'User-Agent': user_agent}

          self.logger = logging.getLogger(name='MyLog')
          self.logger.setLevel(logging.INFO)
          formatter = logging.Formatter('[%(asctime)s, %(levelname)s] %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

          if self.logger.hasHandlers():  #is there existing handler
               self.logger.handlers.clear()
          file_handler = logging.FileHandler("./gmarket/Gmarket.log", mode='a')
          file_handler.setFormatter( formatter )
          self.logger.addHandler(file_handler)
          self.logger.info("Start..")


     def  selenium_driverCall(self, selenimum_mode):
          self.selenimum_mode = selenimum_mode
          if selenimum_mode == 1:
               options = webdriver.ChromeOptions()
               options.add_argument('--headless')
               options.add_experimental_option("useAutomationExtension", False)
               options.add_experimental_option("excludeSwitches", ["enable-automation"])
               options.add_argument('lang=ko_KR')

               chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
               try:
                    self.driver = webdriver.Chrome(service=Service(executable_path=f'./{chrome_ver}/chromedriver'),
                                                   options=options)
               except:
                    chromedriver_autoinstaller.install(True)
                    self.driver = webdriver.Chrome(service=Service(executable_path=f'./{chrome_ver}/chromedriver'),
                                                   options=options)
               self.driver.implicitly_wait(MaxWait)

          elif selenimum_mode == 2:  ## Window subprocess call
               self.callprocess = subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
               options = Options()
               options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

               chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
               try:
                    self.driver = webdriver.Chrome(
                         f'C:\\Users\\DDWU\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\chromedriver_autoinstaller\\{chrome_ver}\\chromedriver.exe',
                         options=options)
               except:
                    path = chromedriver_autoinstaller.install()
                    print("ChromeDriver Version Update:", path)
                    self.driver = webdriver.Chrome(path, options=options)
               self.driver.implicitly_wait(MaxWait)

          elif selenimum_mode == 3:  ## Linux subprocess call
               self.callprocess = subprocess.Popen(
                    f'google-chrome --remote-debugging-port=9222  --user-data-dir=data_dir'.split())
               options= webdriver.ChromeOptions()
               options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

               chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
               try:
                    self.driver = webdriver.Chrome(service=Service(executable_path=f'./{chrome_ver}/chromedriver'),
                                                   options=options)
               except:
                    chromedriver_autoinstaller.install(True)
                    self.driver = webdriver.Chrome(service=Service(executable_path=f'./{chrome_ver}/chromedriver'),
                                                   options=options)
               self.driver.implicitly_wait(MaxWait)


     def login(self, id, passwd):
          self.driver.get('https://signinssl.gmarket.co.kr/login/login?url=https://www.gmarket.co.kr/')

          user_id = self.driver.find_element(By.XPATH, '//*[@id="typeMemberInputId"]')
          user_id.send_keys(id)
          user_pw = self.driver.find_element(By.XPATH, '//*[@id="typeMemberInputPassword"]')
          user_pw.send_keys(passwd)

          self.driver.find_element(By.XPATH, '//*[@id="btn_memberLogin"]').click()
          self.driver.implicitly_wait(MaxWait)


     def category(self):
          resp = requests.get(self.url, headers=self.hdr)  ##Static Crawling instead of Dynamic Crawling:self.driver.get()
          soup = BeautifulSoup(resp.text, 'html.parser')

          f = open("./gmarket/gmarket_category.html", "w", encoding='utf-8')
          f.write(soup.prettify())
          f.close()

          # 정보 크롤링
          tmp1 = soup.select_one('div#box__toggle-filter-c > div > ul > li > a > span')
          productCategory = tmp1.text
          # productCategory = self.driver.find_elements(By.XPATH, '//*[@id="box__toggle-filter-c"]/div/ul/li/a/span').text

          div = soup.select('div#section__inner-content-body-container > div:nth-of-type(2) > div')
          # div = self.driver.find_elements(By.XPATH, '//*[@id="section__inner-content-body-container"]/div[2]/div')

          print("Loop Count: ", len(div))
          i = 1
          for di in div:
               print("Loop Number: ", i)
               # if i >= 20:
               #      break

               tmp = di.find(class_='link__item')
               tmp2 = tmp.attrs
               productNo = tmp2["data-montelena-goodscode"]
               productUrl = tmp2["href"]

               adsYn = 'N'
               tmp = di.find(class_='text__item')
               productName = tmp.text
               # productName = di.select('.text__item').text
               try:
                    box = di.find(class_='box__price-original').find(class_='text text__value')
                    listPrice = box.text
                    print(listPrice)
                    listPrice = listPrice.replace(',', '').replace('원', '')
                    listPrice = (int)(listPrice, base=0)

                    box = di.find(class_='box__discount')
                    tmp = box.find(class_='text text__value')
                    discountRateDouble = tmp.text
                    if (discountRateDouble[-1] == '원'):
                         discountRateDouble = 0
                    else:
                         discountRateDouble = discountRateDouble.replace('%', '')
                         discountRateDouble = float(int(discountRateDouble, base=0)) / 100
               except:
                    print("1: No ListPrice Info in this product")
                    self.logger.info(f'{i}-th Product: No Before-Discount Price Info')
                    listPrice = -1

                    print("3: No DiscountRateDouble Info in this product")
                    self.logger.info(f"{i}-th Product: No Price-Discount Rate Info")
                    discountRateDouble = -1


               price = -1
               discountCouponNameDouble = None
               discountProvider = -1
               discountPriceCommerce = -1
               discountCouponName = 'sale'
               discountDouble = -1
               totalPrice = price
               bestRank = -1

               starScore = -1
               reviewCount = -1

               buyCount = -1
               saleCompany = 'GMARKET'
               deliveryPrice = -1

               deliveryType = "일반 배송"
               searchWord = None
               adArea = '상품리스트'
               optionName = None
               likeClick = -1
               salesMan = 'GMARKET'
               optionNo = -1
               brandName = None
               event = None
               vendorItemId = productNo
               collectionDate = datetime.now()
               commerceType = 'GMARKET'
               created = datetime.now()
               updated = datetime.now()
               updater = 1
               etcDeliveryName = None
               referenceId = -1
               dataRanking = i
               creator = 1

               data = {
                    'product_name': productName,
                    'product_no': productNo,
                    'list_price': listPrice,
                    'price': price,
                    'discount_provider': discountProvider,
                    'discount_price_commerce': discountPriceCommerce,
                    'discount_coupon_name': discountCouponName,
                    'discount_double': discountDouble,
                    'discount_rate_double': discountRateDouble,
                    'discount_coupon_name_double': discountCouponNameDouble,
                    'total_price': totalPrice,
                    'best_rank': bestRank,
                    'star_score': starScore,
                    'review_count': reviewCount,
                    'buy_count': buyCount,
                    'sale_company': saleCompany,
                    'delivery_price': deliveryPrice,
                    'product_url': productUrl,
                    'delivery_type': deliveryType,
                    'search_word': searchWord,
                    'ad_area': adArea,
                    'option_name': optionName,
                    'like_click': likeClick,
                    'salesman': salesMan,
                    'option_no': optionNo,
                    'brand_name': brandName,
                    'event': event,
                    'vendor_item_id': vendorItemId,
                    'collection_date': collectionDate,
                    'commerce_type': commerceType,
                    'created': created,
                    'updated': updated,
                    'updater': updater,
                    'etc_delivery_name': etcDeliveryName,
                    'reference_id': referenceId,
                    'product_category': productCategory,
                    'ads_yn': adsYn,
                    'data_ranking': dataRanking,
                    'creator': creator
               }
               i += 1
               dbInfo.insert_data("total_category", self.dbconn, self.cursor, data)


          ## Close this crawling operation for gmarket category
          self.dbconn.close()
          if self.login_mode == 1: ## click logout button
              logoutBtn = self.driver.find_element(By.XPATH, '//*[@id="desktop_layout-header"]/div/div/div[2]/div[3]/ul/li[2]/a')
              logoutBtn.click()
              self.driver.implicitly_wait(MaxWait)

          if self.selenimum_mode > 0:     ## close the selenium driver
              self.driver.quit()
          if self.selenimum_mode > 1:  ## terminate the called subprocess
              self.callprocess.terminate()


