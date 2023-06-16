import os
import re
import subprocess
import mysql.connector
import chromedriver_autoinstaller
import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support  import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


import loginInfo, dbInfo

class Eleventh:
    def __init__(self, url, login_mode, os_mode): 
        #초기화
        self.url = url
        self.login_mode = login_mode
        self.os_mode = os_mode
        
        #Driver 연결
        if self.os_mode == 0:
            self.callprocess = subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
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
            self.callprocess = subprocess.Popen(f'google-chrome --remote-debugging-port=9222  --user-data-dir=data_dir'.split())
            chrome_option = Options()
            chrome_option.add_argument('headless')
            chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
            try:
                self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver', options=chrome_option)
            except:
                chromedriver_autoinstaller.install(True)

            self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver', options=chrome_option)
            self.driver.implicitly_wait(10)

        elif self.os_mode == 2:
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches",["enable-automation"])

            options.add_argument('--disable-gpu')
            options.add_argument('lang=ko_KR')
            UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36'
            options.add_argument('user-agent=' + UserAgent)

            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.implicitly_wait(10)

        #DB 연결
        db = dbInfo.insertInfo(2)
        self.dbconn = mysql.connector.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'], port=db['port'])
        self.cursor = self.dbconn.cursor(buffered=True)
        self.EleventhData = EleventhData(self.url, self.dbconn, self.cursor, self.driver)

        #로그인 여부
        if self.login_mode == 1:
            self.EleventhData.login()

    def search(self):
        self.EleventhData.total_ads()
        self.dbconn.close()
        if self.login_mode == 1:  ## logout required
            print("Logout is done")
            self.driver.get('https://login.11st.co.kr/login/Logout.tmall')
            WebDriverWait(self.driver, 10).until(EC.title_is)
        self.driver.quit()
        if self.login_mode < 2:
            self.callprocess.terminate()
 
    def best(self):
        self.EleventhData.total_best()
        self.dbconn.close()
        if self.login_mode == 1:  ## logout required
            print("Logout is done")
            self.driver.get('https://login.11st.co.kr/login/Logout.tmall')
            WebDriverWait(self.driver, 10).until(EC.title_is)
        self.driver.quit()
        if self.login_mode < 2:
            self.callprocess.terminate()
        
    def event(self):
        self.EleventhData.total_event()
        self.dbconn.close()
        if self.login_mode == 1:  ## logout required
            print("Logout is done")
            self.driver.get('https://login.11st.co.kr/login/Logout.tmall')
            WebDriverWait(self.driver, 10).until(EC.title_is)
        self.driver.quit()
        if self.login_mode < 2:
            self.callprocess.terminate()

    def category(self):
        self.EleventhData.total_category()
        self.dbconn.close()
        if self.login_mode == 1:  ## logout required
            print("Logout is done")
            self.driver.get('https://login.11st.co.kr/login/Logout.tmall')
            WebDriverWait(self.driver, 10).until(EC.title_is)
        self.driver.quit()
        if self.login_mode < 2:
            self.callprocess.terminate()

    def review(self):
        self.EleventhData.total_review()
        self.dbconn.close()
        if self.login_mode == 1:  ## logout required
            print("Logout is done")
            self.driver.get('https://login.11st.co.kr/login/Logout.tmall')
            WebDriverWait(self.driver, 10).until(EC.title_is)
        self.driver.quit()
        if self.login_mode < 2:
            self.callprocess.terminate()
          

