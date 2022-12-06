############################## import #################################################
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
import xmltodict
import json
import pandas as pd
import xml.etree.ElementTree as ET
from pprint import pprint


############################# function #####################################################

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

########################################### make data ############################################################
path = '/data3/3_kipris/seperate/47_이의신청서지(전문)/'

file_list = read_filelist(path)
file_list_py = [file for file in file_list if file.endswith('xml')]

# 데이터프레임 정의
base_dict = defaultdict(list)
Publication_dict = defaultdict(list)
Staff_dict = defaultdict(list)
Plantiff_dict = defaultdict(list)
for idx ,xml_data_path in enumerate(file_list_py):
    log('######## ({}) Convert {}'.format(idx, xml_data_path))
    if 'trademark' in xml_data_path or 'Trademark' in xml_data_path or 'TM' in xml_data_path:
        # xml에 대한 딕셔너리 반환
        dict_of_xml = return_dict(xml_data_path)
        base = dict_of_xml['krtmk:TrademarkOppositionBibliography']
        
        
        ################# 공용정보 만들기 ################################
        
        # id #
        try :
            base_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
        except Exception:
            base_dict['id'].append('')

        # languageCode #
        try :
            base_dict['languageCode'].append(base['krcom:DocumentCreation']['@com:languageCode'])
        except Exception:
            base_dict['languageCode'].append('')

        # DocumentDate #
        try :
            base_dict['DocumentDate'].append(base['krcom:DocumentCreation']['com:DocumentDate'])
        except Exception:
            base_dict['DocumentDate'].append('')
        
        # DocumentName #
        try :
            base_dict['DocumentName'].append(base['krcom:DocumentCreation']['com:DocumentName'])
        except Exception:
            base_dict['DocumentName'].append('')

        # DocumentOffice #
        try :
            base_dict['DocumentOffice'].append(base['krcom:DocumentCreation']['krcom:DocumentOffice'])
        except Exception:
            base_dict['DocumentOffice'].append('')

        # operationCategory #
        try :
            base_dict['operationCategory'].append(base['krtmk:OppositionBibliographicData']['@com:operationCategory'])
        except Exception:
            base_dict['operationCategory'].append('')

        # OppositionDate #
        try :
            base_dict['OppositionDate'].append(base['krtmk:OppositionBibliographicData']['krcom:OppositionIdentification']['com:OppositionDate'])
        except Exception:
            base_dict['OppositionDate'].append('')

        # OppositionIdentifier #
        try :
            base_dict['OppositionIdentifier'].append(base['krtmk:OppositionBibliographicData']['krcom:OppositionIdentification']['com:OppositionIdentifier'])
        except Exception:
            base_dict['OppositionIdentifier'].append('')
        
        # EventNumberText #
        try :
            base_dict['EventNumberText'].append(base['krtmk:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:EventNumberText'])
        except Exception:
            base_dict['EventNumberText'].append('')
        
        # RightKindText #
        try :
            base_dict['RightKindText'].append(base['krtmk:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:RightKindText']['#text'])
        except Exception:
            base_dict['RightKindText'].append('')
        
        # RightKindText_languageCode #
        try :
            base_dict['RightKindText_languageCode'].append(base['krtmk:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:RightKindText']['@com:languageCode'])
        except Exception:
            base_dict['RightKindText_languageCode'].append('')

        # ApplicationNumberText #
        try :
            base_dict['ApplicationNumberText'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['com:ApplicationNumber']['com:ApplicationNumberText'])
        except Exception:
            base_dict['ApplicationNumberText'].append('')

        # IPOfficeCode #
        try :
            base_dict['IPOfficeCode'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['com:ApplicationNumber']['com:IPOfficeCode'])
        except Exception:
            base_dict['IPOfficeCode'].append('')

        # ApplicationDate #
        try :
            base_dict['ApplicationDate'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['tmk:ApplicationDate'])
        except Exception:
            base_dict['ApplicationDate'].append('')

        # MarkSignificantVerbalElementText #
        try :
            base_dict['MarkSignificantVerbalElementText'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['tmk:MarkSignificantVerbalElementText']['#text'])
        except Exception:
            base_dict['MarkSignificantVerbalElementText'].append('')

        # MarkSignificantVerbalElementText_languageCode #
        try :
            base_dict['MarkSignificantVerbalElementText_languageCode'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['tmk:MarkSignificantVerbalElementText']['@com:languageCode'])
        except Exception:
            base_dict['MarkSignificantVerbalElementText_languageCode'].append('')

        # DecisionDate #
        try :
            base_dict['DecisionDate'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:Decision']['krcom:DecisionDate'])
        except Exception:
            base_dict['DecisionDate'].append('')

        # DecisionText #
        try :
            base_dict['DecisionText'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:Decision']['krcom:DecisionText'])
        except Exception:
            base_dict['DecisionText'].append('')

        # OppositionCurrentStatusText #
        try :
            base_dict['OppositionCurrentStatusText'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:OppositionCurrentStatusText'])
        except Exception:
            base_dict['OppositionCurrentStatusText'].append('')

        # OppositionTotalQuantity #
        try :
            base_dict['OppositionTotalQuantity'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:OppositionTotalQuantity'])
        except Exception:
            base_dict['OppositionTotalQuantity'].append('')

        log('############ Trademark Common Success')
        


        ################################### 여기까지 공용정보 ##########################################################

        ################ Pulbication Bag 시작 #########################################################################

        
        try :
            # Publication Bag
            if type(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication']) == dict:
                # id #
                try :
                    Publication_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Publication_dict['id'].append('')

                # PublicationDate #
                try :
                    Publication_dict['PublicationDate'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication']['com:PublicationDate'])
                except Exception:
                    Publication_dict['PublicationDate'].append('')

                # PublicationIdentifier #
                try :
                    Publication_dict['PublicationIdentifier'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication']['com:PublicationIdentifier'])
                except Exception:
                    Publication_dict['PublicationIdentifier'].append('')
                
                # PublicationSectionCategory #
                try :
                    Publication_dict['PublicationSectionCategory'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication']['tmk:PublicationSectionCategory'])
                except Exception:
                    Publication_dict['PublicationSectionCategory'].append('')

            elif type(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication']) == list:
                count = 0
                while count < len(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication']):
                    
                    # id
                    try :
                        Publication_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Publication_dict['id'].append('')
                    
                    # PublicationDate #
                    try :
                        Publication_dict['PublicationDate'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication'][count]['com:PublicationDate'])
                    except Exception :
                        Publication_dict['PublicationDate'].append('')
                    
                    # PublicationIdentifier #
                    try :
                        Publication_dict['PublicationIdentifier'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication'][count]['com:PublicationIdentifier'])
                    except Exception :
                        Publication_dict['PublicationIdentifier'].append('')

                    # PublicationSectionCategory #
                    try :
                        Publication_dict['PublicationSectionCategory'].append(base['krtmk:OppositionBibliographicData']['krtmk:BasicInformation']['krtmk:PublicationBag']['krtmk:Publication'][count]['tmk:PublicationSectionCategory'])
                    except Exception :
                        Publication_dict['PublicationSectionCategory'].append('')    
                    
                    count += 1
        except Exception :
            pass
        
        log('############ Trademark Publication Success')

        


        ######################## 여기까지 Publication 정보 ####################################################

        ############ Staff 시작 ##########################################################################
        try:
            # Staff Bag
            if type(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['com:StaffBag']['com:Staff']) == dict:
                # id
                try :
                    Staff_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Staff_dict['id'].append('')

                # StaffName #
                try :
                    Staff_dict['StaffName'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['com:StaffBag']['com:Staff']['com:StaffName'])
                except Exception:
                    Staff_dict['StaffName'].append('')

            elif type(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['com:StaffBag']['com:Staff']) == list:
                
                count = 0
                while count < len(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['com:StaffBag']['com:Staff']):
                    # id
                    try :
                        Staff_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
            
                    except Exception:
                        Staff_dict['id'].append('')

                    # StaffName #
                    try :
                        Staff_dict['StaffName'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['com:StaffBag']['com:Staff'][count]['com:StaffName'])
                    except Exception :
                        Staff_dict['StaffName'].append('')
                    
                    count += 1
        except Exception:
            pass
        
        log('############ Trademark Staff Success')
        
        

        ########################### 여기까지 Staff 정보 #########################################################

        ############################# PlaintiffBag 시작 #############################################################

            # PlaintiffBag
        try :
            if type(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']) == dict:
                # id #
                try :
                    Plantiff_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Plantiff_dict['id'].append('')

                # sequenceNumber #
                try :
                    Plantiff_dict['sequenceNumber'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff']['@com:sequenceNumber'])
                except Exception:
                    Plantiff_dict['sequenceNumber'].append('')

                # EntityName #
                try :
                    Plantiff_dict['EntityName'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff']['com:Contact']['com:Name']['com:EntityName'])
                except Exception:
                    Plantiff_dict['EntityName'].append('')

                # NationalityCode #
                try :
                    Plantiff_dict['NationalityCode'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff']['com:NationalityCode'])
                except Exception:
                    Plantiff_dict['NationalityCode'].append('')


                # OrganizationStandardName #
                try :
                    Plantiff_dict['OrganizationStandardName'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff']['com:Contact']['com:Name']['com:OrganizationName']['com:OrganizationStandardName'])
                except Exception:
                    Plantiff_dict['OrganizationStandardName'].append('')
                    

            elif type(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']) == list:

                count = 0
                while count < len(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']):
                    # id
                    try :
                        Plantiff_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Plantiff_dict['id'].append('')

                    # sequenceNumber #
                    try :
                        Plantiff_dict['sequenceNumber'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff'][count]['@com:sequenceNumber'])
                    except Exception:
                        Plantiff_dict['sequenceNumber'].append('')

                    # EntityName #
                    try :
                        Plantiff_dict['EntityName'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff'][count]['com:Contact']['com:Name']['com:EntityName'])
                    except Exception:
                        Plantiff_dict['EntityName'].append('')

                    # NationalityCode #
                    try :
                        Plantiff_dict['NationalityCode'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff'][count]['com:NationalityCode'])
                    except Exception:
                        Plantiff_dict['NationalityCode'].append('')

                    # OrganizationStandardName
                    try :
                        Plantiff_dict['OrganizationStandardName'].append(base['krtmk:OppositionBibliographicData']['krtmk:OppositionInformation']['krcom:PlaintiffBag']['krcom:Plaintiff'][count]['com:Contact']['com:Name']['com:OrganizationName']['com:OrganizationStandardName'])
                    except Exception:
                        Plantiff_dict['OrganizationStandardName'].append('')
                    
                    count += 1
        except Exception:
            pass
    
        log('############ Trademark Plantiff Success')
        
        

        ############################# PlaintiffBag 끝 #############################################################
        

import os

path = '/data3/3_kipris/csv/47_이의신청서(전문)/Trademark/'

os.makedirs(path, exist_ok=True)

base_df = pd.DataFrame(base_dict)
base_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Trademark/Trademark.csv', encoding = 'utf-8-sig', index = False )

Publication_df = pd.DataFrame(Publication_dict)
Publication_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Trademark/Trademark(Publication).csv', encoding = 'utf-8-sig', index = False )

Staff_df = pd.DataFrame(Staff_dict)
Staff_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Trademark/Trademark(Staff).csv', encoding = 'utf-8-sig', index = False )

Plantiff_df = pd.DataFrame(Plantiff_dict)
Plantiff_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Trademark/Trademark(Plantiff).csv', encoding = 'utf-8-sig', index = False )

log('############ Trademark Making data Success')
