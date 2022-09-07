# =============================================================================
# CompleatData
# Accepting a pandas datafram with cleand user data
# returns a datafram with data derived from the user data
# Fills in default parameters for missing values
#
# Jesper Jacobsson
# 2020 06
# =============================================================================

from datetime import datetime
import os
import pickle

from crossref.restful import Works, Etiquette
import numpy as np
import pandas as pd

import UtilityFunctions.CompleatDataFunctionsV5 as codf


def citationData(DOInumbers, defaultDate, defaultAuthor, DOIPath):
    '''Extract citation data from CrossRf based on the DOI number 
    Stor all downloaded reference data in a pickle file located at DOIPath'''

    #%% Use crossref (https://www.crossref.org/) to extract metadata
    # Setting up a session at crossref
    my_etiquette = Etiquette('Perovskite solar', 'version 1', '', 'jacobsson.jesper.work@gmail.com')
    works = Works()
    works = Works(etiquette=my_etiquette)


    #%% Download reference data
     # open a file with previously downloaded reference information if it excist
    if os.path.exists(DOIPath) == True:
        Old_DOI_file_excist = True
        with open(DOIPath, 'rb') as f:
            DOI_saved = pickle.load(f)
    else:
        Old_DOI_file_excist = False


    # Define a dataframe to temporaly store all not previously stored reference information
    DOI_saved_files_temp = pd.DataFrame()
    DOI_saved_files_temp['DOI'] = []
    DOI_saved_files_temp['Dict'] = []

    # Download reference data for all DOI not previously downloaded
    if Old_DOI_file_excist == True:
        listOfSavedDOI = DOI_saved['DOI'].tolist()
    else:
        listOfSavedDOI = []
    
    
    for i, DOI in enumerate(DOInumbers):
        # Check if metadata already is downloaded
        if DOI in listOfSavedDOI or DOI in DOI_saved_files_temp['DOI'].tolist() or DOI == "nan":
            continue
        else:
            print(f'Searching for citation data for paper on row {i}') # for keeping track of progress during development
            # Get the metadata for the paper from Crossref
            try:
                paper = works.doi(DOI)
                
                if type(paper) == dict:
                    # Add the data to the temprary dataframe
                    DOI_saved_files_temp = DOI_saved_files_temp.append({'DOI': DOI, 'Dict': paper}, ignore_index = True)
                else:
                    print(f'Failed to download data for: {DOI}')
                       
            except:
                print(f'Failed to download data for: {DOI}')          

    # Add the newly saved reference information to the already saved data
    if Old_DOI_file_excist == True:
        DOI_saved = DOI_saved.append(DOI_saved_files_temp, ignore_index = True)
    else:
        DOI_saved = DOI_saved_files_temp

    # Save the downloaded reference information
    try:
        with open(DOIPath, 'wb') as f:
            pickle.dump(DOI_saved, f)
    except:
        print(f'Failed to save new DOI data to reference file')

    #%% Extract metadata from the reference data
    data = pd.DataFrame()
    timestamp = []
    mainauthor = []
    journal = []

    for i, DOI in enumerate(DOInumbers):
        try:
            # Get the index for where the DOI is stored
            doiIndex = DOI_saved.index[DOI_saved['DOI'] == DOI].tolist()

            # Retriev the dictionary with the article metadata 
            MetaData = DOI_saved['Dict'].loc[doiIndex[0]]

            # Datetime when the paper was published
            try:
                date = MetaData['created']['date-parts'][0]           
                # Convert datetime string to datetime format
                date = datetime.strptime(str(date)[1:-1], '%Y, %m, %d').date()
            except:
                #date = pd.to_datetime(defaultDate[i])
                date = pd.to_datetime(defaultDate[i].replace(":", "-"))
                date = datetime.date(date)

            timestamp.append(date)

            # First autor's last name (does not get it right every time)
            try:
                if len(MetaData['author']) > 1:
                    author = MetaData['author'][0]['family'] + ' et al.'
                else:
                    author = MetaData['author'][0]['family']
            except:
                author = defaultAuthor[i]              
            mainauthor.append(author)

            # Journal
            try:
               journal.append(MetaData['container-title'][0])
            except:
               journal.append('-')
        except:

            try:
                #date = pd.to_datetime(str(defaultDate[i]))
                date = pd.to_datetime(str(defaultDate[i]).replace(":", "-"))
                date = datetime.date(date)
            except:
                # Default date
                #date = pd.to_datetime(str(2000))
                date = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
                date = datetime.date(date)

            timestamp.append(date)
            mainauthor.append(defaultAuthor[i] )
            journal.append('-')

    data['PublicationDate'] = timestamp
    data['FirstAuthor'] = mainauthor
    data['Journal'] = journal

    # Corect for corupt time data. That menas when date not was extracted from crossref and when the default user date not was in a readable date format
    #data['PublicationDate'] = pd.to_datetime(data['Ref_publication_date'], errors="coerce")
    data['PublicationDate'] = pd.to_datetime(data['PublicationDate'], errors="coerce")
    # Replace corupt values with todays date
    todays_time = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
    data['PublicationDate'].fillna(todays_time, inplace=True)


    return data

