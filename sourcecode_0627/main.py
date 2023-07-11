import os
import sys
import time
import mysql.connector

import  dbInfo
from eleventh.eleventh import Eleventh
from naver.naver import Naver
from coupang.coupang import Coupang
from gmarket.gmarket import Gmarket

site_selection = 1  #1:coupang. 2:gmarket. 3:11st. 4:naver
operation_mode = 1  #1:search. 2:best. 3:event. 4: category. 5:review
login_mode = 0      #O:non-login mode. 1:login model (default mode = 0)
selenium_mode = 0   #0:Non-Selenium, 1:Hidden-Selenium, 2:Subprocess on Windows, 3:Subprocess on Linux
 
if len(sys.argv) < 4:
    print("Command format Error")
    exit(1)
else:    ## argv 값은 문자열이므로, int형 변환 필요
    site_selection = int(sys.argv[1])
    operation_mode = int(sys.argv[2])
    url = sys.argv[3]

if len(sys.argv) >= 5:  #optional parameter, default value=0
    login_mode = int(sys.argv[4])
if len(sys.argv) >= 6:  #optional parameter, default value=0
    selenium_mode = int(sys.argv[5])

start_time = time.time()
print("Start Time: ", start_time)
########################################################################

if site_selection == 1: #coupang site
    db = dbInfo.getInfo(1)
    dbconn = mysql.connector.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],
                                     port=db['port'])
    cursor = self.dbconn.cursor(buffered=True)

    coupang = Coupang(url, login_mode, os_mode)

    if login_mode == 1:
        selenium_mode = 1    ## Change with Hidden-Selenium mode for dynamic call
        id, passwd = dbInfo.getLoginData(site_selection + 1, dbconn, cursor)
        coupang.selenium_driverCall( selenium_mode )
        coupang.login(id, passwd)

    if operation_mode == 1:         #search operation
        coupang.search()
    elif operation_mode == 2:       #best operation
        coupang.best()
    elif operation_mode == 3:       #event operation
        coupang.event()
    elif operation_mode == 4:       #category operation
        coupang.category()
    elif operation_mode == 5:       #review operation
        coupang.review()
    else:
        print("Operation Selection Error")

elif site_selection == 2:    ## Gmarket site
    db = dbInfo.getInfo(2)
    dbconn = mysql.connector.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],
                                     port=db['port'])
    cursor = dbconn.cursor(buffered=True)
    login_mode = 1      ## always set login-mode for Gmarket Site
    gmarket = Gmarket(url, login_mode, dbconn, cursor)

    selenium_mode = 1    ## Change with Hidden-Selenium mode for login-mode
    gmarket.selenium_driverCall( selenium_mode )
    id, passwd = dbInfo.getLoginData(site_selection, dbconn, cursor)
    gmarket.login(id, passwd)

    if operation_mode == 1:
        gmarket.search()
    elif operation_mode == 2:
        gmarket.best()
    elif operation_mode == 3:
        gmarket.event()
    elif operation_mode == 4:
        gmarket.category()
    elif operation_mode == 5:
        gmarket.review()
    else:
        print("Operation Selection Error")

elif site_selection == 3:    #11st site
    db = dbInfo.insertInfo(2)
    dbconn = mysql.connector.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],
                                     port=db['port'])
    cursor = self.dbconn.cursor(buffered=True)
    eleventh = Eleventh(url, login_mode, os_mode)

    if operation_mode == 0:        #search operation
        eleventh.search()
    elif operation_mode == 1:      #best operation
        eleventh.best()
    elif operation_mode == 2:      #event operation
        eleventh.event()
    elif operation_mode == 3:      #category operation
        eleventh.category()
    elif operation_mode == 4:      #review operation
        eleventh.review()
    else:
        print("Operation Selection Error")

elif site_selection == 4:    #Naver site
    db = dbInfo.insertInfo(2)
    dbconn = mysql.connector.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],
                                     port=db['port'])
    cursor = self.dbconn.cursor(buffered=True)
    naver = Naver(url, login_mode, os_mode)

    if operation_mode == 0:        #search operation
        naver.search()
    elif operation_mode == 1:       #best operation
        naver.best()
    elif operation_mode == 2:        #event operation
        naver.event()
    elif operation_mode == 3:        #category operation
        naver.category()
    elif operation_mode == 4:        #review operation
        naver.review()
    else:
        print("Operation Selection Error")
else:
    print("No Such HomeShopping Site")

end_time = time.time()
print("End Time: ", end_time)
print("#### Running Time: ", round(end_time - start_time, 2), " Seconds")