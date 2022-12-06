############################# import ##################################################
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

################################### function ###################################################

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


################################################ make data ##############################################################

path = '/data3/3_kipris/seperate/47_이의신청서지(전문)/'

file_list = read_filelist(path)
file_list_py = [file for file in file_list if file.endswith('xml')]

# 데이터프레임 정의
base_dict = defaultdict(list)
Publication_dict = defaultdict(list)
Staff_dict = defaultdict(list)
Opponent_dict = defaultdict(list)
InventionTitle_dict = defaultdict(list)
Assist_Examiner_dict = defaultdict(list)
Primary_Examiner_dict = defaultdict(list)
for idx, xml_data_path in enumerate(file_list_py):
    log('######## ({}) Convert {}'.format(idx, xml_data_path))
    if 'PT' in xml_data_path:
        # xml에 대한 딕셔너리 반환
        dict_of_xml = return_dict(xml_data_path)
        base = dict_of_xml['krpat:PatentOppositionBibliography']
        #print(dict_of_xml)
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
            base_dict['operationCategory'].append(base['krpat:OppositionBibliographicData']['@com:operationCategory'])
        except Exception:
            base_dict['operationCategory'].append('')

        # OppositionDate
        try :
            base_dict['OppositionDate'].append(base['krpat:OppositionBibliographicData']['krcom:OppositionIdentification']['com:OppositionDate'])
        except Exception:
            base_dict['OppositionDate'].append('')

        # OppositionIdentifier
        try :
            base_dict['OppositionIdentifier'].append(base['krpat:OppositionBibliographicData']['krcom:OppositionIdentification']['com:OppositionIdentifier'])
        except Exception:
            base_dict['OppositionIdentifier'].append('')
        
        # EventNumberText
        try :
            base_dict['EventNumberText'].append(base['krpat:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:EventNumberText'])
        except Exception:
            base_dict['EventNumberText'].append('')
        
        # RightKindText
        try :
            base_dict['RightKindText'].append(base['krpat:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:RightKindText']['#text'])
        except Exception:
            base_dict['RightKindText'].append('')
        
        # RightKindText_languageCode
        try :
            base_dict['RightKindText_languageCode'].append(base['krpat:OppositionBibliographicData']['krcom:OppositionIdentification']['krcom:RightKindText']['@com:languageCode'])
        except Exception:
            base_dict['RightKindText_languageCode'].append('')

        # ApplicationNumberText #
        try :
            base_dict['ApplicationNumberText'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:ApplicationIdentification']['com:ApplicationNumber']['com:ApplicationNumberText'])
        except Exception:
            base_dict['ApplicationNumberText'].append('')  

        # Application_IPOfficeCode #
        try :
            base_dict['Application_IPOfficeCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:ApplicationIdentification']['com:IPOfficeCode'])
        except Exception:
            base_dict['Application_IPOfficeCode'].append('')

        # Application_FilingDate #
        try :
            base_dict['Application_FilingDate'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:ApplicationIdentification']['pat:FilingDate'])
        except Exception:
            base_dict['Application_FilingDate'].append('')

        # PatentGrantIdentification_IPOfficeCode #
        try :
            base_dict['PatentGrantIdentification_IPOfficeCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:PatentGrantIdentification']['com:IPOfficeCode'])
        except Exception:
            base_dict['PatentGrantIdentification_IPOfficeCode'].append('')

        # PatentGrantIdentification_GrantDate #
        try :
            base_dict['PatentGrantIdentification_GrantDate'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:PatentGrantIdentification']['pat:GrantDate'])
        except Exception:
            base_dict['PatentGrantIdentification_GrantDate'].append('')

        # PatentGrantIdentification_Number #
        try :
            base_dict['PatentGrantIdentification_Number'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:PatentGrantIdentification']['pat:PatentNumber'])
        except Exception:
            base_dict['PatentGrantIdentification_Number'].append('')
        

        # OppositionExtentText #
        try :
            base_dict['OppositionExtentText'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['com:OppositionExtentText'])
        except Exception:
            base_dict['OppositionExtentText'].append('')

        # DecisionDate #
        try :
            base_dict['DecisionDate'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krcom:Decision']['krcom:DecisionDate'])
        except Exception:
            base_dict['DecisionDate'].append('')

        # DecisionText #
        try :
            base_dict['DecisionText'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krcom:Decision']['krcom:DecisionText'])
        except Exception:
            base_dict['DecisionText'].append('')
        
        # OppositionCurrentStatusText #
        try :
            base_dict['OppositionCurrentStatusText'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krcom:OppositionCurrentStatusText'])
        except Exception:
            base_dict['OppositionCurrentStatusText'].append('')
        
        # OppositionTotalQuantity #
        try :
            base_dict['OppositionTotalQuantity'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krcom:OppositionTotalQuantity'])
        except Exception:
            base_dict['OppositionTotalQuantity'].append('')

        # OppositionCancellationClaimQuantity
        try :
            base_dict['OppositionCancellationClaimQuantity'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OppositionExtentDetail']['krpat:OppositionCancellationClaimQuantity'])
        except Exception:
            base_dict['OppositionCancellationClaimQuantity'].append('')

        # OppositionCancellationClaimText
        try :
            base_dict['OppositionCancellationClaimText'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OppositionExtentDetail']['krpat:OppositionCancellationClaimText'])
        except Exception:
            base_dict['OppositionCancellationClaimText'].append('')

        # OppositionDeletionQuantity
        try :
            base_dict['OppositionDeletionQuantity'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OppositionExtentDetail']['krpat:OppositionDeletionQuantity'])
        except Exception:
            base_dict['OppositionDeletionQuantity'].append('') 

        # OppositionRemainClaimQuantity
        try :
            base_dict['OppositionRemainClaimQuantity'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OppositionExtentDetail']['krpat:OppositionRemainClaimQuantity'])
        except Exception:
            base_dict['OppositionRemainClaimQuantity'].append('')    

        
        log('############ Patent Common Success')
    

        ################################### 여기까지 공용정보 ##########################################################

        ################################### InventionTitle 시작 ##########################################################
        ## invention title Bag
        try:
            # PatentPublicationIdentificationBag
            if type(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:InventionTitleBag']) == dict:
                # id
                try :
                    InventionTitle_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    InventionTitle_dict['id'].append('')

                # InventionTitle #
                try :
                    InventionTitle_dict['InventionTitle'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:InventionTitleBag']['pat:InventionTitle']['#text'])
                except Exception:
                    InventionTitle_dict['InventionTitle'].append('')

                # InventionTitle_languageCode
                try :
                    InventionTitle_dict['InventionTitle_languageCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:InventionTitleBag']['pat:InventionTitle']['@com:languageCode'])
                except Exception:
                    InventionTitle_dict['InventionTitle_languageCode'].append('')




            elif type(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:InventionTitleBag']) == list:
                
                count = 0
                while count < len(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:InventionTitleBag']):
                    # id
                    try :
                        InventionTitle_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        InventionTitle_dict['id'].append('')

                    # InventionTitle #
                    try :
                        InventionTitle_dict['InventionTitle'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:InventionTitleBag']['pat:InventionTitle'][count]['#text'])
                    except Exception:
                        InventionTitle_dict['InventionTitle'].append('')

                    # InventionTitle_languageCode
                    try :
                        InventionTitle_dict['InventionTitle_languageCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['pat:InventionTitleBag']['pat:InventionTitle'][count]['@com:languageCode'])
                    except Exception:
                        InventionTitle_dict['InventionTitle_languageCode'].append('')


                    
                    count += 1

        except Exception:
            pass
        
        log('############ Patent Invention Success')
        
        ################################### InventionTitle 끝 ##########################################################
        ######################## Publication 시작 ####################################################
        try:
            # PatentPublicationIdentificationBag
            if type(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']) == dict:
                print(len(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']))
                # id
                try :
                    Publication_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Publication_dict['id'].append('')

                # IPOfficeCode #
                try :
                    Publication_dict['IPOfficeCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']['com:IPOfficeCode'])
                except Exception:
                    Publication_dict['IPOfficeCode'].append('')

                # PatentDocumentKindCode
                try :
                    Publication_dict['PatentDocumentKindCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']['com:PatentDocumentKindCode'])
                except Exception:
                    Publication_dict['PatentDocumentKindCode'].append('')

                # PublicationDate
                try :
                    Publication_dict['PublicationDate'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']['com:PublicationDate'])
                except Exception:
                    Publication_dict['PublicationDate'].append('')

                # PublicationNumber
                try :
                    Publication_dict['PublicationNumber'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']['pat:PublicationNumber'])
                except Exception:
                    Publication_dict['PublicationNumber'].append('')





            elif type(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']) == list:
                
                count = 0
                while count < len(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification']):
                    # id
                    try :
                        Publication_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Publication_dict['id'].append('')

                    # IPOfficeCode #
                    try :
                        Publication_dict['IPOfficeCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification'][count]['com:IPOfficeCode'])
                    except Exception:
                        Publication_dict['IPOfficeCode'].append('')

                    # PatentDocumentKindCode
                    try :
                        Publication_dict['PatentDocumentKindCode'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification'][count]['com:PatentDocumentKindCode'])
                    except Exception:
                        Publication_dict['PatentDocumentKindCode'].append('')

                    # PublicationDate
                    try :
                        Publication_dict['PublicationDate'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification'][count]['com:PublicationDate'])
                    except Exception as E:
                        Publication_dict['PublicationDate'].append('')
                        print(E)
                    # PublicationNumber
                    try :
                        Publication_dict['PublicationNumber'].append(base['krpat:OppositionBibliographicData']['krpat:BasicInformation']['krpat:PatentPublicationIdentificationBag']['pat:PatentPublicationIdentification'][count]['pat:PublicationNumber'])
                    except Exception:
                        Publication_dict['PublicationNumber'].append('')

                    
                    count += 1
        except Exception:
            pass
        
        log('############ Patent  PatentPublicationIdentificationBag Success')


        
        

        ########################### 여기까지 Publication 정보 #########################################################

        ############################# Opponent 시작 #############################################################

            # Opponent Bag
        try :
            if type(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']) == dict:
                # id
                try :
                    Opponent_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Opponent_dict['id'].append('')

                # OppositionCurrentStatusText
                try :
                    Opponent_dict['OppositionCurrentStatusText'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krcom:OppositionCurrentStatusText'])
                except Exception:
                    Opponent_dict['id'].append('')

                # NationalityCode
                try :
                    
                    Opponent_dict['NationalityCode'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']['krpat:Opponent']['com:NationalityCode'])
                except Exception:
                    Opponent_dict['NationalityCode'].append('')

                # EntityName
                try :
                    Opponent_dict['EntityName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']['krpat:Opponent']['com:Contact']['com:Name']['com:EntityName'])
                except Exception:
                    Opponent_dict['EntityName'].append('')

                # OrganizationStandardName
                try :
                    Opponent_dict['OrganizationStandardName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']['krpat:Opponent']['com:Contact']['com:Name']['com:OrganizationName']['com:OrganizationStandardName'])
                except Exception:
                    Opponent_dict['OrganizationStandardName'].append('')
                    

            elif type(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']) == list:

                count = 0
                while count < len(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']):

                    # id
                    try :
                        Opponent_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Opponent_dict['id'].append('')
                    
                    # OppositionCurrentStatusText
                    try :
                        Opponent_dict['OppositionCurrentStatusText'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krcom:OppositionCurrentStatusText'])
                    except Exception:
                        Opponent_dict['id'].append('')

                    # NationalityCode
                    try :
                        
                        Opponent_dict['NationalityCode'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']['krpat:Opponent'][count]['com:NationalityCode'])
                    except Exception:
                        Opponent_dict['NationalityCode'].append('')

                    # EntityName
                    try :
                        Opponent_dict['EntityName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']['krpat:Opponent'][count]['com:Contact']['com:Name']['com:EntityName'])
                    except Exception:
                        Opponent_dict['EntityName'].append('')

                    # OrganizationStandardName
                    try :
                        Opponent_dict['OrganizationStandardName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:OpponentBag']['krpat:Opponent'][count]['com:Contact']['com:Name']['com:OrganizationName']['com:OrganizationStandardName'])
                    except Exception:
                        Opponent_dict['OrganizationStandardName'].append('')
                    
                    
                    count += 1
        except Exception:
            pass
    
        log('############ Patent  Opponent Bag Success')
        
        

        ############################# Opponent_Bag 끝 #############################################################

        ################################### Examiner Bag 시작 ##########################################################
        ## Examiner Bag
        # Assistant Examiner & Primary Examiner
        try:
            if type(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:AssistantExaminer']) == dict:

                # id
                try :
                    Assist_Examiner_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Assist_Examiner_dict['id'].append('')

                # Examiner_category
                try :
                    Assist_Examiner_dict['Category'].append('AssistantExaminer')
                except Exception:
                    Assist_Examiner_dict['Category'].append('')

                # AssistantExaminer_sequenceNumber #
                try :
                    Assist_Examiner_dict['SequenceNumber'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:AssistantExaminer']['@com:sequenceNumber'])

                except Exception:
                    Assist_Examiner_dict['SequenceNumber'].append('')

                # AssistantExaminer_EntityName
                try :
                    Assist_Examiner_dict['EntityName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:AssistantExaminer']['com:Name']['com:EntityName'])

                except Exception:
                    Assist_Examiner_dict['EntityName'].append('')



            elif type(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:AssistantExaminer']) == list:
                
                count = 0

                while count < len(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:AssistantExaminer']):
                    # id
                    try :
                        Assist_Examiner_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Assist_Examiner_dict['id'].append('')

                    # Examiner_category
                    try :
                        Assist_Examiner_dict['Category'].append('AssistantExaminer')
                    except Exception:
                        Assist_Examiner_dict['Category'].append('')


                    # AssistantExaminer_sequenceNumber #
                    try :
                        Assist_Examiner_dict['SequenceNumber'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:AssistantExaminer'][count]['@com:sequenceNumber'])
                    except Exception:
                        Assist_Examiner_dict['SequenceNumber'].append('')

                    # AssistantExaminer_EntityName
                    try :
                        Assist_Examiner_dict['EntityName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:AssistantExaminer'][count]['com:Name']['com:EntityName'])
                    except Exception:
                        Assist_Examiner_dict['EntityName'].append('')


                    
                    count += 1
                    
        except Exception:
            pass
        
        log('############ Patent AssistExaminer Success')

        ################################### Primary Examiner #########################################################
        #Primary Examiner
        try:
            if type(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:PrimaryExaminer']) == dict:

                # id
                try :
                    Primary_Examiner_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                except Exception:
                    Primary_Examiner_dict['id'].append('')

                # Examiner_category
                try :
                    Primary_Examiner_dict['Category'].append('PrimaryExaminer')
                except Exception:
                    Primary_Examiner_dict['Category'].append('')

                # PrimaryExaminer_sequenceNumber #
                try :
                    Primary_Examiner_dict['SequenceNumber'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:PrimaryExaminer']['@com:sequenceNumber'])

                except Exception:
                    Primary_Examiner_dict['SequenceNumber'].append('')

                # PrimaryExaminer_EntityName
                try :
                    Primary_Examiner_dict['EntityName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:PrimaryExaminer']['com:Name']['com:EntityName'])

                except Exception:
                    Primary_Examiner_dict['EntityName'].append('')



            elif type(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:PrimaryExaminer']) == list:
                
                count = 0

                while count < len(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:PrimaryExaminer']):
                    # id
                    try :
                        Primary_Examiner_dict['id'].append(base['krcom:DocumentCreation']['@com:id'])
                    except Exception:
                        Primary_Examiner_dict['id'].append('')

                    # Examiner_category
                    try :
                        Primary_Examiner_dict['Category'].append('PrimaryExaminer')
                    except Exception:
                        Primary_Examiner_dict['Category'].append('')


                    # PrimaryExaminer_sequenceNumber #
                    try :
                        Primary_Examiner_dict['SequenceNumber'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:PrimaryExaminer'][count]['@com:sequenceNumber'])
                    except Exception:
                        Primary_Examiner_dict['SequenceNumber'].append('')

                    # PrimaryExaminer_EntityName
                    try :
                        Primary_Examiner_dict['EntityName'].append(base['krpat:OppositionBibliographicData']['krpat:OppositionInformation']['krpat:ExaminerBag']['krpat:PrimaryExaminerExaminer'][count]['com:Name']['com:EntityName'])
                    except Exception:
                        Primary_Examiner_dict['EntityName'].append('')


                    
                    count += 1
                    
        except Exception:
            pass
        
        log('############ Patent Primary Examiner Success')

        ################################### Examiner 끝 ##########################################################

import os
path = '/data3/3_kipris/csv/47_이의신청서(전문)/Patent/'
os.makedirs(path, exist_ok=True)

base_df = pd.DataFrame(base_dict)
base_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Patent/Patent.csv', encoding = 'utf-8-sig', index = False )

Publication_df = pd.DataFrame(Publication_dict)
Publication_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Patent/Patent(Publication).csv', encoding = 'utf-8-sig', index = False )

Opponent_df = pd.DataFrame(Opponent_dict)
Opponent_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Patent/Patent(Opponent).csv', encoding = 'utf-8-sig', index = False )

InventionTitle_df = pd.DataFrame(InventionTitle_dict)
InventionTitle_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Patent/Patent(Inventional).csv', encoding = 'utf-8-sig', index = False )

Assist_Examiner_df = pd.DataFrame(Assist_Examiner_dict)
Primary_Examiner_df = pd.DataFrame(Primary_Examiner_dict)
Examiner_df = pd.concat([Assist_Examiner_df, Primary_Examiner_df])
Examiner_df = Examiner_df.sort_values(by= ['id', 'Category'])
Examiner_df.to_csv('/data3/3_kipris/csv/47_이의신청서(전문)/Patent/Patent(Examinal).csv', encoding = 'utf-8-sig', index = False )

log('############ Patent making data Success')

