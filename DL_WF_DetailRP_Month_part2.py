# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 05:03:26 2018

@author: Chieh-Hsu Yang
"""
import os
import shutil
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Today's date
date_label = time.strftime('%Y%m%d')
# Directory
try:
    #0047
    work_dir = 'C:\\Users\\raymond.hung\\Documents\\Automate_Script\\DLpack_Wayfair\\'
    Download_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\_Download File\\temp_DL_file\\'
    final_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\_Download File\\'
    driver_path = 'C:\\Users\\raymond.hung\\chrome\\chromedriver.exe'
    os.chdir(work_dir)
except:
    #local
    driver_path = 'C:\\Users\\User\\Anaconda3\\chrome\\chromedriver.exe'
    work_dir='C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    Download_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\temp_DL_file\\'
    final_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    os.chdir(work_dir)


# File name
Report_name = 'Monthly_DetailReport_' + date_label + '.csv'

# Account and Password
login_info = pd.read_csv(work_dir+ 'Account & Password.csv',index_col=0)
username = login_info.loc['Account', 'CONTENT']
password = login_info.loc['Password', 'CONTENT']

# Chrome driver setting
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
prefs = {'profile.default_content_settings.popups': '0', 'download.default_directory' : Download_dir}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(driver_path,chrome_options=options)

# Wayfair supplier website
WF_Extrant = 'https://partners.wayfair.com'
Download_page = 'https://partners.wayfair.com/v/supplier/download_center/management/app'
driver.get(WF_Extrant)

LoadingChecker = (By.XPATH, '//*[@id="login"]/button')
WebDriverWait(driver, 120).until(EC.presence_of_element_located(LoadingChecker))
# Input username and password and login
driver.find_element_by_id('js-username').send_keys(username)
driver.find_element_by_id('password_field').send_keys(password)
driver.find_element_by_xpath('//*[@id="login"]/button').click()
time.sleep(5)

try:
    wfe_modal = 'body > div.wfe_modal.modal_transition_bottom.modal_transition_finish > div > span'
    LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
    driver.find_element_by_css_selector(wfe_modal).click()
except:
    pass

# switch to US
LOC ={'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
s1.select_by_visible_text(LOC['US'])
driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
time.sleep(20)

# Turn to Detail Report page
driver.get(Download_page)
time.sleep(20)

# Sort download event by date
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/table/thead/tr/th[4]').click()
time.sleep(5)
# Press Export button
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/table/tbody/tr[1]/td[6]/div/button').click()
time.sleep(20)

driver.quit()
ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name][0]
shutil.move(Download_dir+ori_file, final_dir+Report_name)
