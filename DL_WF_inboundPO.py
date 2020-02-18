import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import shutil
import os

# Today's date
date_label = time.strftime('%Y%m%d')
try:
    #local test Directory
    work_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    Download_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\temp_DL_file\\'
    final_Inv_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    CAN_final_Inv_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    driver_path = 'C:\\Users\\User\\Anaconda3\\chrome\\chromedriver.exe'
    os.chdir(work_dir)
except:
    # 0047Directory
    work_dir = 'N:\\E Commerce\\Public Share\\Automate_Script\\DLpack_Wayfair\\'
    Download_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG Inbound PO\\temp_DL_file\\'
    final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG Inbound PO\\'
    CAN_final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG CAN Inbound PO\\'
    driver_path = 'C:\\Users\\raymond.hung\\chrome\\chromedriver.exe'
    os.chdir(work_dir)

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

# Click select box to choose US or CAN
LOC = {'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
for l in LOC:
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
    
    inbound_page = 'https://partners.wayfair.com/v/wfs/orders/inbound/index'
    driver.get(inbound_page)
    
    # Click dropdown menus and download excel file
    try:
        s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
        s1.select_by_visible_text(LOC[l])    
        driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
        time.sleep(10)
        # Download CSV
        LoadingChecker = (By.XPATH, '/html/body/div[2]/div[4]/div/div/div[2]/div/main/div[2]/div[2]/div/div/p/button')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
        driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[2]/div/main/div[2]/div[2]/div/div/p/button').click()
        time.sleep(120)
        ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name][0]
    except:
        driver.refresh()
        time.sleep(30)
        s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
        s1.select_by_visible_text(LOC[l])    
        driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
        time.sleep(10)
        # Download CSV
        LoadingChecker = (By.XPATH, '/html/body/div[2]/div[4]/div/div/div[2]/div/main/div[2]/div[2]/div/div/p/button')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
        driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[2]/div/main/div[2]/div[2]/div/div/p/button').click()
        time.sleep(120)
        ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name][0]
        
    # File name
    total_name = 'inbound_order' + date_label + '.csv' 
    if l =="US":
        shutil.move(Download_dir + ori_file, final_Inv_dir + total_name)
    elif l=="CAN":
        shutil.move(Download_dir + ori_file, CAN_final_Inv_dir + total_name)

#GO back to US
try:
    s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
    s1.select_by_visible_text(LOC['US'])
    driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
    time.sleep(20)
except:
    driver.refresh()
    time.sleep(30)
    s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
    s1.select_by_visible_text(LOC['US'])
    driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
    time.sleep(20)

driver.quit() 
