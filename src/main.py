import os
import sys
from eleventh.main import Eleventh
from naver.main import Naver
from coupang.main import Coupang
from gmarket.main import Gmarket

site_selection = 0 #0:coupang. 1:gmarket. 2:11st. 3:naver
operation_mode = 0 #0:search. 1:best. 2:event. 3: category. 4:review
search_keyword = "키워드"
url = "https://www.coupang.com/np/search?component=&q=&channel=user"
login_mode = 0 #O:non-login mode. 1: login model (default mode = 0)
os_mode = 0    #0: Windows, 1: Linux, 2: WSL2  (default mode = 0)

 
if len (sys.argv) < 3:
    print("Command format Error")
    exit(1)
else:
    #argv 값은 문자열이므로, int형 변환 필요  
    site_selection = int(sys.argv[1])
    operation_mode = int(sys.argv[2])

if len(sys.argv) >= 5:  #optional parameter, default value=0
    login_mode = int(sys.argv[4])

if len(sys.argv) >= 6:  #optional parameter, default value=0
    os_mode = int(sys.argv[5])

if site_selection == 0:
    #coupang site
    ### url 전체를 입력받는 대신에, 검색 키워드만을 입력 받아서 url을 자동생성하는 경우 코드 변경
    url = sys.argv[3]
    prefix = "http"

    if not url.startswith(prefix):
        search_keyword = url
        url = url.replace(search_keyword, f"https://www.coupang.com/np/search?component=&q={search_keyword}&channel=user")

    coupang = Coupang(url, login_mode, os_mode)

    if operation_mode == 0:
        #search operation
        coupang.search()
    elif operation_mode == 1:
        #best operation
        coupang.best()
    elif operation_mode == 2:
        #event operation
        coupang.event()
    elif operation_mode == 3:
        #category operation
        coupang.category()
    elif operation_mode == 4:
        #review operation
        coupang.review()
    else:
        print("Operation Selection Error")

elif site_selection == 1:
    #gmarket site
    ### url 전체를 입력받는 대신에, 검색 키워드만을 입력 받아서 url을 자동생성하는 경우 코드 변경
    url = sys.argv[3]
    prefix = "http"

    if not url.startswith(prefix):
        search_keyword = url
        url = url.replace(search_keyword, f"http://browse.gmarket.co.kr/search?keyword={search_keyword}")

    gmarket = Gmarket(url, login_mode, os_mode)

    if operation_mode == 0:
        #search operation
        gmarket.search()
    elif operation_mode == 1:
        #best operation
        gmarket.best()
    elif operation_mode == 2:
        #event operation
        gmarket.event()
    elif operation_mode == 3:
        #category operation
        gmarket.category()
    elif operation_mode == 4:
        #review operation
        gmarket.review()
    else:
        print("Operation Selection Error")

elif site_selection == 2:
    #11st site
    ### url 전체를 입력받는 대신에, 검색 키워드만을 입력 받아서 url을 자동생성하는 경우 코드 변경
    url = sys.argv[3]
    prefix = "http"

    if not url.startswith(prefix):
        search_keyword = url
        url = url.replace(search_keyword, f"https://search.11st.co.kr/Search.tmall?kwd={search_keyword}")

    eleventh = Eleventh(url, login_mode, os_mode)

    if operation_mode == 0:
        #search operation
        eleventh.search()
    elif operation_mode == 1:
        #best operation
        eleventh.best()
    elif operation_mode == 2:
        #event operation
        eleventh.event()
    elif operation_mode == 3:
        #category operation
        eleventh.category()
    elif operation_mode == 4:
        #review operation
        eleventh.review()
    else:
        print("Operation Selection Error")

elif site_selection == 3:
    #Naver site
    ### url 전체를 입력받는 대신에, 검색 키워드만을 입력 받아서 url을 자동생성하는 경우 코드 변경
    url = sys.argv[3]
    prefix = "http"

    if not url.startswith(prefix):
        search_keyword = url
        url = url.replace(search_keyword, f"https://search.shopping.naver.com/search/all?query={search_keyword}")

    naver = Naver(url, login_mode, os_mode)

    if operation_mode == 0:
        #search operation
        naver.search()
    elif operation_mode == 1:
        #best operation
        naver.best()
    elif operation_mode == 2:
        #event operation
        naver.event()
    elif operation_mode == 3:
        #category operation
        naver.category()
    elif operation_mode == 4:
        #review operation
        naver.review()
    else:
        print("Operation Selection Error")
else:
    print("No Such site")