def DerivedtUserData(userData, fileName):
    '''Takes a pandas datafram with cleand user data and return a datafram with derived parameters'''

    print(f'Start to derrive data based on {fileName}')

    #%% Initiate an empty datafram to fill with cleaned data
    data = pd.DataFrame()


    #%% Ref. Part of the initial dataset
    data['Ref_part_of_initial_dataset'] = [False for x in range(len(userData))]

    #%% Ref. filename (for tracability purpouse)
    data['Ref_original_filename_data_upload'] = [fileName]*len(userData)

    #%% Ref_ID- Database ID. Will be reset later
    data['Ref_ID'] = list(range(1,len(userData) + 1))

    #%% Voc 
    # Determin the default Voc to plot, i.e. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan
    try:
        data['JV_Voc'], data['JV_Voc_scanDirection'] = codf.defaultVoc(userData)
    except:          
        print(f'Cound not derive the default Voc')
        data['JV_Voc'] = '' 
        data['JV_Voc_scanDirection'] = ''

    #%% Jsc 
    # Determin the default Jsc to plot, i.e. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan
    try:
        data['JV_Jsc'], data['JV_Jsc_scanDirection'] = codf.defaultJsc(userData)
    except:          
        print(f'Cound not derive the default Jsc')
        data['JV_Jsc'] = '' 
        data['JV_Jsc_scanDirection'] = ''

    #%% FF 
    # Determin the default FF to plot, i.e. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan
    try:
        data['JV_FF'], data['JV_FF_scanDirection'] = codf.defaultFF(userData)
    except:          
        print(f'Cound not derive the default FF')
        data['JV_FF'] = '' 
        data['JV_FF_scanDirection'] = ''

    #%% PCE 
    # Determin the default PCE to plot, i.e. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan
    try:
        data['JV_PCE'], data['JV_PCE_scanDirection'] = codf.defaultPCE(userData)
    except:          
        print(f'Cound not derive the default PCE')
        data['JV_PCE'] = '' 
        data['JV_PCE_scanDirection'] = ''

    #%% Hysteresis index
    try:
        data['HysteresisIndex'] = codf.hysteresisIndex(userData)
    except:          
        print(f'Cound not derive the Hysteresis Index')
        data['HysteresisIndex'] = ''

    #%% Perovskite short composition
    try:
        data['PerovskiteShortComp'] = codf.perovskiteShortComp(userData)
    except:           
        print(f'Cound not derive the PerovskiteShortComp:')
        data['PerovskiteShortComp'] = '' 

    #%% Perovskite long composition
    try:
        data['PerovskiteLongComp'] = codf.perovskiteLongComp(userData)
    except:           
        print(f'Cound not derive the PerovskiteLongComp:')
        data['PerovskiteLongComp'] = '' 

    #%% Leadfree perovskite
    try:
        data['Lead_free'] = codf.isLeadFree(data['PerovskiteLongComp'])
    except:           
        print(f'Cound not determin if lead free perovskite:')
        data['Lead_free'] = ''

    print(f'Finished to derrive data based on {fileName}')
    return data

def mergeData(cleanedData, derivedData, citationData):
    '''Takes cleanedData, derivedData, and citationData and returns on 
    dataframe with all data ready for uploading to the database'''

    # start from the cleanedData dataframe
    compleatData = cleanedData

    # Citation data
    compleatData['Ref_lead_author'] = citationData['FirstAuthor']
    compleatData['Ref_publication_date'] = citationData['PublicationDate']
    compleatData.insert(6, "Ref_journal", citationData['Journal'])

    # Derrived data
    compleatData.insert(7, "Ref_part_of_initial_dataset", derivedData['Ref_part_of_initial_dataset'])
    compleatData.insert(8, "Ref_original_filename_data_upload", derivedData['Ref_original_filename_data_upload'])

    compleatData.insert(1, "Ref_ID", derivedData['Ref_ID'])

    tempIndex = compleatData.columns.get_loc('Perovskite_composition_none_stoichiometry_components_in_excess')
    compleatData.insert(tempIndex + 1, "Perovskite_composition_short_form", derivedData['PerovskiteShortComp'])
    compleatData.insert(tempIndex + 2, "Perovskite_composition_long_form", derivedData['PerovskiteLongComp'])

    tempIndex = compleatData.columns.get_loc('JV_link_raw_data')
    compleatData.insert(tempIndex + 1, 'JV_default_Voc', derivedData['JV_Voc'])
    compleatData.insert(tempIndex + 2, 'JV_default_Jsc', derivedData['JV_Jsc'])
    compleatData.insert(tempIndex + 3, 'JV_default_FF', derivedData['JV_FF'])
    compleatData.insert(tempIndex + 4, 'JV_default_PCE', derivedData['JV_PCE'])
    compleatData.insert(tempIndex + 5, 'JV_default_Voc_scan_direction', derivedData['JV_Voc_scanDirection'])
    compleatData.insert(tempIndex + 6, 'JV_default_Jsc_scan_direction', derivedData['JV_Jsc_scanDirection'])
    compleatData.insert(tempIndex + 7, 'JV_default_FF_scan_direction', derivedData['JV_FF_scanDirection'])
    compleatData.insert(tempIndex + 8, 'JV_default_PCE_scan_direction', derivedData['JV_PCE_scanDirection'])
    compleatData.insert(tempIndex + 9, 'JV_hysteresis_index', derivedData['HysteresisIndex'])

    return compleatData
