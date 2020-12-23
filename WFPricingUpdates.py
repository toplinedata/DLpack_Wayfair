from selenium import webdriver
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

print(datetime.today().strftime("%Y%m%d"))

try:
    #local
    work_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    driver_path = 'C:\\Users\\User\\anaconda3\\chrome\\chromedriver.exe'
    Download_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    os.chdir(work_dir)
except:
    #0047
    work_dir = 'N:\\E Commerce\\Public Share\\Automate_Script\\DLpack_Wayfair\\'
    driver_path = 'C:\\Users\\raymond.hung\\chrome\\chromedriver.exe'
    Download_dir = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Pricing Updates\\'
    os.chdir(work_dir)

#   Account and Password
login_info = pd.read_csv(work_dir+ 'Account & Password.csv',index_col=0)
WF_Account = login_info.loc['Account', 'CONTENT']
WF_Password = login_info.loc['Password', 'CONTENT']

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
prefs = {'profile.default_content_settings.popups': '0', 'download.default_directory' : Download_dir}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(driver_path, chrome_options= options)

#   Wayfair extrant website
WF_Extrant = 'https://partners.wayfair.com'
driver.get(WF_Extrant)
#time.sleep(10)

#   Input Account, Password and login
LoadingChecker = (By.ID, 'js-username')
WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
insert_act = driver.find_element_by_id('js-username').send_keys(WF_Account)
insert_pwd = driver.find_element_by_id('password_field').send_keys(WF_Password)
driver.find_element_by_xpath('//*[@id="login"]/button').click()

# skip Wayfair system info.
try:
    wfe_modal = 'body > div.wfe_modal.modal_transition_bottom.modal_transition_finish > div > span'
    LoadingChecker = (By.CSS_SELECTOR, wfe_modal)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
    driver.find_element_by_css_selector(wfe_modal).click()
    time.sleep(5)
except:
    pass
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

# Turn to pricing updates page
for i in range(3):
    price_download="https://partners.wayfair.com/v/supplier/pricing/app/index"
    driver.get(price_download)
    time.sleep(30)
    if driver.find_element_by_css_selector("body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > header > div.BaseBox-sc-16uwbyc-0.jnYHRu > div > h1").text == "Pricing Updates":
        break
    else:
        driver.refresh()
        time.sleep(30)

LOC = {'US':'Topline Furniture Warehouse Corp.', 'CAN':'CAN_Topline Furniture Warehouse Corp.'}
for l in LOC:
    # Click select box to choose US or CAN
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
    for i in range(3):
        try:
            css='body > div.wrapper > div:nth-child(1) > header > div > div > div.PH-Header > div > div.ex-Grid-item.ex-Grid-item--flex.u-flexShrink.ex-Grid-item--column.u-justifyEnd > div > div.PH-Header-information > div > span.PH-HeaderDropdown-value'
            LoadingChecker = (By.CSS_SELECTOR, css)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(css).click()
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
            driver.refresh()
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
            time.sleep(30)
            
    # Download excel file
    for i in range(3):
        #    Select Price Change Reason
        for j in range(3):
            try:
                reason = 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > main > div.ex-Box.ex-Block.ex-Box--mb-large.ex-Box--mt-small > div.ex-Box.ex-Block.ex-Box--mb-medium > div > div.ex-Grid-item.u-size4of12.ex-Grid-item--row > div > div > div.BaseBox-sc-16uwbyc-0.iNvhAH > div.BaseBox-sc-16uwbyc-0.DropdownInput__InputContainer-i6blfk-3.bZDQuc'
                LoadingChecker = (By.CSS_SELECTOR, reason)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector(reason).click()
                time.sleep(5)
                break
            except:
                driver.refresh()
                print("can't select Price Change Reason")
                time.sleep(30)
        
        #   Choose View Only
        for j in range(3):
            try:
                view_only = '#downshift-1-item-0'
                LoadingChecker = (By.CSS_SELECTOR, view_only)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector(view_only).click()
                time.sleep(5)
                break
            except:
                driver.refresh()
                print("can't select View Only")
                time.sleep(30)

        #    Click "Search" Button
        for j in range(3):
            try:
                search = 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > main > div.ex-Box.ex-Block.ex-Box--mb-large.ex-Box--mt-small > div:nth-child(2) > div.ex-Grid-item.u-size1of12.ex-Grid-item--row > span > button'        
                LoadingChecker = (By.CSS_SELECTOR, search)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector(search).click()
                time.sleep(15)
                break
            except:
                driver.refresh()
                print("can't Search")
                time.sleep(30)
    
        #    Click "Export" Button
        for j in range(3):
            try:
                export = 'body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > main > div.ex-Box.ex-Block.ex-Box--mb-large.ex-Box--mt-small > div:nth-child(4) > div > div > div:nth-child(1) > button'
                LoadingChecker = (By.CSS_SELECTOR, export)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
                driver.find_element_by_css_selector(export).click()
                time.sleep(60)
                break
            except:
                driver.refresh()
                print("can't Export")
                time.sleep(30)
                
        #   Check download file
        sqld = datetime.today().strftime("_%Y_%m_%d")
        ori_file = [Inv_name for Inv_name in os.listdir(Download_dir) if 'Topline Furniture Warehouse Corp.'+sqld in Inv_name]
        if l == "US" and len(ori_file) == 1:
            break
        elif l == "CAN" and len(ori_file) == 2:
            break
        else:
            driver.refresh()
            print("download fail")
            time.sleep(30)

driver.quit() 
