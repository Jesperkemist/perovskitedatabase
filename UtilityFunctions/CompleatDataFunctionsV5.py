# =============================================================================
# CompleatDataFunctions
# functions used for compleating user data
# 
# Jesper Jacobsson
# 2019 11
# =============================================================================

#%%
import os
from functools import reduce
from itertools import zip_longest
#import operator

import numpy as np
import pandas as pd
#import re


def defaultFF(userData):
    ''' Determin the default FF to plot. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan'''
    FF = []
    flag = []

    for i in range(len(userData)): 
        try:
            if np.isnan(userData['JV_reverse_scan_FF'][i]) == False:
                FF.append(userData['JV_reverse_scan_FF'][i])
                flag.append('Reversed')
            elif np.isnan(userData['JV_forward_scan_FF'][i]) == False:
                FF.append(userData['JV_forward_scan_FF'][i])
                flag.append('Forward')
            else:
                FF.append(np.nan)
                flag.append(np.nan)
        except:
            FF.append(np.nan)
            flag.append(np.nan)

    return FF, flag

def defaultJsc(userData):
    ''' Determin the default Jsc to plot. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan'''
    Jsc = []
    flag = []

    for i in range(len(userData)):       
        # Check if the data template is of a version with stabilised values
        try:
            if np.isnan(userData['JV_reverse_scan_Jsc'][i]) == False:
                Jsc.append(userData['JV_reverse_scan_Jsc'][i])
                flag.append('Reversed')
            elif np.isnan(userData['JV_forward_scan_Jsc'][i]) == False:
                Jsc.append(userData['JV_forward_scan_Jsc'][i])
                flag.append('Forward')
            else:
                Jsc.append(np.nan)
                flag.append(np.nan)
        except:
            Jsc.append(np.nan)
            flag.append(np.nan)
        
    return Jsc, flag

def defaultVoc(userData):
    ''' Determin the default Voc to plot. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan'''
    Voc = []
    flag = []

    for i in range(len(userData)):       
        # Check if the data template is of a version with stabilised values
        try:
            if np.isnan(userData['JV_reverse_scan_Voc'][i]) == False:
                Voc.append(userData['JV_reverse_scan_Voc'][i])
                flag.append('Reversed')
            elif np.isnan(userData['JV_forward_scan_Voc'][i]) == False:
                Voc.append(userData['JV_forward_scan_Voc'][i])
                flag.append('Forward')
            else:
                Voc.append(np.nan)
                flag.append(np.nan)
        except:
            Voc.append(np.nan)
            flag.append(np.nan)
        
    return Voc, flag

def defaultPCE(userData):
    ''' Determin the default PCE to plot. Chose the first value that excist of: stabilised valuses from mpp, reversed scan and lastly the forward scan'''
    PCE = []
    flag = []

    for i in range(len(userData)):       
        # Check if the data template is of a version with stabilised values
        try:
            if np.isnan(userData['Stabilised_performance_PCE'][i]) == False:
                PCE.append(userData['Stabilised_performance_PCE'][i])
                flag.append('Stabilised')
            elif np.isnan(userData['JV_reverse_scan_PCE'][i]) == False:
                PCE.append(userData['JV_reverse_scan_PCE'][i])
                flag.append('Reversed')
            elif np.isnan(userData['JV_forward_scan_PCE'][i]) == False:
                PCE.append(userData['JV_forward_scan_PCE'][i])
                flag.append('Forward')
            else:
                PCE.append(np.nan)
                flag.append(np.nan)
        except:
            PCE.append(np.nan)
            flag.append(np.nan)
        
    return PCE, flag

