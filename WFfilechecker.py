# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:12:25 2019

@author: User
"""
import os
import time

# local
try:
    #set up download script folder path
    script_dir = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    os.chdir(script_dir)
    
    #Folder of WF daily download script
    # DL_WF_catalog.py
    final_Inv_dir_catalog = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    CAN_final_Inv_dir_catalog = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    # DL_WF_dailyInv.py
    final_Inv_dir_dailyInv = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\CG daily Inventory\\'
    CAN_final_Inv_dir_dailyInv = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\CG CAN daily Inventory\\'
    # DL_WF_inboundPO.py
    final_Inv_dir_inboundPO = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    CAN_final_Inv_dir_inboundPO = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    # DL_WF_pricingupdate.py
    final_Inv_dir_pricingupdate = 'C:\\Users\\User\\Desktop\\0047Automate_Script\\DLpack_Wayfair\\'
    
# 0047
except:    
    #set up download script folder path
    script_dir = 'C:\\Users\\raymond.hung\\Documents\\Automate_Script\\DLpack_Wayfair\\'
    os.chdir(script_dir)
    
    #Folder of WF daily download script
    # DL_WF_catalog.py
    final_Inv_dir_catalog = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Catalog\\WF Catalog\\'
    CAN_final_Inv_dir_catalog = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Catalog\\WF CAN Catalog\\'
    # DL_WF_dailyInv.py
    final_Inv_dir_dailyInv = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG daily Inventory\\'
    CAN_final_Inv_dir_dailyInv = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG CAN daily Inventory\\'
    # DL_WF_inboundPO.py
    final_Inv_dir_inboundPO = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG Inbound PO\\'
    CAN_final_Inv_dir_inboundPO = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\CG CAN Inbound PO\\'
    # DL_WF_pricingupdate.py
    final_Inv_dir_pricingupdate = 'N:\\E Commerce\\Public Share\\Dot Com - Wayfair\\WF Pricing Updates\\'
    
### Check download file for WF daily download script
while 1==1:
    # DL_WF_catalog.py
    date_label1 = time.strftime('%Y.%m.%d')
    for i in range(3):
        count = 0
        file_list=list(os.listdir(final_Inv_dir_catalog)+os.listdir(CAN_final_Inv_dir_catalog))
        for file in file_list:
            if date_label1+' 15379_full_catalog_export' in file:
                count+=1
                print(count, file)
            elif date_label1+' 41910_full_catalog_export' in file:
                count+=1
                print(count, file)
        if count < 2:
            os.system("python "+script_dir+"DL_WF_catalog.py")
        else:
            break
        
    # DL_WF_dailyInv.py
    date_label2 = time.strftime('%Y%m%d')
    for i in range(3):
        count = 2
        file_list=list(os.listdir(final_Inv_dir_dailyInv)+os.listdir(CAN_final_Inv_dir_dailyInv))
        for file in file_list:
            if 'inventory WH'+date_label2 in file:
                count+=1
                print(count, file)
        if count < 4:
            os.system("python "+script_dir+"DL_WF_dailyInv.py")
        else:
            break

    # DL_WF_inboundPO.py
    for i in range(3):
        count = 4
        file_list=list(os.listdir(final_Inv_dir_inboundPO)+os.listdir(CAN_final_Inv_dir_inboundPO))
        for file in file_list:
            if 'inbound_order' + date_label2 in file:
                count+=1
                print(count, file)
        if count < 6:
            os.system("python "+script_dir+"DL_WF_inboundPO.py")
        else:
            break
    
    # WFPricingUpdates.py
    date_label3 = time.strftime('%Y_%m_%d')
    for i in range(3):
        count = 6
        file_list=list(set(os.listdir(final_Inv_dir_pricingupdate)))
        for file in file_list:
            if  'Topline Furniture Warehouse Corp._'+date_label3 in file:
                count+=1
                print(count, file)
        if count < 8:
            for file in file_list:
                if  'Topline Furniture Warehouse Corp._'+date_label3 in file:
                    os.remove(final_Inv_dir_pricingupdate+file)
            os.system("python "+script_dir+"WFPricingUpdates.py")
        else:
            print("Done.")
            break
    if count >= 8:
        break