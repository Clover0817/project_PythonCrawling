import os
import re
import subprocess
import mysql.connector
import chromedriver_autoinstaller
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import loginInfo, dbInfo

class Naver:
    def __init__(self, url, login_mode, os_mode): 
        #초기화
        self.url = url
        self.login_mode = login_mode
        self.os_mode = os_mode
        
        #Driver 연결
        if self.os_mode == 0:
            # import shutil
            # try:
            #     shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
            # except FileNotFoundError:
            #     pass

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
            subprocess.Popen(f'google-chrome --remote-debugging-port=9222  --user-data-dir=data_dir'.split()) 
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
        db = dbInfo.insertInfo(3)
        self.dbconn = mysql.connector.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'], port=db['port'])
        self.cursor = self.dbconn.cursor(buffered=True)
        self.NaverData = NaverData(self.url, self.dbconn, self.cursor, self.driver)

        #로그인 여부
        if self.login_mode == 1:
            NaverData.login(self.driver)

    def search(self):
        self.NaverData.total_ads()
        self.dbconn.close()
        self.driver.quit()
 
    def best(self):
        self.NaverData.total_best()
        self.dbconn.close()
        self.driver.quit()
        
    def event(self):
        self.NaverData.total_event()
        self.dbconn.close() 
        self.driver.quit()

    def category(self):
        self.NaverData.total_category()
        self.dbconn.close()
        self.driver.quit()

    def review(self):
        self.NaverData.total_review()
        self.dbconn.close()
        self.driver.quit()
          

