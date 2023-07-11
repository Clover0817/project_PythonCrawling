def getInfo(site_selection):
    dbInfo = {}
    if site_selection == 1: ##coupang
        dbInfo = {
        'host':'127.0.0.1', 
        'user':'root', 
        'password':'1234',
        'db':'coupangdb',
        'port':'3306'}    
    elif site_selection == 2: ##gmarket
        dbInfo = {
        'host':'127.0.0.1', 
        'user':'root', 
        'password':'1234',
        'db':'coupangdb',
        'port':'3306'}
    elif site_selection == 3: ##11st
        dbInfo = {
        'host':'127.0.0.1', 
        'user':'root', 
        'password':'1234',
        'db':'coupangdb',
        'port':'3306'}
    elif site_selection == 4: ##naver
        dbInfo = {
        'host':'127.0.0.1', 
        'user':'root', 
        'password':'1234',
        'db':'coupangdb',
        'port':'3306'}
    
    return dbInfo

## get login info. from DB
def getLoginData(mode, dbconn, cursor):
    # try:
    #     result = cursor.execute(f"""
    #         SELECT id=1 FROM tb_login_info
    #     """)
    #
    # except Exception as e :
    #     print(f'***** + Get Login Info Error! >> {e}')
    #     exi(1)
    # print(result)

    return "wanlee02", "Crawling2023@@"


