# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 05:03:26 2018

@author: Chieh-Hsu Yang
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
# Directory
try:
    #0047
    driver_path = 'C:\\Users\\raymond.hung\\chrome\\chromedriver.exe'
    work_dir = 'C:\\Users\\raymond.hung\\Documents\\Automate_Script\\DLpack_Wayfair\\'
    os.chdir(work_dir)
except:
    #local
    driver_path = 'C:\\Users\\User\\Anaconda3\\chrome\\chromedriver.exe'
    work_dir='C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    os.chdir(work_dir)
# Account and Password
login_info = pd.read_csv(work_dir+ 'Account & Password.csv',index_col=0)
username = login_info.loc['Account', 'CONTENT']
password = login_info.loc['Password', 'CONTENT']

# Chrome driver setting
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(driver_path,chrome_options=options)

# Wayfair supplier website
WF_Extrant = 'https://partners.wayfair.com'
#Report_page = 'https://partners.wayfair.com/v/tools/report/dashboard#monthlySalesHistory'#original path
Report_page = 'https://partners.wayfair.com/v/supplier/dashboard/revenue/index'
driver.get(WF_Extrant)

LoadingChecker = (By.XPATH, '//*[@id="login"]/button')
WebDriverWait(driver, 120).until(EC.presence_of_element_located(LoadingChecker))
# Input username and password and login
driver.find_element_by_id('js-username').send_keys(username)
driver.find_element_by_id('password_field').send_keys(password)
driver.find_element_by_xpath('//*[@id="login"]/button').click()
time.sleep(10)

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
css='body > div.wrapper > div:nth-child(1) > header > div > div > div.PH-Header > div > div.ex-Grid-item.ex-Grid-item--flex.u-flexShrink.ex-Grid-item--column.u-justifyEnd > div > div.PH-Header-information > div > span.PH-HeaderDropdown-value'
LoadingChecker = (By.CSS_SELECTOR, css)
WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
driver.find_element_by_css_selector(css).click()
for i in range(1,3):
    if driver.find_element_by_css_selector(css+'> ul > li:nth-child('+str(i)+') > button').text == LOC['US']:
        driver.find_element_by_css_selector(css+'> ul > li:nth-child('+str(i)+') > button').click()
        break
time.sleep(20)

# Turn to Detail Report page
driver.get(Report_page)
time.sleep(20)

# select period 30days
driver.find_element_by_class_name('ex-DropdownInput-valueContainer').click()
driver.find_element_by_id('downshift-0-item-0').click()#Select a preset
driver.find_element_by_class_name('ex-DropdownInput-valueContainer').click()
driver.find_element_by_id('downshift-0-item-2').click()#30days

# Press Apply Filters button
css = 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > main > div:nth-child(2) > span > form > fieldset:nth-child(2) > div > div:nth-child(7) > button'
LoadingChecker = (By.CSS_SELECTOR, css)
WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
driver.find_element_by_css_selector(css).click()

# Press Export button
css= 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > main > div.ex-Box.ex-Block.ex-Block--display-flex.ex-Block--isFlex.ex-Block--flexWrap-wrap.ex-Block--justifyContent-space-between.ex-Block--display-flex > aside > button'
LoadingChecker = (By.CSS_SELECTOR, css)
WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
driver.find_element_by_css_selector(css).click()

time.sleep(15)


driver.quit()
