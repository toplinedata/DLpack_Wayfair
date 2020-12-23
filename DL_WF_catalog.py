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
time.sleep(30)
# Skip Wayfair system info.
try:
    iframe = driver.find_element_by_css_selector('body > div.appcues > appcues-container > iframe')
    driver.switch_to_frame(iframe)

    wfe_modal = 'body > appcues > div.appcues-skip > a'
    LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
    driver.find_element_by_css_selector(wfe_modal).click()
except:
    pass
driver.switch_to_default_content()

LOC = {'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
for l in LOC:
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
    # Click select box to choose US or CAN
    for i in range(3):
        try:
            css='body > div.wrapper > div:nth-child(1) > header > div > div > div.PH-Header > div > div.ex-Grid-item.ex-Grid-item--flex.u-flexShrink.ex-Grid-item--column.u-justifyEnd > div > div.PH-Header-information > div'
            LoadingChecker = (By.CSS_SELECTOR, css+' > span.ex-Box.ex-Block.ex-Block--display-flex.ex-Block--isFlex.ex-Block--flexWrap-wrap.ex-Block--alignItems-center.ex-Block--display-flex.ex-Box--ml-small')
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(css+' > span.ex-Box.ex-Block.ex-Block--display-flex.ex-Block--isFlex.ex-Block--flexWrap-wrap.ex-Block--alignItems-center.ex-Block--display-flex.ex-Box--ml-small').click()
            for j in range(1, 3):
                box_text = driver.find_element_by_css_selector(css+'> span.PH-HeaderDropdown-value > ul > li:nth-child('+str(j)+') > button').text
                if box_text == LOC[l]:
                    driver.find_element_by_css_selector(css+'> span.PH-HeaderDropdown-value > ul > li:nth-child('+str(j)+') > button').click()
                    time.sleep(30)
                    break
            css = "body > div.wrapper > div:nth-child(1) > header > div > div > div.PH-Header > div > div.ex-Grid-item.ex-Grid-item--flex.u-flexShrink.ex-Grid-item--column.u-justifyEnd > div > div.PH-Header-information > div > span.PH-HeaderDropdown-value"
            if driver.find_element_by_css_selector(css).text == box_text:
                break
            else:
                print("box not correct")
        except:
            print("switch LOC fail")
            driver.refresh()
            time.sleep(30)
    
    for i in range(3):
        # Turn to Catalog page
        for j in range(3):
            Catalog_Download = 'https://partners.wayfair.com//v/catalog/catalog_management/index'
            driver.get(Catalog_Download)
            time.sleep(30)
                
            # Skip Wayfair system info.
            try:
                iframe = driver.find_element_by_css_selector('body > div.appcues > appcues-container > iframe')
                driver.switch_to_frame(iframe)

                wfe_modal = 'body > appcues > div.appcues-skip > a'
                LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector(wfe_modal).click()
            except:
                pass
            driver.switch_to_default_content()

            ProductManagementDashborad = 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > header > div.BaseBox-sc-16uwbyc-0.jnYHRu > div > h1 > div > div.ex-Grid-item.ex-Grid-item--flex.ex-Grid-item--row'
            if driver.find_element_by_css_selector(ProductManagementDashborad).text == "Product Management Dashboard":
                break
            else:
                print("can't turn to catalog page")

        # Click dropdown menus and download excel file
        for j in range(3):
            try:
                LoadingChecker = (By.CSS_SELECTOR, 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > main > div > div.ex-Grid-item.u-size3of12.ex-Grid-item--row > div > div > div > div:nth-child(6) > button')
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector('body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > main > div > div.ex-Grid-item.u-size3of12.ex-Grid-item--row > div > div > div > div:nth-child(6) > button').click()
                time.sleep(5)
                break
            except:
                print("can't dropdown menus and download") 
                driver.refresh()
                time.sleep(60)
        
        # Turn to download management center page
        for j in range(3):
            download_page = 'https://partners.wayfair.com/v/supplier/download_center/management/app'
            driver.get(download_page)
            time.sleep(30)
                
            #Skip Wayfair system info.
            try:
                iframe = driver.find_element_by_css_selector('body > div.appcues > appcues-container > iframe')
                driver.switch_to_frame(iframe)
                
                wfe_modal = 'body > appcues > div.appcues-skip > a'
                LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector(wfe_modal).click()
            except:
                pass
            driver.switch_to_default_content()

            # Confrom Download Center Status
            DownloadManagementCenter = 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > div > div > div > h1'
            if driver.find_element_by_css_selector(DownloadManagementCenter).text == "Download Management Center":
                break
            else:
                print("can't turn to download management center page")
    
        # Swith Window Handle
        window_after = driver.window_handles[-1]
        driver.switch_to_window(window_after)
    
        # Sorting by Created Date and download file
        for j in range(3):
        # Sorting by Created Date
            try:
                LoadingChecker = (By.CSS_SELECTOR, '.js-autogen-column:nth-child(4) .sorting')
                WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector('.js-autogen-column:nth-child(4) .sorting').click()
                time.sleep(20)
                    
                # Confirm Download Button status
                if driver.find_element_by_css_selector('tbody .table_row .table_data_cell:nth-child(5)').text == 'Complete' and \
                driver.find_element_by_css_selector('tbody .table_row .table_data_cell:nth-child(2)').text == 'Catalog Export':
                    # Confirm Sorting Date status
                    time1 = driver.find_element_by_css_selector('tbody > tr:nth-child(1) > td:nth-child(4)').text
                    time2 = driver.find_element_by_css_selector('tbody > tr:nth-child(2) > td:nth-child(4)').text
                    if datetime(int(time1[6:10]), int(time1[0:2]), int(time1[3:5]), int(time1[11:13]), int(time1[14:16]), int(time1[17:19])) > \
                    datetime(int(time2[6:10]), int(time2[0:2]), int(time2[3:5]), int(time2[11:13]), int(time2[14:16]), int(time2[17:19])):
                        driver.find_elements_by_css_selector('.js-document-download')[0].click()
                        time.sleep(30)
                        break
                    else:
                        print("sorting by created date not ready")
                        driver.refresh()
                        time.sleep(30)
                else:
                    print("download Button not ready")
                    driver.refresh()
                    time.sleep(60)
            except:
                print("can't sorting by created date")
                driver.refresh()
                time.sleep(30)
    
            #Skip Wayfair system info.
            try:
                iframe = driver.find_element_by_css_selector('body > div.appcues > appcues-container > iframe')
                driver.switch_to_frame(iframe)
                
                wfe_modal = 'body > appcues > div.appcues-skip > a'
                LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector(wfe_modal).click()
            except:
                pass
            driver.switch_to_default_content()
    
        # Check download action
        try:
            ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name][0]
            if l == "US" and "Catalog_Export_Topline" in ori_file:
                break
            elif l == "CAN" and "Catalog_Export_41910" in ori_file:
                break
            else:
                os.remove(Download_dir+ori_file)
                print("file not correct")
                driver.refresh()
                time.sleep(30)
        except:
            print("file download fail")
            driver.refresh()
            time.sleep(30)
                           
        #Skip Wayfair system info.
        try:
            iframe = driver.find_element_by_css_selector('body > div.appcues > appcues-container > iframe')
            driver.switch_to_frame(iframe)
            
            wfe_modal = 'body > appcues > div.appcues-skip > a'
            LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(wfe_modal).click()
        except:
            pass
        driver.switch_to_default_content()
                
    # Set File name
    US_total_name = date_label + ' 15379_full_catalog_export.csv'#US
    CAN_total_name = date_label + ' 41910_full_catalog_export.csv'#CAN    
        
    if l == "US":
        shutil.move(Download_dir + ori_file, final_Inv_dir + US_total_name)
        print("US catalog export file is ready")
    elif l == "CAN":
        shutil.move(Download_dir + ori_file, CAN_final_Inv_dir + CAN_total_name)
        print("CAN catalog export file is ready")

driver.quit()
