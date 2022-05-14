#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 13:18:16 2022

@author: bradenlimb
"""
#%% Import Modules
from IPython import get_ipython
get_ipython().run_line_magic('reset','-sf')

# import pandas as pd
# import sys
import datetime
begin_time = datetime.datetime.now()
import shutil
import os
from tqdm import tqdm

import pytz
from win32com.propsys import propsys, pscon

#%% Base Location

source_root = r'C:\Users\Braden Limb\Downloads\iCloud Photos (3)\iCloud Photos'
target_root = r'E:\Video Diaries'



rename_existing_files = False
if rename_existing_files:
    filenames = [ item for item in os.listdir(target_root) if os.path.isfile(os.path.join(target_root, item)) ]
    filenames = [ x for x in filenames if "._" not in x ]
    filenames = [ x for x in filenames if "IMG_" in x ]
    #filenames  = [filenames[1]]
    for filename in tqdm(filenames):
        
        filepath = f'{target_root}\{filename}'
        properties = propsys.SHGetPropertyStoreFromParsingName(filepath)
        dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        
        if not isinstance(dt, datetime.datetime):
            # In Python 2, PyWin32 returns a custom time type instead of
            # using a datetime subclass. It has a Format method for strftime
            # style formatting, but let's just convert it to datetime:
            dt = datetime.datetime.fromtimestamp(int(dt))
            dt = dt.replace(tzinfo=pytz.timezone('UTC'))
        dt_local = dt.astimezone(pytz.timezone('America/Denver'))
        
        dt_local_str = dt_local.strftime('%Y-%m-%d')
        new_filename = f'{dt_local_str} Video Diary{filename[-4:]}'
        target_file = f'{target_root}\{new_filename}'
        shutil.copyfile(filepath, target_file)

move_files = True
if move_files:
    filenames = [ item for item in os.listdir(source_root) if os.path.isfile(os.path.join(source_root, item)) ]
    filenames = [ x for x in filenames if "._" not in x ]
    filenames = [ x for x in filenames if "IMG_" in x ]
    # filenames  = [filenames[1]]
    for filename in tqdm(filenames):
        
        filepath = f'{source_root}\{filename}'
        properties = propsys.SHGetPropertyStoreFromParsingName(filepath)
        dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        
        if not isinstance(dt, datetime.datetime):
            # In Python 2, PyWin32 returns a custom time type instead of
            # using a datetime subclass. It has a Format method for strftime
            # style formatting, but let's just convert it to datetime:
            dt = datetime.datetime.fromtimestamp(int(dt))
            dt = dt.replace(tzinfo=pytz.timezone('UTC'))
        dt_local = dt.astimezone(pytz.timezone('America/Denver'))
        
        dt_local_str = dt_local.strftime('%Y-%m-%d')
        new_filename = f'{dt_local_str} Video Diary{filename[-4:]}'
        target_file = f'{target_root}\{new_filename}'
        shutil.copyfile(filepath, target_file)

#%% End of Code
execute_time = datetime.datetime.now() - begin_time
print('')
print('Code execution time: ', execute_time)