def hysteresisIndex(userData):
    '''Calculate the hysteresis index
    '''
    hysteresis = []
    
    for i in range(len(userData)):
        datatemp = []
        # Gather the IV-data
        try:
            datatemp.append(userData['JV_forward_scan_Voc'][i])
            datatemp.append(userData['JV_reverse_scan_Voc'][i])
            datatemp.append(userData['JV_forward_scan_Jsc'][i])
            datatemp.append(userData['JV_reverse_scan_Jsc'][i])
            datatemp.append(userData['JV_forward_scan_FF'][i])
            datatemp.append(userData['JV_reverse_scan_FF'][i])
            datatemp.append(userData['JV_forward_scan_PCE'][i])
            datatemp.append(userData['JV_reverse_scan_PCE'][i])

            # If not enough data to calculat the hysteresis
            if np.isnan(datatemp).any() or 0 in datatemp:
                hysteresis.append(np.nan)

            # Calcualte the rations for all parameters between the forward and the revers scan
            else:
                fractions = []
                fractions.append(userData['JV_forward_scan_Voc'][i]/userData['JV_reverse_scan_Voc'][i])
                fractions.append(userData['JV_forward_scan_Jsc'][i]/userData['JV_reverse_scan_Jsc'][i])
                fractions.append(userData['JV_forward_scan_FF'][i]/userData['JV_reverse_scan_FF'][i])
                fractions.append(userData['JV_forward_scan_PCE'][i]/userData['JV_reverse_scan_PCE'][i])

                # Enfores that all the elements in the fractions are above 1. i.e. in the form biggest/smallest
                for i, item in enumerate(fractions):
                    if item < 1:
                     fractions[i] = 1/item

                # Calculate a proxy for the hysteresis
                hysteresis.append(np.cumprod(np.array(fractions))[-1] - 1)
        except:
            print(f'Failed to derrive the hysteresis index on row {i}')
            hysteresis.append(np.nan)

    return hysteresis

def isLeadFree(userData):
    '''Return true every perovskite not containing lead (Pb) '''
    leadFree = []

    for compound in userData:
        if 'Pb' in compound:
            leadFree.append(False)
        else:
            leadFree.append(True)

    return leadFree

def perovskiteShortComp(userData):
    ''' Derive the perovskite short composition'''

    A_site = userData['Perovskite_composition_a_ions']
    B_site = userData['Perovskite_composition_b_ions']
    C_site = userData['Perovskite_composition_c_ions']
    numberOfSamples = len(userData)

    shortComposition = []
    for i in range(numberOfSamples):
        try:
            # Split on | (in case there are several perovskite layers)
            A_split = A_site[i].split('|')
            B_split = B_site[i].split('|')
            C_split = C_site[i].split('|')

            # For each perovskite layer
            layers = []
            for j in range(len(A_split)):
                layer = perovskiteShortCompElements(A_split[j], B_split[j], C_split[j])
                # Remove blank spaces
                layer =  layer.strip().replace(" ","")
                layers.append(layer)

            # Merge the formated layers
            stack = ' | '.join(layers)

            # Append the result
            shortComposition.append(stack)
        except:
            print(f'Faild to extract perovskite short composition on row {i}')
            shortComposition.append('')


    return shortComposition

def perovskiteShortCompElements(A_site, B_site, C_site):
    '''Takes text strings of ions separated by ' ;' and return the perovskite short composition '''
    
    # Split the text strings 
    a_list = A_site.split('; ')
    b_list = B_site.split('; ')
    c_list = C_site.split('; ')

    # Sort the lists
    a_list.sort()
    b_list.sort()
    c_list.sort()

    # Merge the lists
    shortCompList = a_list + b_list + c_list

    # Concatenate the ions
    shortComp = ''.join(shortCompList)

    return shortComp

def perovskiteLongComp(userData):
    ''' Derive the perovskite long composition'''

    A_site = userData['Perovskite_composition_a_ions']
    B_site = userData['Perovskite_composition_b_ions']
    C_site = userData['Perovskite_composition_c_ions']
    A_kof = userData['Perovskite_composition_a_ions_coefficients']
    B_kof = userData['Perovskite_composition_b_ions_coefficients']
    C_kof = userData['Perovskite_composition_c_ions_coefficients']

    numberOfSamples = len(userData)

    LongComposition = []
    for i in range(numberOfSamples):
        try:
            # Split on | (in case there are several perovskite layers)
            A_split = A_site[i].split('|')
            B_split = B_site[i].split('|')
            C_split = C_site[i].split('|')
            A_kof_split = A_kof[i].split('|')
            B_kof_split = B_kof[i].split('|') 
            C_kof_split = C_kof[i].split('|') 

            # For each perovskite layer
            layers = []
            for j in range(len(A_split)):
                layer = perovskiteLongCompElements(A_split[j], B_split[j], C_split[j], A_kof_split[j], B_kof_split[j], C_kof_split[j])
                # Remove blank spaces
                layer =  layer.strip().replace(" ","")
                layers.append(layer)

            # Merge the formated layers
            stack = ' | '.join(layers)

            # Append the result
            LongComposition.append(stack)
        except:
            print(f'Faild to extract perovskite long composition on row {i}')
            LongComposition.append('')


    return LongComposition

