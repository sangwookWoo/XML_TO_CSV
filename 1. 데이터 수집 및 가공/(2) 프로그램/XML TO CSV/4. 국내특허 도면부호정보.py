########################## import ###########################################

import xml.etree.ElementTree as ET
from collections import defaultdict
import pandas as pd
import numpy as np
from urllib import response
import warnings
from logging.config import dictConfig
import logging
import inspect
import traceback
import datetime
import time
import sys
import os
import re
#import settings as st
import zipfile
import tarfile
from tqdm import tqdm
#import xmltodict
import json
import pandas as pd
import xml.etree.ElementTree as ET
from pprint import pprint

########################## function #########################################################

def log(msg):
    
    logging.info(msg)
    
def read_filelist(path):
    try:
        log('#### Read path {}'.format(path))
        file_list = list([])
        
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                try:
                    file_list.append(os.path.abspath(os.path.join(dirpath, f)))
                except:
                    log('######## Read file error : {}'.format(filenames))
                    log('############ {}'.format(traceback.format_exc()))
                
        return file_list
    except:
          
        log('#### Read file list error')
        log('######## {}'.format(traceback.format_exc()))
        
        
def return_dict(path):
    xml_file = open(path, 'r', encoding='UTF8')
    xml_file = xml_file.read()

    dictionary = xmltodict.parse(xml_file)
    json_object = json.dumps(dictionary) 
    dict2_type = json.loads(json_object)
    return dict2_type

# xml 들어가서 키 값 종류 찾기                         
def parsing_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root

########################## make data ############################################################

path = '/data2/3_kipris/seperate/78_국내특허 도면부호정보(전문)/'

# 데이터프레임 정의
base_dict = defaultdict(list)
object_dict = defaultdict(list)
file_list = read_filelist(path)
file_list_py = [file for file in file_list if file.endswith('xml')]


for idx, xml_data_path in enumerate(file_list_py):
    log('######## ({}) Convert {}'.format(idx, xml_data_path))
    dict_of_xml = return_dict(xml_data_path)
    base = dict_of_xml['annotation']

    try :
        base_dict['filename'].append(base['filename'])
    except Exception :
        base_dict['filename'].append('')

    try :
        base_dict['folder'].append(base['folder'])
    except Exception :
        base_dict['folder'].append('')
    
    try :
        base_dict['path'].append(base['path'])
    except Exception :
        base_dict['path'].append('')
    
    try :
        base_dict['segmented'].append(base['segmented'])
    except Exception :
        base_dict['segmented'].append('')
    
    try :
        base_dict['depth'].append(base['size']['depth'])
    except Exception :
        base_dict['depth'].append('')
    try :
        base_dict['height'].append(base['size']['height'])
    except Exception :
        base_dict['height'].append('')
    try :
        base_dict['width'].append(base['size']['width'])
    except Exception :
        base_dict['width'].append('')
    try :
        base_dict['database'].append(base['source']['database'])
    except Exception :
        base_dict['database'].append('')
        
    log('############ Common Success ###############')
    

    if type(base['object']) == dict:
        try :
            object_dict['folder'].append(base['folder'])
        except Exception :
            object_dict['folder'].append('')
        try :
            object_dict['xmax'].append(base['object']['bndbox']['xmax'])
        except Exception :
            object_dict['xmax'].append('')
        try :
            object_dict['xmin'].append(base['object']['bndbox']['xmin'])
        except Exception :
            object_dict['xmin'].append('')
        try :
            object_dict['ymax'].append(base['object']['bndbox']['ymax'])
        except Exception :
            object_dict['ymax'].append('')
        try :
            object_dict['ymin'].append(base['object']['bndbox']['ymin'])
        except Exception :
            object_dict['ymin'].append('')
        try :
            object_dict['difficult'].append(base['object']['difficult'])
        except Exception :
            object_dict['difficult'].append('')
        try :
            object_dict['name'].append(base['object']['name'])
        except Exception :
            object_dict['name'].append('')
        try :
            object_dict['pose'].append(base['object']['pose'])
        except Exception :
            object_dict['pose'].append('')
        try :
            object_dict['truncated'].append(base['object']['truncated'])
        except Exception :
            object_dict['truncated'].append('')

    elif type(base['object']) == list:
        count = 0
        while count < len(base['object']) :
            try :
                object_dict['folder'].append(base['folder'])
            except Exception :
                object_dict['folder'].append('')
            try :
                object_dict['xmax'].append(base['object'][count]['bndbox']['xmax'])
            except Exception :
                object_dict['xmax'].append('')
            try :
                object_dict['xmin'].append(base['object'][count]['bndbox']['xmin'])
            except Exception :
                object_dict['xmin'].append('')
            try :
                object_dict['ymax'].append(base['object'][count]['bndbox']['ymax'])
            except Exception :
                object_dict['ymax'].append('')
            try :
                object_dict['ymin'].append(base['object'][count]['bndbox']['ymin'])
            except Exception :
                object_dict['ymin'].append('')
            try :
                object_dict['difficult'].append(base['object'][count]['difficult'])
            except Exception :
                object_dict['difficult'].append('')
            try :
                object_dict['name'].append(base['object'][count]['name'])
            except Exception :
                object_dict['name'].append('')
            try :
                object_dict['pose'].append(base['object'][count]['pose'])
            except Exception :
                object_dict['pose'].append('')
            try :
                object_dict['truncated'].append(base['object'][count]['truncated'])
            except Exception :
                object_dict['truncated'].append('')
            count += 1

    log('############ Object Success ###############')

import os
path = '/data3/3_kipris/csv/78_국내특허 도면부호정보/'
os.makedirs(path, exist_ok=True)

base_df = pd.DataFrame(base_dict)
base_df.to_csv('/data3/3_kipris/csv/78_국내특허 도면부호정보/BASE.csv',index = False)

object_df = pd.DataFrame(object_dict)
object_df.to_csv('/data3/3_kipris/csv/78_국내특허 도면부호정보/OBJECT.csv', index = False)
