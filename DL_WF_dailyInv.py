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
    # 0047 Directory
    work_dir = 'N:\\E Commerce\\Public Share\\Automate_Script\\DLpack_Wayfair\\'
    Download_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG daily Inventory\\temp_DL_file\\'
    final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG daily Inventory\\'
    CAN_final_Inv_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG CAN daily Inventory\\'
    driver_path = 'C:\\Users\\raymond.hung\\chrome\\chromedriver.exe'
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

LOC ={'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
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
     
    # Turn to inventory page
    for i in range(3):
        try:
            Inventory_page = 'https://partners.wayfair.com/v/wfs/products/product/index'
            driver.get(Inventory_page)
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
    
            if driver.find_element_by_css_selector("#utilitybar-title").text == "Inventory":
                break
            else:
                driver.refresh()
                time.sleep(30)
        except:
            print("Can't turn to inventory page")
    
    # Set File name
    total_name = 'inventory WH' + date_label + '.csv'
        
    # Click dropdown menus and download excel file
    for i in range(3):
        try:
            css = 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div.CastleGatePageContainer > div > main > div.ex-Grid.ex-Grid--withGutter.ex-Grid--row > div.ex-Grid-item.u-size3of12.ex-Grid-item--row > div > button'
            LoadingChecker = (By.CSS_SELECTOR, css)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(css).click()
            time.sleep(60)
            ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if '.csv' in Inv_name][0]
            break
        except:
            print("Can't download excel file")
            driver.refresh()
            time.sleep(30)
    
    if l == "US":
        shutil.move(Download_dir + ori_file, final_Inv_dir + total_name)
    elif l == "CAN":
        shutil.move(Download_dir + ori_file, CAN_final_Inv_dir + total_name)
    time.sleep(10)

driver.quit() 