def perovskiteLongCompElements(A_site, B_site, C_site, A_kof, B_kof, C_kof):
    '''Takes text strings of ions separated by ' ;' and return the perovskite short composition '''
    
    # Split the text strings 
    a_list = A_site.split('; ')
    b_list = B_site.split('; ')
    c_list = C_site.split('; ')
    a_kof_list = A_kof.split('; ')
    b_kof_list = B_kof.split('; ')
    c_kof_list = C_kof.split('; ')

    # Replace ones with enpty strings
    a_kof_list = ['' if x in [' 1', '1', '1 '] else x for x in a_kof_list]
    b_kof_list = ['' if x in [' 1', '1', '1 '] else x for x in b_kof_list]
    c_kof_list = ['' if x in [' 1', '1', '1 '] else x for x in c_kof_list]

    # Zip together the lists
    a_compleat = list(zip_longest(a_list, a_kof_list, fillvalue = ''))
    b_compleat = list(zip_longest(b_list, b_kof_list, fillvalue = ''))
    c_compleat = list(zip_longest(c_list, c_kof_list, fillvalue = ''))

    # Flatten the list of tuples generated by hte zip function
    a_compleat = [item for sublist in a_compleat for item in sublist]
    b_compleat = [item for sublist in b_compleat for item in sublist]
    c_compleat = [item for sublist in c_compleat for item in sublist]

    # Merge the lists
    LongCompList = a_compleat + b_compleat + c_compleat

    # Concatenate the ions
    LongComp = ''.join(LongCompList)

    return LongComp





# only used in V4
def bandgapComplemetation(bandgap, preovskite, defaultBandgaps):
    '''Check if hte band gap is given. If not, provide default values for the most common compositions 
    returns a list of bandgaps and a list indicating if they have been estimated from the composition or not'''

    newBandgap = []
    estimatedfromComposition = []

    for i in range(len(bandgap)):
        # If the band gap is as a number, use that number
        if isFloat(bandgap[i]):
            # If the number is a nan, se if there is a defaul value for the composition
            if np.isnan(float(bandgap[i])):
                if preovskite[i] in defaultBandgaps:
                    newBandgap.append(defaultBandgaps[preovskite[i]])
                    estimatedfromComposition.append(True)
                else:
                    newBandgap.append(np.nan)
                    estimatedfromComposition.append(False)
            else:
                newBandgap.append(float(bandgap[i]))
                estimatedfromComposition.append(False)

        # If there is a default band gap for that composition
        elif preovskite[i] in defaultBandgaps:
            newBandgap.append(defaultBandgaps[preovskite[i]])
            estimatedfromComposition.append(True)

        else:
            newBandgap.append(np.nan)
            estimatedfromComposition.append(False)

    return newBandgap, estimatedfromComposition

def cellAria(userData, defaultArea):
    '''Set a default cell area when it is missing'''
    newCellArea = []
    for area in userData:
        if isFloat(area):
            if np.isnan(area):
                newCellArea.append(defaultArea)
            else:
                newCellArea.append(area)
        else:
            newCellArea.append(defaultArea)

    return newCellArea

def coeficients(ionsInCompound, componentList):
    '''ionCoeficients a list of the numberical indices for each ionsInCompound that excist in componentList
    The fucntion will only work coreclty if the cemical formula is written without parantesises'''
    ionCoeficients = []
    
    for ion in ionsInCompound:
        indexOfIon = componentList.index(ion)

        # If this is the last position in the componentList we know a number will not follow and the coficient will be 1
        if indexOfIon >= len(componentList) - 1:
            ionCoeficients.append(1)
        
        # If there is a number following the ion
        elif isFloat(componentList[indexOfIon + 1]):
            ionCoeficients.append(componentList[indexOfIon + 1])

        # If the ion not is followed by a number, the coefficient will be 1
        else:
            ionCoeficients.append(1)
                    
    return ionCoeficients
      