class NaverData:
    def __init__(self, url, dbconn, cursor, driver) : 
        #초기화
        self.url = url
        self.dbconn = dbconn
        self.cursor = cursor
        self.driver = driver
    
    def login(driver):
        driver.get('https://nid.naver.com/nidlogin.login')
        driver.implicitly_wait(5)

        id, password = loginInfo.login(3) #site_option = 3

        driver.execute_script(
            f"document.querySelector('input[id=\"id\"]').setAttribute('value', '{id}')"
        )
        driver.implicitly_wait(2)

        driver.execute_script(
            f"document.querySelector('input[id=\"pw\"]').setAttribute('value', '{password}')"
        )
        driver.implicitly_wait(2)

        driver.find_element(By.ID,'log.login').click()

        
    def total_ads(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./naver/naver_ads.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        #//*[@id="content"]/div[1]/div[2]/div/div[1] /div/div/div[2]/div[1]/a
        #//*[@id="content"]/div[1]/div[2]/div/div[2] /div/div/div[2]/div[1]/a
        lists = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div')
        lis = lists.find_elements(By.XPATH, 'div')
        print("Loop Count: ", len(lis))

        i = 1
        for li in lis:
            print("Loop Number: ", i)
            try:
                productUrl = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_img_area__AdRY_ > div > a').get_attribute('href')
                salesMan = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_mall_area__faH62 > div.basicList_mall_title__FDXX5 > a.basicList_mall__BC5Xu').text
                productCategory = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_info_area__TWvzp > div.basicList_depth__SbZWF').text

                li.find_element(By.CSS_SELECTOR, 'div > div.basicList_img_area__AdRY_ > div > a').click()
                self.driver.implicitly_wait(5)
                self.driver.switch_to.window(self.driver.window_handles[-1]) 

                productName = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3').text
                
                try:
                    listPrice = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > del > span._1LY7DqCnwR').text
                    listPrice = listPrice.replace(',', '')
                    listPrice = (int)(listPrice, base=0)
                except NoSuchElementException:
                    listPrice = 0
                try:
                    price = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > strong > span._1LY7DqCnwR').text
                    price = price.replace(',', '')
                    price = (int)(price, base=0)
                except NoSuchElementException:
                    price = 0

                deliveryType = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1rGSKv6aq_ > div > span:nth-child(1)').text
                deliveryPrice = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1rGSKv6aq_ > div > span:nth-child(2)').text
                
                discountProvider = 0
                discountPriceCommerce = 0
                discountCouponName = 'sale'
                discountDouble = 0
                discountRateDouble = 0
                discountCouponNameDouble = '알 수 없음'

                totalPrice = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > strong > span._1LY7DqCnwR').text
                totalPrice = totalPrice.replace(',', '')
                totalPrice = (int)(totalPrice, base=0)
                
                starScore = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv > div:nth-child(2) > strong').text
                starScore = starScore.replace('\n/\n5', '')
                starScore = float(starScore)
                reviewCount = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv > div:nth-child(1) > a > strong').text
                reviewCount = reviewCount.replace(',', '')
                reviewCount = (int)(reviewCount, base=0)

                productNo = self.driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(1) > td:nth-child(2) > b').text
                saleCompany = self.driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
                brandName = self.driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(2) > td:nth-child(4)').text
                event = self.driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(3) > td:nth-child(2)').text

                bestRank = -1
                buyCount = 0
                adArea = '상품리스트'
                optionNo = 0
            
                optionName = '알 수 없음'
                likeClick = 0
            
                vendorItemId = '알 수 없음'
                searchWord = '즉석밥'
                adsYn = 'Y'
                commerceType = 'NAVER'
                created = datetime.now()
                updated = datetime.now()
                updater = 'root'
                collectionDate = datetime.now()
                etcDeliveryName = '알 수 없음'
                referenceId = 0
                dataRanking = i
                creator = 1

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0]) 
                self.driver.implicitly_wait(5)
                
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
                #print("================")
                #print(data)
                dbInfo.insert_data("total_ads", self.dbconn, self.cursor, data)

            except NoSuchElementException:
                print("No data found and Skip..")
                i += 1
                continue

    def total_best(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./naver/naver_best.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        list = self.driver.find_elements(By.CLASS_NAME, 'imageProduct_item__KZB_F')
        print("Loop Count: ", len(list))
        i = 1
        for lis in list:
            print("Loop Number: ", i)
            productNo = lis.get_attribute('id')
            if productNo == '':
                print("No product number")
                break
            product = lis.find_element(By.CSS_SELECTOR, 'a')
            
            productName = product.find_element(By.CSS_SELECTOR, 'div.imageProduct_text_area__ik6VN > div.imageProduct_title__Wdeb1').text
            productUrl = product.get_attribute('href')
            price = product.find_element(By.CSS_SELECTOR, 'div.imageProduct_text_area__ik6VN > div.imageProduct_price__W6pU1 > strong').text
            price = price.replace(',', '')
            price = (int)(price, base=0)

            listPrice = 0
            discountRate = 0
            discountPrice = 0
            discountRateCommerce = 0
            discountCouponName = '없음'
            discountDouble = '없음'
            discountRateDouble = 0
            discountCouponNameDouble = '없음'
            totalPrice = 0
            bestRank = 0
            starScore = 0
            starScoreBestRate = 0
            starScoreGoodRate = 0
            starScoreBadRate = 0
            starScoreWorstRate = 0
            reviewCount = 0
            buyCount = 0
            saleCompany = '없음'
            deliveryPrice = 0
            productOption = '없음'
            deliveryType = '없음'
            collect = '수집완료'
            brandName = '없음'
            category = '없음'
            venderItemId = '없음'
            event = '없음'
            dealProjectName = '없음'
            dealNo = '없음'
            storeFriend = '없음'
            likeCount = 0
            priceUnit = 0
            division = '없음'
            created = datetime.now()
            updated = datetime.now()
            updater = 'root'
            collection_date = datetime.now()
            commerceType = 'NAVER'
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
            i = i + 1
            dbInfo.insert_data("total_best", self.dbconn, self.cursor, data)


    def total_event(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./naver/naver_event.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        div = self.driver.find_element(By.CSS_SELECTOR, '#tab_container > div > div.listTab_plusdeal_product_area__5gLg_ > div > div')
        list = div.find_elements(By.CLASS_NAME, 'productCard_product_card_view__yt7Ji')
        print("Loop Count: ", len(list))
        i = 1
        for lis in list:
            print("Loop Number: ", i)
            productNo = lis.find_element(By.CLASS_NAME, 'productCard_inner__Q_DtB').get_attribute('id')
            productNo = re.sub(r'[^0-9]', '', productNo)
            if productNo == '':
                break
            productName = lis.find_element(By.XPATH, '//*[@id="title_' + str(productNo) + '"]').text
            trash = lis.find_element(By.XPATH, '//*[@id="title_' + str(productNo) + '"]/span').text
            productName = productName.replace(trash, '')
            productUrl = self.driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > a').get_attribute('href')
            price = self.driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > div.productCard_information__YEkjB > div.productCard_price_area__RleMi > div.productCard_price_wrap__WaX_2 > span.productCard_price__2waKK > span').text
            price = price.replace(',', '')
            price = (int)(price, base=0)
            discountRate = self.driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > div.productCard_information__YEkjB > div.productCard_price_area__RleMi > div.productCard_price_wrap__WaX_2 > span.productCard_discount__tupNR').text
            discountRate = discountRate.replace('%', '').replace('할인율\n', '')
            discountRate = float(discountRate)
            try:
                totalPrice = self.driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > div.productCard_information__YEkjB > div.productCard_price_area__RleMi > div.productCard_benefit__lQNjK > span').text
                totalPrice = totalPrice.replace(',', '')
                totalPrice = (int)(totalPrice, base=0)
            except NoSuchElementException:
                totalPrice = price
            listPrice = 0
            discountPrice = 0
            discountRateCommerce = 0
            discountCouponName = '없음'
            discountDouble = '없음'
            discountRateDouble = 0
            discountCouponNameDouble = '없음'
            bestRank = 0
            starScore = 0
            starScoreBestRate = 0
            starScoreGoodRate = 0
            starScoreBadRate = 0
            starScoreWorstRate = 0
            reviewCount = 0
            buyCount = 0
            saleCompany = '없음'
            deliveryPrice = 0
            productOption = '없음'
            deliveryType = '없음'
            collect = '수집완료'
            brandName = '없음'
            category = '없음'
            venderItemId = '없음'
            event = '없음'
            dealProjectName = '없음'
            dealNo = '없음'
            storeFriend = '없음'
            likeCount = 0
            priceUnit = 0
            division = '없음'
            created = datetime.now()
            updated = datetime.now()
            updater = 'root'
            collection_date = datetime.now()
            commerceType = 'NAVER'
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
            i = i + 1
            dbInfo.insert_data("total_event", self.dbconn, self.cursor, data)


    def total_category(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./naver/naver_category.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()
        
        #정보 크롤링
        div = self.driver.find_element(By.CSS_SELECTOR, '#content > div.style_content__xWg5l')
        list = div.find_element(By.CSS_SELECTOR, 'div.basicList_list_basis__uNBZx')
        lis = list.find_elements(By.CLASS_NAME, 'basicList_item__0T9JD')
        print("Loop Count: ", len(lis))

        i = 1
        for li in lis:
            print("Loop Number: ", i)
            try:
                productUrl = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_img_area__AdRY_ > div > a').get_attribute('href')
                salesMan = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_mall_area__faH62 > div.basicList_mall_title__FDXX5 > a.basicList_mall__BC5Xu').text
                productCategory = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_info_area__TWvzp > div.basicList_depth__SbZWF').text
                productName = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_info_area__TWvzp > div.basicList_title__VfX3c > a').text
                price = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_info_area__TWvzp > div.basicList_price_area__K7DDT > strong > span > span.price_price__LEGN7 > span').text
                price = price.replace(',', '').replace('원', '')
                price = (int)(price, base=0)
                deliveryPrice = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_info_area__TWvzp > div.basicList_price_area__K7DDT > strong > span > span.price_delivery__yw_We').text
                deliveryPrice = re.sub(r'[^0-9]', '', deliveryPrice)
                if deliveryPrice == '':
                    deliveryPrice = 0
                else :
                    deliveryPrice = (int)(deliveryPrice, base=0)
                
                productNo = '알 수 없음'
                listPrice = 0
                discountProvider = 0
                discountPriceCommerce = 0
                discountCouponName = 'sale'
                discountDouble = 0
                discountRateDouble = 0
                discountCouponNameDouble = 'sale'
                totalPrice = 0
                bestRank = -1
                starScore = 0
                reviewCount = 0
                buyCount = 0
                saleCompany = '알 수 없음'
                deliveryType = '알 수 없음'
                searchWord = '카테고리'
                adArea = '알 수 없음'
                optionName = '알 수 없음'
                likeClick = 0
                optionNo = 0
                brandName = salesMan
                event = '알 수 없음'
                vendorItemId = '알 수 없음'
                collectionDate = datetime.now()
                commerceType = 'naver'
                created = datetime.now()
                updated = datetime.now()
                updater = 'root'
                etcDeliveryName = '알 수 없음'
                referenceId = 0
                adsYn = 'N'
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
                self.driver.implicitly_wait(1)
            except NoSuchElementException:
                print("Product url Not found and Skip..")
                i = i + 1
                continue


    def total_review(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)

        #html 정보 출력
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        f = open("./naver/naver_review.html", "w", encoding='utf-8')
        f.write(soup.prettify())
        f.close()

        #정보 크롤링
        productName = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset').find_element(By.CLASS_NAME, '_22kNQuEXmb').text
        reviews = self.driver.find_elements(By.CSS_SELECTOR, '#content > div > div.z7cS6-TO7X > div.FtuIjPoTdk > div._2EO7T3WnKX > ul > li')
        print("Loop Count: ", len(reviews))

        i = 1
        for review in reviews:
            print("Loop Number: ", i)
            userName = review.find_element(By.CLASS_NAME, '_3eMaa46Quy').text
            rating = review.find_element(By.CLASS_NAME, '_15NU42F3kT').text
            headline = '요약 없음'
            reviewContent = review.find_element(By.CLASS_NAME, 'IrHstFoqIi').text
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
            #print(data)
            dbInfo.insert_data("total_review", self.dbconn, self.cursor, data)
         
