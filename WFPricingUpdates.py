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
    prefs = {'download.default_directory': 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'}
    os.chdir(work_dir)
except:
    #0047
    work_dir = 'N:\\E Commerce\\Public Share\\Automate_Script\\DLpack_Wayfair\\'
    driver_path = 'C:\\Users\\raymond.hung\\chrome\\chromedriver.exe'
    prefs = {'download.default_directory': 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Pricing Updates\\'}
    os.chdir(work_dir)

#   Account and Password
login_info = pd.read_csv(work_dir+ 'Account & Password.csv',index_col=0)
WF_Account = login_info.loc['Account', 'CONTENT']
WF_Password = login_info.loc['Password', 'CONTENT']

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
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

# Turn to pricing updates page
for i in range(9):
    try:
        price_download="https://partners.wayfair.com/v/supplier/pricing/app/index"
        driver.get(price_download)
        time.sleep(30)
        if driver.find_element_by_css_selector("body > div.wrapper > div.body.wfe_content_wrap.js-wfe-content-wrap > div > div > div > header > div.ex-PageContainer-titlebar > div > h1").text == "Pricing Updates":
            break
        else:
             driver.refresh()
             time.sleep(30)
    except:
        driver.refresh()
        time.sleep(30)

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
                    break
            break
        except:
            driver.refresh()
            if count == 10:
                print("over count")
                break
            count+=1
            time.sleep(30)
            
    # Download excel file
    for i in range(3):
        try:
    #    Click "Search" Button
            LoadingChecker = (By.CSS_SELECTOR, ".u-size1of12 .ex-Button--primary")
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(".u-size1of12 .ex-Button--primary").click()
            time.sleep(10)
            
    #    Click "Export" Button
            LoadingChecker = (By.CSS_SELECTOR, ".ex-Grid-item--row > .ex-Button--secondary")
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(LoadingChecker))
            driver.find_element_by_css_selector(".ex-Grid-item--row > .ex-Button--secondary").click()
            time.sleep(60)
            break
        except:
            driver.refresh()

# #   GO back to US
# try:
#     s1 = Select(driver.find_element_by_id('switchsupplier').find_element_by_name('switchsupplier'))
#     s1.select_by_visible_text(LOC['US'])
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
