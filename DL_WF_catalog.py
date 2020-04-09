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
    Download_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Catalog\\temp_DL_file\\'
    final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Catalog\\WF Catalog\\'
    CAN_final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Catalog\\WF CAN Catalog\\'
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

# skip Wayfair system info.
try:
    wfe_modal = 'body > div.wfe_modal.modal_transition_bottom.modal_transition_finish > div > span'
    LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
    driver.find_element_by_css_selector(wfe_modal).click()
except:
    pass

LOC = {'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
for l in LOC:
    # Turn to Catalog page & Download My Catalog
    Catalog_Download = 'https://partners.wayfair.com//v/catalog/catalog_management/index'
    driver.get(Catalog_Download)
    time.sleep(30)

    # Click select box to choose US or CAN
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
    css='body > div.wrapper > div:nth-child(1) > header > div > div > div.PH-Header > div > div.ex-Grid-item.ex-Grid-item--flex.u-flexShrink.ex-Grid-item--column.u-justifyEnd > div > div.PH-Header-information > div > span'
    LoadingChecker = (By.CSS_SELECTOR, css)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
    driver.find_element_by_css_selector(css).click()
    for i in range(1,3):
        if driver.find_element_by_css_selector(css+'> ul > li:nth-child('+str(i)+') > button').text == LOC[l]:
            driver.find_element_by_css_selector(css+'> ul > li:nth-child('+str(i)+') > button').click()
            break
    
    # Set File name
    US_total_name = date_label + ' 15379_full_catalog_export.csv'#US
    CAN_total_name = date_label + ' 41910_full_catalog_export.csv'#CAN    
    time.sleep(30)
    
    # Click dropdown menus and download excel file
    for i in range(5):
        try:
            LoadingChecker = (By.CSS_SELECTOR, 'button.ex-Button.ex-Button--text')
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector('button.ex-Button.ex-Button--text').click()
            time.sleep(5)
            break
        except:
            driver.refresh()
            time.sleep(60)
        
    # Goto Download Center    
    download_page = 'https://partners.wayfair.com/v/supplier/download_center/management/app'
    driver.get(download_page)
    time.sleep(10)
    # Swith Window Handle
    window_after = driver.window_handles[-1]
    driver.switch_to_window(window_after)

    for i in range(3):
        for j in range(5):
            try:
                # Sorting by Created Date
                LoadingChecker = (By.CSS_SELECTOR, '.js-autogen-column:nth-child(4) .sorting')
                WebDriverWait(driver, 120).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector('.js-autogen-column:nth-child(4) .sorting').click()
                break
            except:
                driver.refresh()

        time.sleep(30)
        # Confirm Download Button is ready
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
            driver.refresh()
            time.sleep(30)
    
    ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name][0]
    if l=="US":
        shutil.move(Download_dir + ori_file, final_Inv_dir + US_total_name)
    elif l=="CAN":
        shutil.move(Download_dir + ori_file, CAN_final_Inv_dir + CAN_total_name)

#GO back to US
# try:
#     s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
#     s1.select_by_visible_text(LOC['US'])
#     LoadingChecker = (By.ID, 'switchsupplier')
#     WebDriverWait(driver, 120).until(EC.presence_of_element_located(LoadingChecker))
#     driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
#     time.sleep(20)
# except:
#     driver.refresh()
#     time.sleep(60)
#     s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
#     s1.select_by_visible_text(LOC['US'])
#     LoadingChecker = (By.ID, 'switchsupplier')
#     WebDriverWait(driver, 120).until(EC.presence_of_element_located(LoadingChecker))
#     driver.find_element_by_id('switchsupplier').find_element_by_name('changeSupplier').click()
#     time.sleep(20)

driver.quit()