class EleventhData:
    def __init__(self, url, dbconn, cursor, driver) : 
        #초기화
        self.url = url
        self.dbconn = dbconn
        self.cursor = cursor
        self.driver = driver
    
    def login(self):
        self.driver.get('https://login.11st.co.kr/auth/v2/login')
        WebDriverWait(self.driver, 10).until(EC.title_is)

        id, password = loginInfo.login(2) #site_option = 2

        id_input = self.driver.find_element(By.CSS_SELECTOR, "#memId")
        id_input.send_keys(id)

        pw_input = self.driver.find_element(By.CSS_SELECTOR, "#memPwd")
        pw_input.send_keys(password)

        time.sleep(1)
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > form > fieldset > div.c-buttons > button")
        login_btn.click()
        WebDriverWait(self.driver, 10).until(EC.title_is)
        time.sleep(3)
        #driver.find_element(By.XPATH, '//*[@id="arModalQuickInfo"]/div/div/div[4]/a').click()

        
    def total_ads(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.title_is)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./eleventh/eleventh_ads.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        i = 0
        uls = self.driver.find_elements(By.CSS_SELECTOR, '#layBodyWrap > div > div > div.l_search_content > div > section > ul')
        print("Outer Loop Count: ", len(uls) )

        for ul in uls:
            lis = ul.find_elements(By.CSS_SELECTOR, 'li')
            print("Inner Loop Count: ", len(lis))
            for li in lis:
                data = {}
                print("Loop Number: ", i, ", window index = ", self.driver.window_handles)
                try: 
                    productName = li.find_element(By.CLASS_NAME, 'c_prd_name').text
                    price = li.find_element(By.CLASS_NAME, 'price').find_element(By.CLASS_NAME, 'value').text
                    price = price.replace(',', '')
                    price = (int)(price, base=0)

                    deliveryPrice = li.find_element(By.CLASS_NAME, 'delivery').text
                    
                    productUrl = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    product = li.find_element(By.CSS_SELECTOR, 'div > div.c_prd_thumb > a')
                    # product.click()
                    # self.driver.implicitly_wait(5)
                    # self.driver.switch_to.window(self.driver.window_handles[-1])

                    discountProvider = 0
                    discountPriceCommerce = 0
                    discountCouponName = 'sale'
                    discountDouble = 0
                    
                    discountCouponNameDouble = '알 수 없음'
                    totalPrice = price
                    bestRank = -1
                    productNo = '알 수 없음'
                    listPrice = 0
                    discountRateDouble = 0
                    starScore = 0
                    reviewCount = 0
                    searchWord = '즉석밥'
                    adsYn = 'Y'
                    commerceType = 'ELEVEN_TH'
                    buyCount = 0
                    saleCompany = 'ELEVEN_TH'
                    deliveryType = "로켓배송"
                    adArea = '상품리스트'
                    optionName = '알 수 없음'
                    likeClick = 0
                    salesMan = 'ELEVEN_TH'
                    optionNo = 0
                    brandName = '알 수 없음'
                    event = '없음'
                    vendorItemId = '알 수 없음'
                    collectionDate = datetime.now()
                    created = datetime.now()
                    updated = datetime.now()
                    updater = 1
                    etcDeliveryName = '알 수 없음'
                    referenceId = 0
                    productCategory = '알 수 없음'
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
                    dbInfo.insert_data("total_ads", self.dbconn, self.cursor, data)

                except NoSuchElementException:
                    print("Product name Not found and Skip..")
                    i += 1
                    continue

    def total_best(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.title_is)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./eleventh/eleventh_best.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        ul = self.driver.find_element(By.CSS_SELECTOR, '#bestPrdList > div:nth-child(2) > ul')
        lists = ul.find_elements(By.CSS_SELECTOR, 'li')

        i = 1
        #data={}
        print("Loop Count: ", len(lists))
        for li in lists:
            print("Loop Number: ", i)
            productNo = li.get_attribute('id')
            productNo = re.sub(r'[^0-9]', '', productNo)
            productUrl = li.find_element(By.CSS_SELECTOR, 'div > a').get_attribute('href')
            bestRank = li.find_element(By.CLASS_NAME, 'best').text
            bestRank = (int)(bestRank, base=0)
            info = li.find_element(By.CLASS_NAME, 'pname')
            productName = info.find_element(By.CSS_SELECTOR, 'p').text
            try:
                discountRate = info.find_element(By.CSS_SELECTOR, 'div.price_info.cfix > span.sale').text
                discountRate = discountRate.replace('%', '')
                discountRate = (float)(int(discountRate, base=0))/100
            except NoSuchElementException:
                discountRate = 0
            try:
                listPrice = info.find_element(By.CLASS_NAME, 'normal_price').text
                listPrice = listPrice.replace(',', '').replace('원', '')
                listPrice = (int)(listPrice, base=0)
            except NoSuchElementException:
                listPrice = 0
            price = li.find_element(By.CLASS_NAME, 'sale_price').text
            price = price.replace(',', '')
            price = (int)(price, base=0)

            discountPrice = 0
            discountRateCommerce = 0
            discountCouponName = '알수 없음'
            discountDouble = '알수 없음'
            discountRateDouble = 0
            discountCouponNameDouble = '알수 없음'
            totalPrice = 0
            starScore = 0
            starScoreBestRate = 0
            starScoreGoodRate = 0
            starScoreBadRate = 0
            starScoreWorstRate = 0
            reviewCount = 0
            buyCount = 0
            saleCompany = '알수 없음'
            deliveryPrice = 0
            productOption = '알수 없음'
            deliveryType = '알수 없음'
            collect = '수집완료'
            brandName = saleCompany
            category = '알 수 없음'
            venderItemId = '알 수 없음'
            event = '알 수 없음'
            dealProjectName = 'event'
            dealNo = i
            storeFriend = '알 수 없음'
            likeCount = 0
            priceUnit = 0
            division = '알 수 없음'
            created = datetime.now()
            updated = datetime.now()
            updater = 'root'
            collection_date = datetime.now()
            commerceType = 'ELEVENTH'
            discountProvider = 0
            discountPriceCommerce = 0
            etcDeliveryName = ''
            searchWord = '베스트'
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

            i += 1
            dbInfo.insert_data("total_best", self.dbconn, self.cursor, data)
            

    def total_event(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.title_is)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./eleventh/eleventh_event.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        uls = self.driver.find_elements(By.CLASS_NAME, 'cfix')
        print("Outer Loop Count: ", len(uls) )

        i = 1
        for ul in uls:
            lis = ul.find_elements(By.CSS_SELECTOR, 'li')
            print("Inner Loop Count: ", len(lis))
            for li in lis :
                print("Loop Number: ", i)
                try :
                    productNo = li.get_attribute('prdno')
                    info = li.find_element(By.CSS_SELECTOR, 'div > a')
                    productUrl = info.get_attribute('href')
                    productName = info.find_element(By.CLASS_NAME, 'fs_16').text
                    discountRate = self.driver.find_element(By.CLASS_NAME, 'sale').get_attribute('innerText')
                    discountRate = re.sub(r'[^0-9]', '', discountRate)
                    discountRate = (float)(int(discountRate, base=0))/100
                    try:
                        listPrice = info.find_element(By.CLASS_NAME, 'normal_price').text
                        listPrice = listPrice.replace(',', '').replace('원', '')
                        listPrice = (int)(listPrice, base=0)
                    except NoSuchElementException:
                        listPrice = 0
                    price = li.find_element(By.CLASS_NAME, 'sale_price').text
                    price = re.sub(r'[^0-9]', '', price)
                    price = (int)(price, base=0)
                    try:
                        buyCount = info.find_element(By.CLASS_NAME, 'puchase_num').text
                        buyCount = re.sub(r'[^0-9]', '', buyCount)
                        if buyCount=='':
                            buyCount = 0
                        else :
                            buyCount = (int)(buyCount, base=0)
                    except NoSuchElementException:
                        buyCount = 0
                except NoSuchElementException:
                    print("Product number Not found and Skip..")
                    i = i + 1
                    continue

                discountPrice = 0
                discountRateCommerce = 0
                discountCouponName = '알수 없음'
                discountDouble = '알수 없음'
                discountRateDouble = 0
                discountCouponNameDouble = '알수 없음'
                totalPrice = 0
                bestRank = -1
                starScore = 0
                starScoreBestRate = 0
                starScoreGoodRate = 0
                starScoreBadRate = 0
                starScoreWorstRate = 0
                reviewCount = 0
                saleCompany = '알수 없음'
                deliveryPrice = 0
                productOption = '알수 없음'
                deliveryType = '알수 없음'
                collect = '수집완료'
                brandName = saleCompany
                category = '알 수 없음'
                venderItemId = '알 수 없음'
                event = '알 수 없음'
                dealProjectName = 'event'
                dealNo = i
                storeFriend = '알 수 없음'
                likeCount = 0
                priceUnit = 0
                division = '알 수 없음'
                created = datetime.now()
                updated = datetime.now()
                updater = 'root'
                collection_date = datetime.now()
                commerceType = 'ELEVENTH'
                discountProvider = 0
                discountPriceCommerce = 0
                etcDeliveryName = ''
                searchWord = '이벤트'
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

                i += 1
                dbInfo.insert_data("total_event", self.dbconn, self.cursor, data)


    def total_category(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.title_is)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./eleventh/eleventh_category.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()
        
        #정보 크롤링
        uls = self.driver.find_elements(By.CLASS_NAME, 'tt_listbox')
        i = 1
        print("Outer Loop Count: ", len(uls) )

        for ul in uls:
            lis = ul.find_elements(By.CSS_SELECTOR, 'li')
            print("Inner Loop Count: ", len(lis))
            for li in lis :
                print("Loop Number: ", i)
                try :
                    productNo = li.get_attribute('id')
                    productNo = re.sub(r'[^0-9]', '', productNo)
                    a = li.find_element(By.CSS_SELECTOR, 'div > div.list_info > p > a')
                    productUrl = a.get_attribute('href')
                    productName = a.text
                    starScore = li.find_element(By.CLASS_NAME, 'selr_star').text
                    starScore = starScore.replace('판매자 평점 별5개 중 ', '').replace('개', '')
                    starScore = float(starScore)
                    reviewCount = li.find_element(By.CLASS_NAME, 'review').text
                    reviewCount = re.sub(r'[^0-9]', '', reviewCount)
                    likeClick = li.find_element(By.CSS_SELECTOR, 'div > div.list_info > div > div.info_btm > div.def_likethis > button > strong').text
                    if likeClick == '' :
                        likeClick = 0
                    else :
                        likeClick = re.sub(r'[^0-9]', '', likeClick)
                        likeClick = (int)(likeClick, base=0)
                    discountRate = self.driver.find_element(By.CLASS_NAME, 'sale').get_attribute('innerText')
                    discountRate = re.sub(r'[^0-9]', '', discountRate)
                    discountRate = (float)(int(discountRate, base=0))/100
                    try:
                        listPrice = li.find_element(By.CLASS_NAME, 'normal_price').text
                        listPrice = listPrice.replace(',', '').replace('원', '')
                        listPrice = (int)(listPrice, base=0)
                    except NoSuchElementException:
                        listPrice = 0
                    price = li.find_element(By.CLASS_NAME, 'sale_price').text
                    price = re.sub(r'[^0-9]', '', price)
                    price = (int)(price, base=0)
                    deliveryPrice = li.find_element(By.CSS_SELECTOR, 'div > div.list_price > div.deliver > p:nth-child(2) > span').text
                    deliveryPrice = re.sub(r'[^0-9]', '', deliveryPrice)
                    if deliveryPrice == '':
                        deliveryPrice = 0
                    else :
                        deliveryPrice = (int)(deliveryPrice, base=0)
                except NoSuchElementException:
                    print("Product number Not found and Skip..")
                    i = i + 1
                    continue

                discountCouponName = '알수 없음'
                discountDouble = '알수 없음'
                discountRateDouble = 0
                discountCouponNameDouble = '알수 없음'
                totalPrice = 0
                bestRank = -1
                buyCount = 0
                saleCompany = '알수 없음'
                deliveryPrice = 0
                deliveryType = '알수 없음'
                brandName = saleCompany
                productCategory = '알 수 없음'
                event = '알 수 없음'
                optionNo = i
                adArea = '알 수 없음'
                optionName = '알 수 없음'
                vendorItemId = '알 수 없음'
                referenceId = '알 수 없음'
                dataRanking = -1
                created = datetime.now()
                updated = datetime.now()
                updater = 'root'
                collectionDate = datetime.now()
                commerceType = 'ELEVENTH'
                salesMan = 'ELEVENTH'
                discountProvider = 0
                discountPriceCommerce = 0
                etcDeliveryName = ''
                searchWord = '이벤트'
                adsYn = 'Y'
                creator = 0

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


    def total_review(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.title_is)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./eleventh/eleventh_review.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        productName = self.driver.find_element(By.CSS_SELECTOR, '#layBodyWrap > div > div.s_product.s_product_detail > div.l_product_cont_wrap > div > div.l_product_view_wrap > div.l_product_summary > div.l_product_side_info > div.c_product_info_title > h1').text

        #iframes = self.driver.find_elements(By.CSS_SELECTOR, 'iframe')
        #for iframe in iframes:
        #    print(iframe.get_attribute('name'))
        self.driver.switch_to.frame("ifrmReview")


        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./eleventh/eleventh_review_iframe.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        ul = self.driver.find_element(By.XPATH, '//*[@id="review-list-page-area"]')
        lis = ul.find_elements(By.XPATH, './/li')
        print("Loop Count: ", len(lis))
        i = 1
        for li in lis:
            print("Loop Number: ", i)
            reviewContent = self.driver.find_element(By.XPATH,
                        '//*[@id="review-list-page-area"]/ul/li["' + str(i) + '"]/div/div/div[2]/p[1]').text
            userName = self.driver.find_element(By.XPATH,
                        '//*[@id = "review-list-page-area"] / ul / li["' + str(i) + '"] / dl / dt').text
            rating = self.driver.find_element(By.XPATH,
                        '//*[@id="review-list-page-area"] / ul / li["' + str(i) + '"] / div / p[1] / span').text
            rating = rating.replace('평점 별 5점 중','')
            rating = (int)(rating, base=0)
            headline = '요약 없음'
            liked = '평가 없음'

            data = {
                'product_name':productName,
                'user_name':userName,
                'rating':rating,
                'headline':headline,
                'review_content':reviewContent,
                'liked':liked
            }
            i = i + 1
            dbInfo.insert_data("total_review", self.dbconn, self.cursor, data)
