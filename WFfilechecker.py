# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:12:25 2019

@author: User
"""
import os
import time

# Today's date_label for WF daily download script
date_label1 = time.strftime('%Y.%m.%d')
date_label2 = time.strftime('%Y%m%d')
date_label3 = time.strftime('%Y_%m_%d')

try:    #local
    #set up download script folder path
    script_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    
    #Folder of WF daily download script
    #   DL_WF_catalog.py
    final_Inv_dir_catalog = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    CAN_final_Inv_dir_catalog = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    #   DL_WF_dailyInv.py
    final_Inv_dir_dailyInv = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\CG daily Inventory\\'
    CAN_final_Inv_dir_dailyInv = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\CG CAN daily Inventory\\'
    #   DL_WF_pricingupdate.py
    final_Inv_dir_pricingupdate = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    os.chdir(script_dir)
except:    #0047
    #set up download script folder path
    script_dir = 'C:\\Users\\raymond.hung\\Documents\\Automate_Script\\DLpack_Wayfair\\'
    
    #Folder of WF daily download script
    #   DL_WF_catalog.py
    final_Inv_dir_catalog = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Catalog\\WF Catalog\\'
    CAN_final_Inv_dir_catalog = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Catalog\\WF CAN Catalog\\'
    #   DL_WF_dailyInv.py
    final_Inv_dir_dailyInv = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG daily Inventory\\'
    CAN_final_Inv_dir_dailyInv = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG CAN daily Inventory\\'
    #   DL_WF_pricingupdate.py
    final_Inv_dir_pricingupdate = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Pricing Updates\\'
    os.chdir(script_dir)
    
# Check today's download file for WF daily download script
for i in range(3):
    count = 0
    file_list1=list(os.listdir(final_Inv_dir_catalog)+os.listdir(CAN_final_Inv_dir_catalog)   \
                    +os.listdir(final_Inv_dir_dailyInv)+os.listdir(CAN_final_Inv_dir_dailyInv))
    for file in file_list1:
        if date_label1+' 15379_full_catalog_export' in file:
            count+=1
            print(count, file)
        elif date_label1+' 41910_full_catalog_export' in file:
            count+=1
            print(count, file)
        elif 'inventory WH'+date_label2 in file:
            count+=1
            print(count, file)
    if count < 4:
        os.system("python "+script_dir+"DL_WF_catalog.py")
        os.system("python "+script_dir+"DL_WF_dailyInv.py")
    else:
        break


for i in range(3):
    file_list2=list(set(os.listdir(final_Inv_dir_pricingupdate)))
    for file in file_list2:
        if  'Topline Furniture Warehouse Corp._'+date_label3 in file:
            count+=1
            print(count, file)
    if count != 6:
        for file in file_list2:
            if  'Topline Furniture Warehouse Corp._'+date_label3 in file:
                os.remove(final_Inv_dir_pricingupdate+file)
        os.system("python "+script_dir+"WFPricingUpdates.py")
    else:
        print("Done.")
        break
