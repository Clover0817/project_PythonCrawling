import os
import subprocess
import mysql.connector
import chromedriver_autoinstaller
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import loginInfo, dbInfo 

class Gmarket:

     def __init__(self, url, login_mode, os_mode): 
          #초기화
          self.url = url
          self.login_mode = login_mode
          self.os_mode = os_mode

          #Driver 연결
          if self.os_mode == 0:
               subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
               option = Options()
               option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

               chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
               try:
                    self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
               except:
                    chromedriver_autoinstaller.install(True)
                    self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
               self.driver.implicitly_wait(10)
          elif self.os_mode == 1:
               options = webdriver.ChromeOptions()
               options.add_argument('--headless')
               options.add_experimental_option("useAutomationExtension", False)
               options.add_experimental_option("excludeSwitches", ["enable-automation"])

               options.add_argument('--disable-gpu')
               options.add_argument('lang=ko_KR')
               UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0'
               options.add_argument('user-agent=' + UserAgent)

               self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
               self.driver.implicitly_wait(10)

          #DB 연결
          db = dbInfo.insertInfo(1)
          self.dbconn = mysql.connector.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'], port=db['port'])
          self.cursor = self.dbconn.cursor(buffered=True)
          self.GmarketData = GmarketData(self.url, self.dbconn, self.cursor, self.driver)

          #로그인 여부
          if self.login_mode == 1:
               self.GmarketData.login()

     def search(self):
          self.GmarketData.total_ads()
          self.dbconn.close()
          self.driver.quit()

     def best(self):
          self.GmarketData.total_best()
          self.dbconn.close()
          self.driver.quit()
          
     def event(self):
          self.GmarketData.total_event()
          self.dbconn.close() 
          self.driver.quit()

     def category(self):
          self.GmarketData.total_category()
          self.dbconn.close()
          self.driver.quit()

     def review(self):
          self.GmarketData.total_review()
          self.dbconn.close()
          self.driver.quit()
     