## insert data into DB
def insert_data(mode, dbconn, cursor, data): 
    if mode == "total_search":
        try : 
            cursor.execute(f"""
                INSERT IGNORE INTO tb_total_search
                (
                        PRODUCT_NAME, PRODUCT_NO, LIST_PRICE, PRICE, 
                        DISCOUNT_PROVIDER, DISCOUNT_PRICE_COMMERCE, DISCOUNT_COUPON_NAME, DISCOUNT_DOUBLE, DISCOUNT_RATE_DOUBLE,
                        DISCOUNT_COUPON_NAME_DOUBLE, TOTAL_PRICE, BEST_RANK, STAR_SCORE, REVIEW_COUNT, 
                        BUY_COUNT, SALE_COMPANY, DELIVERY_PRICE, PRODUCT_URL, DELIVERY_TYPE, 
                        SEARCH_WORD, AD_AREA, OPTION_NAME, LIKE_CLICK, SALESMAN, 
                        OPTION_NO, BRAND_NAME, EVENT, VENDOR_ITEM_ID, COLLECTION_DATE, 
                        COMMERCE_TYPE, CREATED, UPDATED, UPDATER, ETC_DELIVERY_NAME,
                        REFERENCE_ID, PRODUCT_CATEGORY, ADS_YN, DATA_RANKING, CREATOR
                ) 
                VALUES (
                        "{data['product_name']}", "{data['product_no']}", "{data['list_price']}", "{data['price']}", 
                        "{data['discount_provider']}", "{data['discount_price_commerce']}", "{data['discount_coupon_name']}", "{data['discount_double']}", "{data['discount_rate_double']}", 
                        "{data['discount_coupon_name_double']}", "{data['total_price']}", "{data['best_rank']}", "{data['star_score']}", "{data['review_count']}", 
                        "{data['buy_count']}", "{data['sale_company']}", "{data['delivery_price']}", "{data['product_url']}", "{data['delivery_type']}", 
                        "{data['search_word']}", "{data['ad_area']}", "{data['option_name']}", "{data['like_click']}", "{data['salesman']}", 
                        "{data['option_no']}", "{data['brand_name']}", "{data['event']}", "{data['vendor_item_id']}", "{data['collection_date']}", 
                        "{data['commerce_type']}", "{data['created']}", "{data['updated']}", "{data['updater']}", "{data['etc_delivery_name']}", 
                        "{data['reference_id']}", "{data['product_category']}", "{data['ads_yn']}", "{data['data_ranking']}", "{data['creator']}"
                ) 
            """)
        except Exception as e :
            print(f'***** + insert_data error! >> {e}')
        finally : 
            dbconn.commit()
            print('****  상품 insert 완료! ')

    if mode == "total_best":
        try : 
            cursor.execute(f"""
                INSERT IGNORE INTO tb_total_best
                (
                    PRODUCT_NO, PRODUCT_NAME, LIST_PRICE, PRICE, DISCOUNT_RATE, 
                    DISCOUNT_PRICE, DISCOUNT_RATE_COMMERCE, DISCOUNT_COUPON_NAME, DISCOUNT_DOUBLE, DISCOUNT_RATE_DOUBLE,
                    DISCOUNT_COUPON_NAME_DOUBLE, TOTAL_PRICE, BEST_RANK, STAR_SCORE, STAR_SCORE_BEST_RATE, 
                    STAR_SCORE_GOOD_RATE, STAR_SCORE_BAD_RATE, STAR_SCORE_WORST_RATE, REVIEW_COUNT, BUY_COUNT, 
                    SALE_COMPANY, DELIVERY_PRICE, PRODUCT_URL, PRODUCT_OPTION, DELIVERY_TYPE,
                    COLLECT, BRAND_NAME, CATEGORY, VENDOR_ITEM_ID, EVENT, 
                    DEAL_PROJECT_NAME, DEAL_NO, STORE_FRIEND, LIKE_COUNT, PRICE_UNIT, 
                    DIVISION, CREATED, UPDATED, UPDATER, COLLECTION_DATE, 
                    COMMERCE_TYPE, DISCOUNT_PROVIDER, DISCOUNT_PRICE_COMMERCE, ETC_DELIVERY_NAME, SEARCH_WORD, 
                    ADS_YN, URL, CREATOR
                ) 
                VALUES (
                    "{data['product_no']}", "{data['product_name']}", "{data['list_price']}", "{data['price']}", "{data['discount_rate']}", 
                    "{data['discount_price']}", "{data['discount_rate_commerce']}", "{data['discount_coupon_name']}", "{data['discount_double']}", "{data['discount_rate_double']}", 
                    "{data['discount_coupon_name_double']}", "{data['total_price']}", "{data['best_rank']}", "{data['star_score']}", "{data['star_score_best_rate']}", 
                    "{data['star_score_good_rate']}", "{data['star_score_bad_rate']}", "{data['star_score_worst_rate']}", "{data['review_count']}", "{data['buy_count']}", 
                    "{data['sale_company']}", "{data['delivery_price']}", "{data['product_url']}", "{data['product_option']}", "{data['delivery_type']}", 
                    "{data['collect']}", "{data['brand_name']}", "{data['category']}", "{data['vendor_item_id']}", "{data['event']}", 
                    "{data['deal_project_name']}", "{data['deal_no']}", "{data['store_friend']}", "{data['like_count']}", "{data['price_unit']}", 
                    "{data['division']}", "{data['created']}", "{data['updated']}", "{data['updater']}", "{data['collection_date']}", 
                    "{data['commerce_type']}", "{data['discount_provider']}", "{data['discount_price_commerce']}", "{data['etc_delivery_name']}", "{data['search_word']}", 
                    "{data['ads_yn']}", "{data['url']}", "{data['creator']}"
                ) 
            """)
        except Exception as e :
            print(f'***** + insert_data error! >> {e}')
        finally : 
            dbconn.commit()
            print('****  상품 insert 완료! ')

    if mode == "total_event":
        try : 
            cursor.execute(f"""
                INSERT IGNORE INTO tb_total_event
                (
                    PRODUCT_NO, PRODUCT_NAME, LIST_PRICE, PRICE, DISCOUNT_RATE, 
                    DISCOUNT_PRICE, DISCOUNT_RATE_COMMERCE, DISCOUNT_COUPON_NAME, DISCOUNT_DOUBLE, DISCOUNT_RATE_DOUBLE,
                    DISCOUNT_COUPON_NAME_DOUBLE, TOTAL_PRICE, BEST_RANK, STAR_SCORE, STAR_SCORE_BEST_RATE, 
                    STAR_SCORE_GOOD_RATE, STAR_SCORE_BAD_RATE, STAR_SCORE_WORST_RATE, REVIEW_COUNT, BUY_COUNT, 
                    SALE_COMPANY, DELIVERY_PRICE, PRODUCT_URL, PRODUCT_OPTION, DELIVERY_TYPE,
                    COLLECT, BRAND_NAME, CATEGORY, VENDOR_ITEM_ID, EVENT, 
                    DEAL_PROJECT_NAME, DEAL_NO, STORE_FRIEND, LIKE_COUNT, PRICE_UNIT, 
                    DIVISION, CREATED, UPDATED, UPDATER, COLLECTION_DATE, 
                    COMMERCE_TYPE, DISCOUNT_PROVIDER, DISCOUNT_PRICE_COMMERCE, ETC_DELIVERY_NAME, SEARCH_WORD, 
                    ADS_YN, URL, CREATOR
                ) 
                VALUES (
                    "{data['product_no']}", "{data['product_name']}", "{data['list_price']}", "{data['price']}", "{data['discount_rate']}", 
                    "{data['discount_price']}", "{data['discount_rate_commerce']}", "{data['discount_coupon_name']}", "{data['discount_double']}", "{data['discount_rate_double']}", 
                    "{data['discount_coupon_name_double']}", "{data['total_price']}", "{data['best_rank']}", "{data['star_score']}", "{data['star_score_best_rate']}", 
                    "{data['star_score_good_rate']}", "{data['star_score_bad_rate']}", "{data['star_score_worst_rate']}", "{data['review_count']}", "{data['buy_count']}", 
                    "{data['sale_company']}", "{data['delivery_price']}", "{data['product_url']}", "{data['product_option']}", "{data['delivery_type']}", 
                    "{data['collect']}", "{data['brand_name']}", "{data['category']}", "{data['vendor_item_id']}", "{data['event']}", 
                    "{data['deal_project_name']}", "{data['deal_no']}", "{data['store_friend']}", "{data['like_count']}", "{data['price_unit']}", 
                    "{data['division']}", "{data['created']}", "{data['updated']}", "{data['updater']}", "{data['collection_date']}", 
                    "{data['commerce_type']}", "{data['discount_provider']}", "{data['discount_price_commerce']}", "{data['etc_delivery_name']}", "{data['search_word']}", 
                    "{data['ads_yn']}", "{data['url']}", "{data['creator']}"
                ) 
            """)
        except Exception as e :
            print(f'***** + insert_data error! >> {e}')
        finally : 
            dbconn.commit()
            print('****  상품 insert 완료! ')

    if mode == "total_category":
        try : 
            cursor.execute(f"""
                INSERT IGNORE INTO tb_total_category
                (
                    PRODUCT_NAME, PRODUCT_NO, LIST_PRICE, PRICE, 
                    DISCOUNT_PROVIDER, DISCOUNT_PRICE_COMMERCE, DISCOUNT_COUPON_NAME, DISCOUNT_DOUBLE, DISCOUNT_RATE_DOUBLE,
                    DISCOUNT_COUPON_NAME_DOUBLE, TOTAL_PRICE, BEST_RANK, STAR_SCORE, REVIEW_COUNT, 
                    BUY_COUNT, SALE_COMPANY, DELIVERY_PRICE, PRODUCT_URL, DELIVERY_TYPE, 
                    SEARCH_WORD, AD_AREA, OPTION_NAME, LIKE_CLICK, SALESMAN, 
                    OPTION_NO, BRAND_NAME, EVENT, VENDOR_ITEM_ID, COLLECTION_DATE, 
                    COMMERCE_TYPE, CREATED, UPDATED, UPDATER, ETC_DELIVERY_NAME,
                    REFERENCE_ID, PRODUCT_CATEGORY, ADS_YN, DATA_RANKING, CREATOR
                ) 
                VALUES (
                    "{data['product_name']}", "{data['product_no']}", "{data['list_price']}", "{data['price']}", 
                    "{data['discount_provider']}", "{data['discount_price_commerce']}", "{data['discount_coupon_name']}", "{data['discount_double']}", "{data['discount_rate_double']}", 
                    "{data['discount_coupon_name_double']}", "{data['total_price']}", "{data['best_rank']}", "{data['star_score']}", "{data['review_count']}", 
                    "{data['buy_count']}", "{data['sale_company']}", "{data['delivery_price']}", "{data['product_url']}", "{data['delivery_type']}", 
                    "{data['search_word']}", "{data['ad_area']}", "{data['option_name']}", "{data['like_click']}", "{data['salesman']}", 
                    "{data['option_no']}", "{data['brand_name']}", "{data['event']}", "{data['vendor_item_id']}", "{data['collection_date']}", 
                    "{data['commerce_type']}", "{data['created']}", "{data['updated']}", "{data['updater']}", "{data['etc_delivery_name']}", 
                    "{data['reference_id']}", "{data['product_category']}", "{data['ads_yn']}", "{data['data_ranking']}", "{data['creator']}"
                ) 
            """)
        except Exception as e :
            print(f'***** + insert_data error! >> {e}')
        finally : 
            dbconn.commit()
            print('****  상품 insert 완료! ')

    if mode == "total_review":
        try : 
            cursor.execute(f"""
                INSERT IGNORE INTO tb_total_review
                (
                    PRODUCT_NAME, USER_NAME, RATING, HEADLINE, REVIEW_CONTENT, LIKED
                ) 
                VALUES (
                    "{data['product_name']}", "{data['user_name']}", "{data['rating']}", "{data['headline']}", "{data['review_content']}", "{data['liked']}"
                ) 
            """)
        except Exception as e :
            print(f'***** + insert_data error! >> {e}')
        finally : 
            dbconn.commit()
            print('****  상품 insert 완료! ')
