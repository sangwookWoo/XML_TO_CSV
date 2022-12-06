############################ import library ##################################################

# import
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


#################################### function ##################################################
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

##################################### make data ####################################################
path = '/data3/3_kipris/seperate/47_이의신청서지(전문)/'

file_list = read_filelist(path)
file_list_py = [file for file in file_list if file.endswith('xml')]

# 데이터프레임 정의
base_dict = defaultdict(list)
Publication_dict = defaultdict(list)
Staff_dict = defaultdict(list)
Opponent_dict = defaultdict(list)
for idx, xml_data_path in enumerate(file_list_py):
    log('######## ({}) Convert {}'.format(idx, xml_data_path))
    if 'design' in xml_data_path or 'Design' in xml_data_path or 'DS' in xml_data_path:
        # xml에 대한 딕셔너리 반환
        dict_of_xml = return_dict(xml_data_path)
        base = dict_of_xml['krdgn:DesignOppositionBibliography']

        ################# 공용정보 만들기 ################################
        # id
        try :
            base_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
        except Exception:
            base_dict['id'].append('')

        # languageCode
        try :
            base_dict['languageCode'].append(base['krcom:DocumentCreation']['@com:languageCode'])
        except Exception:
            base_dict['languageCode'].append('')

        # DocumentDate
        try :
            base_dict['DocumentDate'].append(base['krcom:DocumentCreation']['com:DocumentDate'])
        except Exception:
            base_dict['DocumentDate'].append('')
        
        # DocumentName
        try :
            base_dict['DocumentName'].append(base['krcom:DocumentCreation']['com:DocumentName'])
        except Exception:
            base_dict['DocumentName'].append('')

        # DocumentOffice
        try :
            base_dict['DocumentOffice'].append(base['krcom:DocumentCreation']['krcom:DocumentOffice'])
        except Exception:
            base_dict['DocumentOffice'].append('')

        # operationCategory
        try :
            base_dict['operationCategory'].append(base['krdgn:OppositionBibliographicData']['@com:operationCategory'])
        except Exception:
            base_dict['operationCategory'].append('')

        # OppositionDate
        try :
            base_dict['OppositionDate'].append(base['krdgn:OppositionBibliographicData']['krcom:OppositionIdentification']['com:OppositionDate'])
        except Exception:
            base_dict['OppositionDate'].append('')

        # OppositionIdentifier
        try :
            base_dict['OppositionIdentifier'].append(base['krdgn:OppositionBibliographicData']['krcom:OppositionIdentification']['com:OppositionIdentifier'])
        except Exception:
            base_dict['OppositionIdentifier'].append('')
        
        # EventNumberText
        try :
            base_dict['EventNumberText'].append(base['krdgn:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:EventNumberText'])
        except Exception:
            base_dict['EventNumberText'].append('')
        
        # RightKindText
        try :
            base_dict['RightKindText'].append(base['krdgn:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:RightKindText']['#text'])
        except Exception:
            base_dict['RightKindText'].append('')
        
        # RightKindText_languageCode
        try :
            base_dict['RightKindText_languageCode'].append(base['krdgn:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:RightKindText']['@com:languageCode'])
        except Exception:
            base_dict['RightKindText_languageCode'].append('')

        # ApplicationNumberText
        try :
            base_dict['ApplicationNumberText'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['com:ApplicationNumber']['com:ApplicationNumberText'])
        except Exception:
            base_dict['ApplicationNumberText'].append('')

        # IPOfficeCode
        try :
            base_dict['IPOfficeCode'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['com:ApplicationNumber']['com:IPOfficeCode'])
        except Exception:
            base_dict['IPOfficeCode'].append('')

        # RegistrationDate
        try :
            base_dict['RegistrationDate'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['com:RegistrationDate'])
        except Exception:
            base_dict['RegistrationDate'].append('')

        # RegistrationNumber
        try :
            base_dict['RegistrationNumber'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['com:RegistrationNumber'])
        except Exception:
            base_dict['RegistrationNumber'].append('')
        
        # DesignApplicationDate
        try :
            base_dict['DesignApplicationDate'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:DesignApplicationDate'])
        except Exception:
            base_dict['DesignApplicationDate'].append('')

        # DecisionDate
        try :
            base_dict['DecisionDate'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['krcom:Decision']['krcom:DecisionDate'])
        except Exception:
            base_dict['DecisionDate'].append('')

        # DecisionText
        try :
            base_dict['DecisionText'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['krcom:Decision']['krcom:DecisionText'])
        except Exception:
            base_dict['DecisionText'].append('')

        # OppositionCurrentStatusText
        try :
            base_dict['OppositionCurrentStatusText'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['krcom:OppositionCurrentStatusText'])
        except Exception:
            base_dict['OppositionCurrentStatusText'].append('')

        # OppositionTotalQuantity
        try :
            base_dict['OppositionTotalQuantity'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['krcom:OppositionTotalQuantity'])
        except Exception:
            base_dict['OppositionTotalQuantity'].append('')

        log('############ Design Common Success')
        


        ################################### 여기까지 공용정보 ##########################################################

        ################ Pulbication Bag 시작 #########################################################################

        
        try :
            # Publication Bag
            if type(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication']) == dict:
                # id
                try :
                    Publication_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Publication_dict['id'].append('')

                # PublicationDate
                try :
                    Publication_dict['PublicationDate'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication']['com:PublicationDate'])
                except Exception:
                    Publication_dict['PublicationDate'].append('')

                # PublicationIdentifier
                try :
                    Publication_dict['PublicationIdentifier'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication']['com:PublicationIdentifier'])
                except Exception:
                    Publication_dict['PublicationIdentifier'].append('')
                    
                # DesignPublicationCategory
                try :
                    Publication_dict['DesignPublicationCategory'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication']['dgn:DesignPublicationCategory'])
                except Exception:
                    Publication_dict['DesignPublicationCategory'].append('')

            elif type(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication']) == list:
                count = 0
                while count < len(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication']):
                    
                    # id
                    try :
                        Publication_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Publication_dict['id'].append('')
                    
                    # PublicationDate
                    try :
                        Publication_dict['PublicationDate'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication'][count]['com:PublicationDate'])
                    except Exception :
                        Publication_dict['PublicationDate'].append('')
                    
                    # PublicationIdentifier
                    try :
                        Publication_dict['PublicationIdentifier'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication'][count]['com:PublicationIdentifier'])
                    except Exception :
                        Publication_dict['PublicationIdentifier'].append('')

                    # DesignPublicationCategory
                    try :
                        Publication_dict['DesignPublicationCategory'].append(base['krdgn:OppositionBibliographicData']['krdgn:BasicInformation']['dgn:PublicationBag']['dgn:Publication'][count]['dgn:DesignPublicationCategory'])
                    except Exception :
                        Publication_dict['DesignPublicationCategory'].append('')    
                    
                    count += 1
        except Exception :
            pass
        

        log('############ Design Publication Success')
        
        


        ######################## 여기까지 Publication 정보 ####################################################

        ############ Staff 시작 ##########################################################################
        try:
                # Staff Bag
            if type(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['com:StaffBag']['com:Staff']) == dict:
                # id
                try :
                    Staff_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Staff_dict['id'].append('')

                # StaffName
                try :
                    Staff_dict['StaffName'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['com:StaffBag']['com:Staff']['com:StaffName'])
                except Exception:
                    Staff_dict['StaffName'].append('')

            elif type(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['com:StaffBag']['com:Staff']) == list:

                count = 0
                while count < len(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['com:StaffBag']['com:Staff']):
                    # id
                    try :
                        Staff_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Staff_dict['id'].append('')

                    # StaffName
                    try :
                        Staff_dict['StaffName'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['com:StaffBag']['com:Staff'][count]['com:StaffName'])
                    except Exception :
                        Staff_dict['StaffName'].append('')
                    
                    count += 1
        except Exception:
            pass
        
        
        log('############ Design Staff Success')
        

        ########################### 여기까지 Staff 정보 #########################################################

        ############################# Opponent 시작 #############################################################

            # Opponent Bag
        try :
            if type(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']) == dict:
                # id
                try :
                    Opponent_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Opponent_dict['id'].append('')

                # EntityName
                try :
                    Opponent_dict['EntityName'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']['dgn:Opponent']['com:Contact']['com:Name']['com:EntityName'])
                except Exception:
                    Opponent_dict['EntityName'].append('')

                # NationalityCode
                try :
                    
                    Opponent_dict['NationalityCode'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']['dgn:Opponent']['com:NationalityCode'])
                except Exception:
                    Opponent_dict['NationalityCode'].append('')

                # OrganizationStandardName
                try :
                    Opponent_dict['OrganizationStandardName'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']['dgn:Opponent']['com:Contact']['com:Name']['com:OrganizationName']['com:OrganizationStandardName'])
                except Exception:
                    Opponent_dict['OrganizationStandardName'].append('')
                    

            elif type(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']) == list:

                count = 0
                while count < len(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']):
                    # id
                    try :
                        Opponent_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Opponent_dict['id'].append('')

                    # EntityName
                    try :
                        Opponent_dict['EntityName'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']['dgn:Opponent'][count]['com:Contact']['com:Name']['com:EntityName'])
                    except Exception :
                        Opponent_dict['EntityName'].append('')

                    # NationalityCode
                    try :
                        Opponent_dict['NationalityCode'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']['dgn:Opponent'][count]['com:NationalityCode'])
                    except Exception:
                        Opponent_dict['NationalityCode'].append('')

                    # OrganizationStandardName
                    try :
                        Opponent_dict['OrganizationStandardName'].append(base['krdgn:OppositionBibliographicData']['krdgn:OppositionInformation']['dgn:OpponentBag']['dgn:Opponent'][count]['com:Contact']['com:Name']['com:OrganizationName']['com:OrganizationStandardName'])
                    except Exception:
                        Opponent_dict['OrganizationStandardName'].append('')
                    
                    count += 1
        except Exception:
            pass
            
    
        
        log('############ Design Opponent Success')
        

        ############################# Opponent 끝 #############################################################

import os

path = '/data3/3_kipris/csv/47_이의신청서(전문)/Design/'

os.makedirs(path, exist_ok=True)

############################
base_df = pd.DataFrame(base_dict)
base_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Design/Design.csv', encoding = 'utf-8-sig', index = False )

Publication_df = pd.DataFrame(Publication_dict)
Publication_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Design/Design(Publication).csv', encoding = 'utf-8-sig', index = False )

Staff_df = pd.DataFrame(Staff_dict)
Staff_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Design/Design(Staff).csv', encoding = 'utf-8-sig', index = False )

Opponent_df = pd.DataFrame(Opponent_dict)
Opponent_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Design/Design(Opponent).csv', encoding = 'utf-8-sig', index = False )