def extractIons_Asite(userData, ionsToCheckFor):
    ''' Extract the ions specified in the list "ions" that are in each element of userData''' 
    ionList_level_1 = []
    for perovskiteEntry in userData:

        # Split on |
        perovskites = perovskiteEntry.split('|')

        ionList_level_2 = []
        # Loop over all perovskite layers in the stack
        for perovskite in perovskites:
            ionList_level_3 = []
            ## Take care of exeptions and corner cases
            #if perovskite == 'SrTiO3':
            #    ionList_level_3 = ['Sr']
            #    ionList_level_2.append(ionList_level_3)       
            #    continue
            #if perovskite == 'Cu3BiI6':
            #    ionList_level_3 = ['Cu']
            #    ionList_level_2.append(ionList_level_3)       
            #    continue

            # The default standard case
            for ion in ionsToCheckFor:    
                if ion in perovskite:
                    ionList_level_3.append(ion)
            
            # Sort ions in alphabetical order
            ionList_level_3.sort()
            ionList_level_3 = '; '.join(ionList_level_3)

            ionList_level_2.append(ionList_level_3)  
            
        ionList_level_2 = ' | '.join(ionList_level_2)
        ionList_level_1.append(ionList_level_2)

    return ionList_level_1

def extractIons_Bsite(userData, ionsToCheckFor):
    ''' Extract the ions specified in the list "ions" that are in each element of userData''' 
    ionList_level_1 = []
    for perovskiteEntry in userData:

        # Split on |
        perovskites = perovskiteEntry.split('|')

        ionList_level_2 = []
        # Loop over all perovskite layers in the stack
        for perovskite in perovskites:
            ionList_level_3 = []
            ## Take care of exeptions and corner cases
            #if perovskite == 'SrTiO3':
            #    ionList_level_3 = ['Ti']
            #    ionList_level_2.append(ionList_level_3)       
            #    continue
            #if perovskite == 'Cu3BiI6':
            #    ionList_level_3 = ['Bi']
            #    ionList_level_2.append(ionList_level_3)       
            #    continue

            # The default standard case
            for ion in ionsToCheckFor:    
                if ion in perovskite:
                    ionList_level_3.append(ion)
            
            # Sort ions in alphabetical order
            ionList_level_3.sort()
            ionList_level_3 = '; '.join(ionList_level_3)

            ionList_level_2.append(ionList_level_3)  
            
        ionList_level_2 = ' | '.join(ionList_level_2)
        ionList_level_1.append(ionList_level_2)
        #    ionList_level_3.sort()

        #    ionList_level_2.append(ionList_level_3)       
        #ionList_level_1.append(ionList_level_2)

    return ionList_level_1

def extractIons_Csite(userData, ionsToCheckFor):
    ''' Extract the ions specified in the list "ions" that are in each element of userData''' 
    ionList_level_1 = []
    for perovskiteEntry in userData:

        # Split on |
        perovskites = perovskiteEntry.split('|')

        ionList_level_2 = []
        # Loop over all perovskite layers in the stack
        for perovskite in perovskites:
            ionList_level_3 = []
            # Take care of exeptions and corner cases
            #if perovskite == 'SrTiO3':
            #    ionList_level_3 = ['O']
            #    ionList_level_2.append(ionList_level_3)       
            #    continue
            #if perovskite == 'Cu3BiI6':
            #    ionList_level_3 = ['I']
            #    ionList_level_2.append(ionList_level_3)       
            #    continue

            # The default standard case
            for ion in ionsToCheckFor:    
                if ion in perovskite:
                    ionList_level_3.append(ion)
            
            # Sort ions in alphabetical order
            ionList_level_3.sort()
            ionList_level_3 = '; '.join(ionList_level_3)

            ionList_level_2.append(ionList_level_3)  
            
        ionList_level_2 = ' | '.join(ionList_level_2)
        ionList_level_1.append(ionList_level_2)

    return ionList_level_1

