def login(site_selection):
    if site_selection == 0:   ## coupang
            id = "wanyeon.lee@gmail.com"
            password = "Crawling2023@@"
    elif site_selection == 1: ## gmarket
            id = "wanlee02"
            password = "Crawling2023@@"
    elif site_selection == 2: ## 11st
            id = "wanlee02"
            password = "Crawling2023@@"
    elif site_selection == 3: ## naver
            id = "bestsy777"
            password = "muze2005;"
    else:
        print("로그인 오류")

    return id, password