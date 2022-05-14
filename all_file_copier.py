# -*- coding: utf-8 -*-
"""
Created on Sun May  1 14:13:39 2022

@author: Braden Limb
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

def make_dir(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    
from PIL import Image
def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

import exifread
def exif_read(directoryInput,filename):
        with open("%s/%s" % (directoryInput, filename), 'rb') as image: # file path and name
            exif = exifread.process_file(image)
            dt = str(exif['EXIF DateTimeOriginal'])  # might be different
            return dt


#%% Base Location

camera = 'R6'
# camera = 'iPhone 11'

source_root = r'C:\Users\Braden Limb\Downloads\iCloud Photos (1)\iCloud Photos'
target_root = r'F:\Pictures'

source_root = r'E:\DCIM\100CANON'
target_root = r'F:\Pictures'

# source_root = r'C:\Users\Braden Limb\Downloads\iCloud Photos (1)\iCloud Photos'

not_copied = []
move_files = True
if move_files:
    filenames = [ item for item in os.listdir(source_root) if os.path.isfile(os.path.join(source_root, item)) ]
    filenames = [ x for x in filenames if "._" not in x ]
    # filenames = [ x for x in filenames if "IMG_" in x ]
    # filenames  = ['IMG_3625.JPG']
    # filename = 'IMG_9514.HEIC'
    for filename in tqdm(filenames):
        
        filepath = f'{source_root}\{filename}'
        
        try:
            dt = get_date_taken(filepath)
        except:
            try:
                dt = exif_read(source_root,filename)
            except:
                try:
                    properties = propsys.SHGetPropertyStoreFromParsingName(filepath)
                    dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
                except:
                    try:
                       dt = os.path.getctime(filepath) 
                    except: 
                        not_copied.append(filename)
                        continue
        
        if not isinstance(dt, datetime.datetime):
            
            if dt == None:
                not_copied.append(filename)
                continue
            
            # In Python 2, PyWin32 returns a custom time type instead of
            # using a datetime subclass. It has a Format method for strftime
            # style formatting, but let's just convert it to datetime:
                
            try:
                dt = datetime.datetime.strptime(dt, '%Y:%m:%d %H:%M:%S')
            except:
                dt = datetime.datetime.fromtimestamp(int(dt))
            dt = dt.replace(tzinfo=pytz.timezone('UTC'))
        dt_local = dt.astimezone(pytz.timezone('America/Denver'))
        
        target_path = f'{target_root}\{dt_local.strftime("%Y")}'
        make_dir(target_path)
        target_path = f'{target_path}\{dt_local.strftime("%m")} {dt_local.strftime("%B")}'
        make_dir(target_path)
        target_path = f'{target_path}\{camera}'
        make_dir(target_path)
        if camera == 'R6':
            target_path = f'{target_path}\{dt_local.strftime("%Y-%m-%d")}'
            make_dir(target_path)
            if filename[-4:] == '.JPG':
                target_path = f'{target_path}\JPEG'
                make_dir(target_path)
            elif filename[-4:] == '.CR3':
                target_path = f'{target_path}\RAW'
                make_dir(target_path)
            elif filename[-4:] == '.MP4':
                target_path = f'{target_path}\Videos'
                make_dir(target_path)

        target_file = f'{target_path}\{filename}'
        shutil.copyfile(filepath, target_file)


#%% End of Code
execute_time = datetime.datetime.now() - begin_time
print('')
print('Code execution time: ', execute_time)