def isInorganic(perovskite, organicIons):
    '''Check if the perovksite contain any organic ions. If not return True to indicate an Inorganic perovskite '''
    inorganic = []

    for compound in perovskite:
        flag = True
        # If we find an organic ion in the compound, change the flag to false to indicate organic perovskite
        for ion in organicIons:
            if ion in compound:
                flag = False

        inorganic.append(flag)

    return inorganic

def perovskiteShortCompOld(A_site, B_site, C_site, composition):
    ''' Derive the perovskite short composition'''
    shortComposition = []

    for i in range(len(A_site)):
        # If a single layered perovskite
        if '|' not in composition[i]:
        # Take care of exeptions and corner cases
            if composition[i] == 'CsAg2Sb2I9':
                shortComposition.append('CsAgSbI')
                continue
            elif composition[i] == 'Bi2FeCrO6':
                shortComposition.append('BiFeCrO')
                continue

            # The standard case
            shortComposition.append(''.join(sorted(A_site[i][0]) + sorted(B_site[i][0]) + sorted(C_site[i][0])))

        else:
            # Split on |
            composition_list = composition[i].split('|')

            short_comp_list = []
            for j, element in enumerate(composition_list):
                # Remove leading and tailing blank spaces
                element = element.strip()
                
                # Take care of exeptions and corner cases
                if composition[i] == 'CsAg2Sb2I9':
                    short_comp_list.append('CsAgSbI')
                    continue
                
                # The standard case
                short_comp_list.append(''.join(sorted(A_site[i][j]) + sorted(B_site[i][j]) + sorted(C_site[i][j])))

            shortComposition.append(" | ".join(short_comp_list))

    return shortComposition

def perovskiteIonFractions(perovskites, allPosiblePerovsktieIons, ionsToCheckFor):
    '''Return a list of a list of fractions of the ionsToCheckFor for the asicate site '''
    # A regular expression for splitting the string in ions and numbers
    expression = allPosiblePerovsktieIons + '|\d+\.\d+' + '|\d+'
    
    expression = expression.replace("(","\(")
    expression = expression.replace(")","\)")

    fractions = []

    # For every row (which most ofthen is one perovskite composition, but could also be two separated by a |)
    for i, row in enumerate(perovskites):
        
        try:
            # Split on |
            compounds = row.split('|')
        
            # For every perovskite in the row (most often 1 if not a layered structure)
            fractionList_level_2 = []
            compund_foeficients = []
            for compound in compounds:
                # split the composition string into a list of ions and numbers
                componentList = re.findall(expression, compound)
            
                # Check which ions that are in the compound
                ionsInCompound = ionExctraction(ionsToCheckFor, componentList)
        
                # Calculate the coeficients of the ions with respect to the ions on that site
                kof = coeficients(ionsInCompound, componentList)

                # Convert numbers to strings
                for j, koeficient in enumerate(kof):
                    kof[j] = str(koeficient)

                ## Normalise the numbers in coeficients
                #normalisedCoeficients = normalise(kof)

                #fractionList_level_2.append(normalisedCoeficients)
                kofstring = '; '.join(kof)
                compund_foeficients.append(kofstring)

            fractionList_level_2 = ' | '.join(compund_foeficients)

    
            fractions.append(fractionList_level_2)
        except:
            fractions.append('')
            print(f'Fail to derive the ion fractions for {row} on row {i}')

    return fractions

def removeParantesises(perovskite):
    '''Remove parantesises from the perovskites'''
    formatedPerovskite = []
    for item in perovskite:
        # Ensure that input is formated a a string
        item = str(item)

        # Remove starting and ending blank spaces
        item = item.strip()

        # Split on |
        itemList = item.split('|')

        for element in itemList:
            # Remove leading and tailing blank spaces
            element = element.strip()

            #############################
            # Do hevy lifting with paranthesis removal
            #############################

        # Concatenate all parts with proper spacing
        item = " | ".join(itemList)


        formatedPerovskite.append(item)

    return formatedPerovskite


# Old functions
def ionExctraction(ionsToCheckFor, perovskite):
    '''Check whihc ions defind in "site" that is in "perovksite" '''
    ions = []
    for ion in ionsToCheckFor:
        if ion in perovskite:
            ions.append(ion)                 
    return ions






