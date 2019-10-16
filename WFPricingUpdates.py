# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:24:00 2018

@author: User
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
#from urllib import request
#from bs4 import BeautifulSoup
import pandas as pd
import time
import os
try:
    #local
    work_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    driver_path = 'C:\\Users\\User\\anaconda3\\chrome\\chromedriver.exe'
    prefs = {'download.default_directory': 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'}
    os.chdir(work_dir)
except:
    #0047
    work_dir = 'N:\\E Commerce\\Public Share\\Automate_Script\\DLpack_Wayfair\\'
    driver_path = 'C:\\Users\\raymond.hung\\chrome\\chromedriver.exe'
    prefs = {'download.default_directory': 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Pricing Updates\\'}
    os.chdir(work_dir)

# Account and Password
login_info = pd.read_csv(work_dir+ 'Account & Password.csv',index_col=0)
WF_Account = login_info.loc['Account', 'CONTENT']
WF_Password = login_info.loc['Password', 'CONTENT']

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(driver_path, chrome_options= options)

# Wayfair extrant website
WF_Extrant = 'https://partners.wayfair.com'
price_update='https://partners.wayfair.com/v/supplier/pricing/app/index'
driver.get(WF_Extrant)
time.sleep(5)

# Input Account, Password and login
insert_act = driver.find_element_by_id('js-username').send_keys(WF_Account)
insert_pwd = driver.find_element_by_id('password_field').send_keys(WF_Password)
driver.find_element_by_xpath('//*[@id="login"]/button').click()
time.sleep(10)

price_download="https://partners.wayfair.com/v/supplier/pricing/exports/export_generic_csv?supplier_id=15379"
CANprice_download="https://partners.wayfair.com/v/supplier/pricing/exports/export_generic_csv?supplier_id=41910"
 

#
#driver.get(price_download)
#time.sleep(15)
#driver.get(CANprice_download)
#time.sleep(15)
#driver.quit()
# switch to US
LOC ={'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
try:
    s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
    s1.select_by_visible_text(LOC['US'])
    driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
except:
    driver.refresh()
    time.sleep(60)
    s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
    s1.select_by_visible_text(LOC['US'])
    driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()

time.sleep(20)

## Click select box to choose US or CAN
for i in range(3):
    try:
        for l in LOC:
            print(l)
            driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
            s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
            s1.select_by_visible_text(LOC[l])
            driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
           
            time.sleep(10)
            
            #download price excel
            price_download="https://partners.wayfair.com/v/supplier/pricing/app/index"
        #    price_download="https://partners.wayfair.com/v/supplier/pricing/exports/export_generic_csv?supplier_id=15379"
            #CANprice_download="https://partners.wayfair.com/v/supplier/pricing/exports/export_generic_csv?supplier_id=41910"
            #US:https://partners.wayfair.com/v/supplier/pricing/exports/export_generic_csv?supplier_id=15379
            #CAN:https://partners.wayfair.com/v/supplier/pricing/exports/export_generic_csv?supplier_id=41910
            driver.get(price_download)
            time.sleep(30)
            
        #    Click "Search" Button
            driver.find_element_by_css_selector(".u-size1of12 .ex-Button--primary").click()
            time.sleep(10)
        #    Click "Export" Button
            driver.find_element_by_css_selector(".ex-Grid-item--row > .ex-Button--secondary").click()
            time.sleep(60)
        #    driver.get(CANprice_download)
        #    time.sleep(10)
        break
    except:
        driver.refresh()
        continue
    
#GO back to US
s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
s1.select_by_visible_text(LOC['US'])
driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
time.sleep(20)

driver.quit()

