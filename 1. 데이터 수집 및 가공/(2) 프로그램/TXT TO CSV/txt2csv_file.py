#!/usr/bin/python
# -*- coding : utf-8 -*-
'''
 @author : yjjo
'''
''' install '''

''' import '''
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
import pandas as pd
import numpy as np
import settings as st
from tqdm import tqdm
import csv
import multiprocessing as mp
from multiprocessing import Pool

''' log '''
warnings.filterwarnings(action = 'ignore') 
filePath = os.path.dirname(os.path.abspath(__file__))
fileName = re.split('[.]', inspect.getfile(inspect.currentframe()))[0]

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s --- %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '{}/logs/{}_{}.log'.format(filePath, fileName, re.sub('-', '', str(datetime.date.today()))),
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

def log(msg):
    logging.info(msg)

''' main '''
def main():    
    # 필드 문자 제한 설정
    csv_field_limit = 10 ** 8
    csv.field_size_limit(csv_field_limit)
    log('#### Set CSV Field Size Limit : {}'.format(csv_field_limit))
    
    # 멀티프로세싱 cpu 개수 설정
    cpu_count = 32
    pool = Pool(cpu_count)
    log('#### CPU Count : {}'.format(cpu_count))
    
    # Chunksize 설정
    chunksize = 10 ** 4
    log('#### Chunksize : {}'.format(chunksize))
    
    full_path = sys.argv[1]
    # full_path = "/data3/3_kipris/seperate/09_상표 공보(서지)/20220305/20220305/KT_DELETE.txt"
    # Read Text File & Save as CSV
    try:
        log('######## Read : \"{}\"'.format(full_path))
        with open(full_path, "r") as file:
            first_line = file.readline()
        
        save_path = re.sub('.txt', '.csv', full_path)
        save_path = re.sub('.TXT', '.csv', save_path)
        
        if len(re.split('¶', first_line)) > 1:
            chunks = pd.read_table(full_path, sep = '\¶', chunksize = chunksize, on_bad_lines = 'skip')
            log('######## Convert \"{}\" to \"{}\" Seperator : ¶'.format(full_path, save_path))
        elif len(re.split('\^B', first_line)) > 1:
            chunks = pd.read_table(full_path, sep = '\^B', chunksize = chunksize, on_bad_lines = 'skip')
            log('######## Convert \"{} to \"{} Seperator : ^B'.format(full_path, save_path))
        elif len(re.split('\\n', first_line)) > 1:
            chunks = pd.read_table(full_path, sep = '\\n', on_bad_lines = 'skip')
            log('######## Convert \"{} to \"{} No Seperator'.format(full_path, save_path))
        else:
            log('######## Cannot Convert \"{} to \"{}'.format(full_path, save_path))          
            
        for jdx, chunk in enumerate(chunks):
            log('######## \"{}\" Chunk Count : {}'.format(save_path, jdx))
            chunk = chunk.drop([x for x in list(chunk.columns) if 'Unnamed' in x], axis = 1)
            if jdx == 0:
                pool.map(chunk.to_csv(save_path, index = False, encoding = 'UTF-8-SIG'), '')
            else:
                pool.map(chunk.to_csv(save_path, index = False, encoding = 'UTF-8-SIG', mode = 'a', header = False), '')
    except:
        log('######## ({}) Convert \"{}\" to \"{}\" Error'.format(full_path))
        log('######## {}'.format(traceback.format_exc()))
    
''' funtions '''
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

def create_dir(path):
    try:
        log('#### Create Directory')
        if not os.path.exists(path):
            os.makedirs(path)
    except:
        log('######## Create Directory Error {}'.format(path))
        log(traceback.format_exc())

''' main '''
if __name__ == '__main__':
    # 시간 계산
    startTime = time.time()

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    main()

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    log('#### ===================== Time =====================')
    log('#### {:.3f} seconds'.format(time.time() - startTime))
    log('#### ================================================')