class GmarketData:
     def __init__(self, url, dbconn, cursor, driver) : 
          #초기화
          self.url = url
          self.dbconn = dbconn
          self.cursor = cursor
          self.driver = driver

     def login(self):
          self.driver.get('https://signinssl.gmarket.co.kr/login/login?url=https://www.gmarket.co.kr/')

          id, password = loginInfo.login(1) #site_option = 1

          user_id = self.driver.find_element(By.XPATH, '//*[@id="typeMemberInputId"]')
          user_id.send_keys(id)
          user_pw = self.driver.find_element(By.XPATH, '//*[@id="typeMemberInputPassword"]')
          user_pw.send_keys(password)

          self.driver.find_element(By.XPATH, '//*[@id="btn_memberLogin"]').click()
          time.sleep(3)
          
     def total_ads(self):
          self.driver.get(self.url)
          self.driver.implicitly_wait(10)

          #html 정보 출력
          html = self.driver.page_source
          soup = BeautifulSoup(html, 'html.parser')
          f = open("./gmarket/gmarket_ads.html", "w", encoding='utf-8')
          f.write(soup.prettify())
          f.close()

          ul = self.driver.find_element(By.XPATH, '//*[@id="section__inner-content-body-container"]/div[2]/div/ul')
          lis = ul.find_elements(By.XPATH, './/li')
          print("Loop Count: ", len(lis))

          i = 1
          for li in lis:
               print("Loop Number: ", i)
               adsYn = 'Y'
               try:
                    productUrl = self.driver.find_element(By.XPATH, '//*[@id="section__inner-content-body-container"]/div[2]/div/ul/li[' + str(i) + ']/div/div[1]/a').get_attribute('href')
                    self.driver.find_element(By.XPATH, '//*[@id="section__inner-content-body-container"]/div[2]/div/ul/li[' + str(i) + ']').click()
                    self.driver.implicitly_wait(5)

                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.find_element(By.XPATH, '/html/body/div[3]/div/span').text
                    productName = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/h1').text
                    productNo = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/span').text
                    productNo = productNo[8:]
                    productNo = (int)(productNo.lstrip('0'), base=0)
                    try:
                         listPrice = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[5]/span[2]/strong').text
                         listPrice = listPrice.replace(',', '').replace('원', '')
                         listPrice = (int)(listPrice, base=0)
                    except NoSuchElementException:
                         listPrice = 0
                    try:
                         price = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[5]/span[3]/strong').text
                         price = price.replace(',', '').replace('원', '')
                         price = (int)(price, base=0)
                    except NoSuchElementException:
                         price = 0

                    discountProvider = 0
                    discountPriceCommerce = 0
                    discountCouponName = 'sale'
                    discountDouble = 0
                    discountRateDouble = (float(listPrice-price)/listPrice)*100
                    try:
                         discountCouponNameDouble = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[5]/span[3]/div/ul/li[2]/em').text
                    except NoSuchElementException:
                         discountCouponNameDouble = '알 수 없음'
                         totalPrice = price
                         bestRank = -1
                         starScore = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[2]/div/span').get_attribute('style')
                    import re
                    width = re.search(r"width:\s*(\d+)", starScore)
                    if width:
                         widthVal = width.group(1)
                    else:
                         widthVal = None
                         widthVal = widthVal.replace('%', '')
                         starScore = (float)(int(widthVal, base=0)) / 20
                         reviewCount = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[2]/span[2]').text
                         reviewCount = reviewCount.replace('(', '').replace(',', '').replace(')', '')
                         reviewCount = (int)(reviewCount, base=0)
                         buyCount = 0
                         saleCompany = 'GMARKET'
                         deliveryPrice = 0
                    try:
                         deliveryType = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/div[2]/div[2]/ul/li[4]/div/div').text
                    except NoSuchElementException:
                         deliveryType = "일반배송"

                    searchWord = self.driver.find_element(By.XPATH, '//*[@id="skip-navigation-search"]/span/button').get_attribute('data-montelena-keyword')
                    adArea = '상품리스트'
                    optionName = '알 수 없음'
                    likeClick = 0
                    salesMan = 'GMARKET'
                    optionNo = 0
                    brandName = '알 수 없음'
                    event = '없음'
                    vendorItemId = productNo
                    collectionDate = datetime.now()
                    commerceType = 'GMARKET'
                    created = datetime.now()
                    updated = datetime.now()
                    updater = 1
                    etcDeliveryName = '알 수 없음'
                    referenceId = 0
                    productCategory = self.driver.find_element(By.XPATH, '/html/body/div[3]/ul/li[2]/a').text
                    dataRanking = i
                    creator = 1

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    data = {
                    'product_name': productName,
                    'product_no':productNo,
                    'list_price': listPrice,
                    'price':price,
                    'discount_provider':discountProvider,
                    'discount_price_commerce': discountPriceCommerce,
                    'discount_coupon_name':discountCouponName,
                    'discount_double':discountDouble,
                    'discount_rate_double':discountRateDouble,
                    'discount_coupon_name_double':discountCouponNameDouble,
                    'total_price':totalPrice,
                    'best_rank':bestRank,
                    'star_score':starScore,
                    'review_count':reviewCount,
                    'buy_count':buyCount,
                    'sale_company':saleCompany,
                    'delivery_price':deliveryPrice,
                    'product_url':productUrl,
                    'delivery_type':deliveryType,
                    'search_word':searchWord,
                    'ad_area':adArea,
                    'option_name':optionName,
                    'like_click':likeClick,
                    'salesman':salesMan,
                    'option_no':optionNo,
                    'brand_name':brandName,
                    'event':event,
                    'vendor_item_id':vendorItemId,
                    'collection_date':collectionDate,
                    'commerce_type':commerceType,
                    'created':created,
                    'updated':updated,
                    'updater':updater,
                    'etc_delivery_name':etcDeliveryName,
                    'reference_id':referenceId,
                    'product_category':productCategory,
                    'ads_yn':adsYn,
                    'data_ranking':dataRanking,
                    'creator':creator
                    }
                    i += 1
                    dbInfo.insert_data("total_ads", self.dbconn, self.cursor, data)

               except NoSuchElementException:
                    print(" == Product URL Not found & Skip..")
                    i += 1
                    continue


     def total_best(self):
          self.driver.get(self.url)
          self.driver.implicitly_wait(10)

          #html 정보 출력
          html = self.driver.page_source
          soup = BeautifulSoup(html, 'html.parser')
          f = open("./gmarket/gmarket_ads.html", "w", encoding='utf-8')
          f.write(soup.prettify())
          f.close()

          ul = self.driver.find_elements(By.XPATH, '//*[@id="gBestWrap"]/div[2]/ul/li')
          print("Loop Count: ", len(ul))
          i = 1
          for li in ul:
               print("Loop Number: ", i)
               try:
                    productUrl = self.driver.find_element(By.XPATH, '//*[@id="gBestWrap"]/div[2]/ul/li[' + str(i) + ']/div[1]/a').get_attribute('href')
                    self.driver.find_element(By.XPATH, '//*[@id="gBestWrap"]/div[2]/ul/li[' + str(i) + ']/div[1]/a').click()
                    self.driver.implicitly_wait(5)

                    productName = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/h1').text
                    try:
                         deliveryType = self.driver.find_element(By.XPATH, '//*[@id="ship_open"]/div/div[1]/span[2]').text
                    except NoSuchElementException:
                         deliveryType = '일반 배송'
                    try:
                         discountCouponName = self.driver.find_element(By.XPATH, '//*[@id="vip_coupon_optimal_banner"]/button/span[1]/span').text
                    except NoSuchElementException:
                         discountCouponName = '없음'
                    try:
                         totalPrice = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[4]/span[2]/strong').text
                         totalPrice = totalPrice.replace(',', '').replace('원', '')
                         totalPrice = (int)(totalPrice, base=0)
                    except NoSuchElementException:
                         totalPrice = 0
                    productOption = '없음'
                    event = '알 수 없음'

                    try:
                         listPrice = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[4]/span[2]/span/span[1]').text
                         listPrice = listPrice.replace(',', '').replace('원', '')
                         listPrice = (int)(listPrice, base=0)
                    except NoSuchElementException:
                         listPrice = 0
                    productNo = str(i)
                    try:
                         price = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[4]/span[3]/strong').text
                         price = price.replace(',', '').replace('원', '')
                         price = (int)(price, base=0)
                    except NoSuchElementException:
                         price = 0

                    if listPrice > price:
                         discountRate = (float(listPrice-price)/listPrice)*100
                         discountPrice = listPrice - price
                    else:
                         discountRate = 0
                         discountPrice = 0
                    discountRateCommerce = discountRate
                    discountCouponName = '알 수 없음'
                    discountDouble = '알 수 없음'
                    discountRateDouble = '알 수 없음'
                    discountCouponNameDouble = '알 수 없음'
                    bestRank = -1
                    try:
                         starScore = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[2]/div/span').get_attribute('style')
                         import re
                         width = re.search(r"width:\s*(\d+)", starScore)
                         if width:
                              widthVal = width.group(1)
                         else:
                              widthVal = None
                              widthVal = widthVal.replace('%', '')
                              starScore = (float)(int(widthVal, base=0)) / 20
                         starScoreBestRate = 0.0
                         starScoreGoodRate = 0.0
                         starScoreBadRate = 0.0
                         starScoreWorstRate = 0.0
                    except NoSuchElementException:
                         starScore = 0.0
                         starScoreBestRate = 0.0
                         starScoreGoodRate = 0.0
                         starScoreBadRate = 0.0
                         starScoreWorstRate = 0.0
                    try:
                         reviewCount = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[2]/span[2]').text
                         reviewCount = reviewCount.replace('(', '').replace(',', '').replace(')', '')
                         reviewCount = (int)(reviewCount, base=0)
                    except NoSuchElementException:
                         reviewCount = 0

                    buyCount = 0
                    saleCompany = 'GMARKET'
                    deliveryPrice = 0
                    collect = '수집완료'
                    brandName = saleCompany
                    category = '알 수 없음'
                    venderItemId = '알 수 없음'
                    dealProjectName = event
                    dealNo = i
                    storeFriend = '알 수 없음'
                    likeCount = 0
                    priceUnit = 0
                    division = category
                    created = datetime.now()
                    updated = datetime.now()
                    updater = 'root'
                    collection_date = datetime.now()
                    commerceType = 'GMARKET'
                    discountProvider = 0
                    discountPriceCommerce = 0
                    etcDeliveryName = ''
                    searchWord = '행사'
                    adsYn = 'Y'
                    url = productUrl
                    creator = 0

                    data = {
                         'product_no': productNo,
                         'product_name':productName,
                         'list_price': listPrice,
                         'price':price,
                         'discount_rate':discountRate,
                         'discount_price': discountPrice,
                         'discount_rate_commerce':discountRateCommerce,
                         'discount_coupon_name':discountCouponName,
                         'discount_double':discountDouble,
                         'discount_rate_double':discountRateDouble,
                         'discount_coupon_name_double':discountCouponNameDouble,
                         'total_price':totalPrice,
                         'best_rank':bestRank,
                         'star_score':starScore,
                         'star_score_best_rate':starScoreBestRate,
                         'star_score_good_rate':starScoreGoodRate,
                         'star_score_bad_rate':starScoreBadRate,
                         'star_score_worst_rate':starScoreWorstRate,
                         'review_count':reviewCount,
                         'buy_count':buyCount,
                         'sale_company':saleCompany,
                         'delivery_price':deliveryPrice,
                         'product_url':productUrl,
                         'product_option':productOption,
                         'delivery_type':deliveryType,
                         'collect':collect,
                         'brand_name':brandName,
                         'category':category,
                         'vendor_item_id':venderItemId,
                         'event':event,
                         'deal_project_name':dealProjectName,
                         'deal_no':dealNo,
                         'store_friend':storeFriend,
                         'like_count':likeCount,
                         'price_unit':priceUnit,
                         'division':division,
                         'created':created,
                         'updated':updated,
                         'updater':updater,
                         'collection_date':collection_date,
                         'commerce_type':commerceType,
                         'discount_provider':discountProvider,
                         'discount_price_commerce':discountPriceCommerce,
                         'etc_delivery_name':etcDeliveryName,
                         'search_word':searchWord,
                         'ads_yn':adsYn,
                         'url':url,
                         'creator':creator
                    }
                    self.driver.back()
                    i += 1
                    dbInfo.insert_data("total_best", self.dbconn, self.cursor, data)

               except NoSuchElementException:
                    print(" == Product URL Not Found & Skip..")
                    i += 1
                    continue


     def total_event(self):
          self.driver.get(self.url)
          self.driver.implicitly_wait(10)

          #html 정보 출력
          html = self.driver.page_source
          soup = BeautifulSoup(html, 'html.parser')
          f = open("./gmarket/gmarket_event.html", "w", encoding='utf-8')
          f.write(soup.prettify())
          f.close()

          ul = self.driver.find_elements(By.XPATH, '//*[@id="container"]/div[2]/ul/li')
          print("Loop Count: ", len(ul))

          #정보 크롤링
          i = 1
          for li in ul:
               print("Loop Number: ", i)
               try:
                    productUrl = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/ul/li[' + str(i) + ']/div/a').get_attribute('href')
                    self.driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/ul/li[' + str(i) + ']/div/a').click()
                    self.driver.implicitly_wait(5)

                    productName = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/h1').text
                    try:
                         deliveryType = self.driver.find_element(By.XPATH, '//*[@id="ship_open"]/div/div[1]/span[2]').text
                    except NoSuchElementException:
                         deliveryType = '일반 배송'
                    try:
                         discountCouponName = self.driver.find_element(By.XPATH, '//*[@id="vip_coupon_optimal_banner"]/button/span[1]/span').text
                    except NoSuchElementException:
                         discountCouponName = '없음'
                    try:
                         totalPrice = self.driver.find_element(By.XPATH, '//*[@id="goodsDetailTab"]/div[3]/div/div[5]/div[1]/span/span/span[2]').text
                         totalPrice = totalPrice.replace(',', '')
                         totalPrice = (int)(totalPrice, base=0)
                    except NoSuchElementException:
                         totalPrice = 0
                    productOption = '없음'
                    event = '알 수 없음'

                    try:
                         listPrice = self.driver.find_element(By.XPATH, '//*[@id="goodsDetailTab"]/div[3]/div/div[5]/div[1]/del/span[2]').text
                         listPrice = listPrice.replace(',', '')
                         listPrice = (int)(listPrice, base=0)
                    except NoSuchElementException:
                         listPrice = 0
                    productNo = str(i)
                    try:
                         price = self.driver.find_element(By.XPATH, '//*[@id="goodsDetailTab"]/div[3]/div/div[5]/div[1]/span/span/span[2]').text
                         price = price.replace(',', '')
                         price = (int)(price, base=0)
                    except NoSuchElementException:
                         price = 0

                    if listPrice > price:
                         discountRate = (float(listPrice-price)/listPrice)*100
                         discountPrice = listPrice - price
                    else:
                         discountRate = 0
                         discountPrice = 0
                    discountRateCommerce = discountRate
                    discountCouponName = '알 수 없음'
                    discountDouble = '알 수 없음'
                    discountRateDouble = '알 수 없음'
                    discountCouponNameDouble = '알 수 없음'
                    bestRank = -1
                    try:
                         starScore = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[2]/div/span').get_attribute('style')
                         import re
                         width = re.search(r"width:\s*(\d+)", starScore)
                         if width:
                              widthVal = width.group(1)
                         else:
                              widthVal = None
                              widthVal = widthVal.replace('%', '')
                              starScore = (float)(int(widthVal, base=0)) / 20
                         starScoreBestRate = 0
                         starScoreGoodRate = 0
                         starScoreBadRate = 0
                         starScoreWorstRate = 0
                    except NoSuchElementException:
                         starScore = 0
                         starScoreBestRate = 0
                         starScoreGoodRate = 0
                         starScoreBadRate = 0
                         starScoreWorstRate = 0
                    try:
                         reviewCount = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[2]/span[2]').text
                         reviewCount = reviewCount.replace('(', '').replace(',', '').replace(')', '')
                         reviewCount = (int)(reviewCount, base=0)
                    except NoSuchElementException:
                         reviewCount = 0
                    buyCount = 0
                    saleCompany = 'GMARKET'
                    deliveryPrice = 0
                    collect = '수집완료'
                    brandName = saleCompany
                    category = '알 수 없음'
                    venderItemId = '알 수 없음'
                    dealProjectName = event
                    dealNo = i
                    storeFriend = '알 수 없음'
                    likeCount = 0
                    priceUnit = 0
                    division = category
                    created = datetime.now()
                    updated = datetime.now()
                    updater = 'root'
                    collection_date = datetime.now()
                    commerceType = 'GMARKET'
                    discountProvider = 0
                    discountPriceCommerce = 0
                    etcDeliveryName = ''
                    searchWord = '행사'
                    adsYn = 'Y'
                    url = productUrl
                    creator = 0

                    data = {
                         'product_no': productNo,
                         'product_name':productName,
                         'list_price': listPrice,
                         'price':price,
                         'discount_rate':discountRate,
                         'discount_price': discountPrice,
                         'discount_rate_commerce':discountRateCommerce,
                         'discount_coupon_name':discountCouponName,
                         'discount_double':discountDouble,
                         'discount_rate_double':discountRateDouble,
                         'discount_coupon_name_double':discountCouponNameDouble,
                         'total_price':totalPrice,
                         'best_rank':bestRank,
                         'star_score':starScore,
                         'star_score_best_rate':starScoreBestRate,
                         'star_score_good_rate':starScoreGoodRate,
                         'star_score_bad_rate':starScoreBadRate,
                         'star_score_worst_rate':starScoreWorstRate,
                         'review_count':reviewCount,
                         'buy_count':buyCount,
                         'sale_company':saleCompany,
                         'delivery_price':deliveryPrice,
                         'product_url':productUrl,
                         'product_option':productOption,
                         'delivery_type':deliveryType,
                         'collect':collect,
                         'brand_name':brandName,
                         'category':category,
                         'vendor_item_id':venderItemId,
                         'event':event,
                         'deal_project_name':dealProjectName,
                         'deal_no':dealNo,
                         'store_friend':storeFriend,
                         'like_count':likeCount,
                         'price_unit':priceUnit,
                         'division':division,
                         'created':created,
                         'updated':updated,
                         'updater':updater,
                         'collection_date':collection_date,
                         'commerce_type':commerceType,
                         'discount_provider':discountProvider,
                         'discount_price_commerce':discountPriceCommerce,
                         'etc_delivery_name':etcDeliveryName,
                         'search_word':searchWord,
                         'ads_yn':adsYn,
                         'url':url,
                         'creator':creator
                    }
                    self.driver.back()
                    i += 1
                    dbInfo.insert_data("total_event", self.dbconn, self.cursor, data)

               except NoSuchElementException:
                    print(" == Product URL Not Found & Skip..")
                    self.driver.back()
                    i += 1
                    continue


     def total_category(self):
          self.driver.get(self.url)
          self.driver.implicitly_wait(10)

          html = self.driver.page_source
          soup = BeautifulSoup(html, 'html.parser')
          f = open("./gmarket/gmarket_category.html", "w", encoding='utf-8')
          f.write(soup.prettify())
          f.close()

          #정보 크롤링
          productCategory = self.driver.find_element(By.XPATH, '//*[@id="box__toggle-filter-c"]/div/ul/li/a/span').text
          div = self.driver.find_elements(By.XPATH, '//*[@id="section__inner-content-body-container"]/div[2]/div')

          print("Loop Count: ", len(div))
          i = 1
          for di in div:
               print("Loop Number: ", i)
               try:
                    productNo = di.find_element(By.CLASS_NAME, 'link__item').get_attribute("data-montelena-goodscode")
                    productUrl = di.find_element(By.CLASS_NAME, 'link__item').get_attribute('href')

                    adsYn = 'N'
                    productName = di.find_element(By.CLASS_NAME, 'text__item').text
                    try:
                         box = di.find_element(By.CLASS_NAME, 'box__price-original')
                         listPrice = box.find_element(By.CLASS_NAME, 'text.text__value').text
                         listPrice = listPrice.replace(',', '').replace('원', '')
                    except NoSuchElementException:
                         print("No ListPrice Info in this product")
                         listPrice = 0
                    try:
                         box = di.find_element(By.CLASS_NAME, 'box__price-seller')
                         price = box.find_element(By.CLASS_NAME, 'text.text__value').text
                         price = price.replace(',', '')
                         price = (int)(price, base=0)
                    except NoSuchElementException:
                         print("No Price Info in this product")
                         price = 0

                    try:
                         box = di.find_element(By.CLASS_NAME, 'box__discount')
                         discountRateDouble = box.find_element(By.CLASS_NAME, 'text.text__value').text
                         if (discountRateDouble[-1] == '원'):
                              discountRateDouble = 0
                         else:
                              discountRateDouble = discountRateDouble.replace('%', '')
                              discountRateDouble = float(int(discountRateDouble, base=0))/100
                    except NoSuchElementException:
                         print("No DiscountRateDouble Info in this product")
                         discountRateDouble = 0
                    discountCouponNameDouble = '알 수 없음'
                    discountProvider = 0
                    discountPriceCommerce = 0
                    discountCouponName = 'sale'
                    discountDouble = 0
                    totalPrice = price
                    bestRank = -1
                    try:
                         starScore = di.find_element(By.CLASS_NAME, 'image__awards-points').get_attribute('style')
                         import re
                         width = re.search(r"width:\s*(\d+)", starScore)
                         if width:
                              widthVal = width.group(1)
                         else:
                              widthVal = None
                              widthVal = widthVal.replace('%', '')
                              starScore = (float)(int(widthVal, base=0)) / 20
                    except NoSuchElementException:
                         print("No StarScore Info in this product")
                         starScore = 0
                    try:
                         box = di.find_element(By.CLASS_NAME, 'list-item.list-item__feedback-count')
                         reviewCount = box.find_element(By.CLASS_NAME, 'text').text
                         reviewCount = reviewCount.replace('(', '').replace(',', '').replace(')', '')
                         reviewCount = (int)(reviewCount, base=0)
                    except NoSuchElementException:
                         print("No ReviewCount Info in this product")
                         reviewCount = 0
                    buyCount = 0
                    saleCompany = 'GMARKET'
                    try:
                         box = di.find_element(By.CLASS_NAME, 'list-item__tag')
                         deliveryPrice = box.find_element(By.CLASS_NAME, 'text__tag').text
                         deliveryPrice = deliveryPrice[4:]
                    except NoSuchElementException:
                         print("No DeliveryPrice Info in this product")
                         deliveryPrice = 0
                    deliveryType = "일반 배송"
                    searchWord = '없음'
                    adArea = '상품리스트'
                    optionName = '알 수 없음'
                    likeClick = 0
                    salesMan = 'GMARKET'
                    optionNo = 0
                    brandName = '알 수 없음'
                    event = '없음'
                    vendorItemId = productNo
                    collectionDate = datetime.now()
                    commerceType = 'GMARKET'
                    created = datetime.now()
                    updated = datetime.now()
                    updater = 1
                    etcDeliveryName = '알 수 없음'
                    referenceId = 0
                    dataRanking = i
                    creator = 1

                    data = {
                         'product_name': productName,
                         'product_no':productNo,
                         'list_price': listPrice,
                         'price':price,
                         'discount_provider':discountProvider,
                         'discount_price_commerce': discountPriceCommerce,
                         'discount_coupon_name':discountCouponName,
                         'discount_double':discountDouble,
                         'discount_rate_double':discountRateDouble,
                         'discount_coupon_name_double':discountCouponNameDouble,
                         'total_price':totalPrice,
                         'best_rank':bestRank,
                         'star_score':starScore,
                         'review_count':reviewCount,
                         'buy_count':buyCount,
                         'sale_company':saleCompany,
                         'delivery_price':deliveryPrice,
                         'product_url':productUrl,
                         'delivery_type':deliveryType,
                         'search_word':searchWord,
                         'ad_area':adArea,
                         'option_name':optionName,
                         'like_click':likeClick,
                         'salesman':salesMan,
                         'option_no':optionNo,
                         'brand_name':brandName,
                         'event':event,
                         'vendor_item_id':vendorItemId,
                         'collection_date':collectionDate,
                         'commerce_type':commerceType,
                         'created':created,
                         'updated':updated,
                         'updater':updater,
                         'etc_delivery_name':etcDeliveryName,
                         'reference_id':referenceId,
                         'product_category':productCategory,
                         'ads_yn':adsYn,
                         'data_ranking':dataRanking,
                         'creator':creator
                    }
                    i += 1
                    dbInfo.insert_data("total_category", self.dbconn, self.cursor, data)

               except NoSuchElementException:
                    print(" == Product URL Not Found & Skip..")
                    i += 1
                    continue


     def total_review(self):
          self.driver.get(self.url)
          self.driver.implicitly_wait(10)

          productName = self.driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/h1').text
          self.driver.find_element(By.XPATH, '//*[@id="container"]/div[6]/div[1]/ul/li[2]/a').click()
          self.driver.implicitly_wait(5)

          # html 정보 저장
          html = self.driver.page_source
          soup = BeautifulSoup(html, 'html.parser')
          f = open("./gmarket/gmarket_review.html", "w", encoding='utf-8')
          f.write(soup.prettify())
          f.close()

          table = self.driver.find_element(By.XPATH, '//*[@id="text-wrapper"]/table')
          tr = table.find_elements(By.XPATH, '//*[@id="text-wrapper"]/table/tbody/tr')
          print("Loop Count: ", len(tr))

          i = 1
          for t in tr:
               print("Loop Number: ", i)
               userName = self.driver.find_element(By.XPATH, '//*[@id="text-wrapper"]/table/tbody/tr[' + str(i) + ']/td[3]/dl/dd[1]').text
               #recommend = self.driver.find_element(By.XPATH, '//*[@id="text-wrapper"]/table/tbody/tr[' + str(i) + ']/td[1]/span[1]/em').text
               #delivery = self.driver.find_element(By.XPATH, '//*[@id="text-wrapper"]/table/tbody/tr[' + str(i) + ']/td[1]/span[2]/em').text
               option = self.driver.find_element(By.XPATH, '//*[@id="text-wrapper"]/table/tbody/tr[' + str(i) + ']/td[2]/p[1]').text
               reviewContent = self.driver.find_element(By.XPATH, '//*[@id="text-wrapper"]/table/tbody/tr[' + str(i) + ']/td[2]/p[2]').text
               date = self.driver.find_element(By.XPATH, '//*[@id="text-wrapper"]/table/tbody/tr[' + str(i) + ']/td[3]/dl/dd[2]').text

               liked = '정보 없음'
               rating = 0
               data = {
                    'product_name': productName,
                    'user_name': userName,
                    'rating': rating,
                    'headline': option,
                    'review_content': reviewContent,
                    'liked': liked
               }
               i += 1
               dbInfo.insert_data("total_review", self.dbconn, self.cursor, data)
