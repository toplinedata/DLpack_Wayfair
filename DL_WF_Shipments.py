import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import shutil
import os

print(datetime.today().strftime("%Y%m%d"))

# Today's date
date_label = time.strftime('%Y.%m.%d')
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
    Download_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG Daily AC Data\\temp_DL_file\\'
    final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG Daily AC Data\\'
    CAN_final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG CAN Daily AC Data\\'
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

#Skip Wayfair system info.
try:
    wfe_modal = 'body > div.wfe_modal.modal_transition_bottom.modal_transition_finish > div > span'
    LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
    driver.find_element_by_css_selector(wfe_modal).click()
except:
    pass

LOC = {'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
for l in LOC:
    # Click select box to choose US or CAN
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
    count = 0
    while 1==1:
        try:
            css='body > div.wrapper > div:nth-child(1) > header > div > div > div.PH-Header > div > div.ex-Grid-item.ex-Grid-item--flex.u-flexShrink.ex-Grid-item--column.u-justifyEnd > div > div.PH-Header-information > div > span.PH-HeaderDropdown-value'
            LoadingChecker = (By.CSS_SELECTOR, css)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(css).click()
            for i in range(1,3):
                if driver.find_element_by_css_selector(css+'> ul > li:nth-child('+str(i)+') > button').text == LOC[l]:
                    driver.find_element_by_css_selector(css+'> ul > li:nth-child('+str(i)+') > button').click()
                    time.sleep(30)
                    break
            break
        except:
            driver.refresh()
            if count == 10:
                print("over count")
                break
            count+=1
            time.sleep(30)

    # Turn to CastleGate -> Inbound Orders -> Shipments Page
    Shipments_Page = 'https://partners.wayfair.com/castlegate_inbound/shipments/transit'                    
    driver.get(Shipments_Page)
    time.sleep(60)
    
    # Export Asia Consolidation Data to CSV
    for i in range(3):
        try:
            css = ' body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div.CastleGatePageContainer > div > main > div.ex-TabbedContent > div.ex-TabbedContent-content.is-active > div > div > div.margin_bottom_medium > div > div > div.BaseBox-sc-16uwbyc-0.eJpMgj > div > p > button'
            LoadingChecker = (By.CSS_SELECTOR, css)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(css).click()
            break
        except:
            driver.refresh()
            time.sleep(30)
        
    # Turn to Download Center
    download_page = 'https://partners.wayfair.com/v/supplier/download_center/management/app'
    driver.get(download_page)
    time.sleep(30)
    
    # Sorting by Created Date
    LoadingChecker = (By.CSS_SELECTOR, '.js-autogen-column:nth-child(4) .sorting')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
    driver.find_element_by_css_selector('.js-autogen-column:nth-child(4) .sorting').click()
    time.sleep(60)
            
    # Confirm Download Button is ready
    for i in range(3):
        if driver.find_element_by_css_selector('tbody .table_row .js-status').text == 'Complete':
            driver.find_elements_by_css_selector('.js-document-download')[0].click()
            time.sleep(60)
                    
            file_checker = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name]
            # Confirm Download file is ready
            if len(file_checker) != 0:
                break
            else:
                driver.refresh()
                time.sleep(30)
        else:
            print("download not complete")
            driver.refresh()
            time.sleep(60)
        
    # Set File name
    US_file_name = date_label + ' AC_Shipments_CSV_Topline.csv'#US
    CAN_file_name = date_label + ' AC_Shipments_CSV_41910.csv'#CAN    
    ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name][0]
    
    if l=="US":
        shutil.move(Download_dir + ori_file, final_Inv_dir + US_file_name)
    elif l=="CAN":
        shutil.move(Download_dir + ori_file, CAN_final_Inv_dir + CAN_file_name)

driver.quit()
