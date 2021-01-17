# =============================================================================
# CleanDataFunctions
# functions used for clening user data
# 
# Jesper Jacobsson
# 2020 05
# =============================================================================

#%%
import os
import numpy as np
import pandas as pd
from datetime import datetime

def ageingIsoProtocoll(userData):
    ''' Return the text string for the ISO protocoll'''
    protocoll = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Replace 'nan' with emty string
            if item.lower() == 'nan':
                item = ''
                
            # Remove starting and ending blank spaces
            item = item.strip()

            # Remove starting and ending blank spaces
            item = item.strip()

            protocoll.append(item)
        except:
            print(f'faild to ageingIsoProtocoll of {item} on row {i}')
            protocoll.append(item)

    return protocoll

def ageingLightSource(userData):
    ''' Return the text string for the ISO protocoll'''
    protocoll = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Replace 'nan' with emty string
            if item.lower() == 'nan':
                item = ''
        
            # Remove starting and ending blank spaces
            item = item.strip()

            # Remove starting and ending blank spaces
            item = item.strip()

            protocoll.append(item)
        except:
            print(f'faild to extract ageingLightSource of {item} on row {i}')
            protocoll.append(item)

    return protocoll

def ageingLoadCondition(userData):
    ''' Return the text string for the ISO protocoll'''
    protocoll = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Replace 'nan' with emty string
            if item.lower() == 'nan':
                item = ''

            # Remove starting and ending blank spaces
            item = item.strip()

            # Go through all known formating variations and convert them to the corect one
            if item.lower() in ['mpp']:
                item = 'MPP' 
            elif item.lower() in ['false']:
                item = False

            protocoll.append(item)
        except:
            print(f'faild to extract ageingLoadCondition of {item} on row {i}')
            protocoll.append(item)

    return protocoll

def aggregationStates(userData):
    '''Format the agregtion stat list'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several gases in the solution separted by ;

    stateList = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Enfors the notation of lists rather than that of mixing
            item = item.replace(':', ';')   

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    states = depositionStep.split(';')

                    for k, state in enumerate(states):
                        # Enforse proper formating
                        states[k] = aggregationStatesFormating(state)

                    depositionSteps[j] = '; '.join(states)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            stateList.append(item)

        except:
            print(f'faild to extract aggregationStates of {item} on row {i}')
            stateList.append(item)

    return stateList

def aggregationStatesFormating(state):
    '''Format the textstring describing the precursor state'''
 
    # Remove starting and ending blank spaces
    state = state.strip()

    # Go through all known formating variations and convert them to the corect one 
    if state.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        formatedState = 'Unknown'
    elif state.lower() in ['solid']:
        formatedState = 'Solid'   
    elif state.lower() in ['solution', 'solutionn', 'soultion', 'solutions', 'liquid']:
        formatedState = 'Liquid' 
    elif state.lower() in ['gas', 'vapor', 'vapour']:
        formatedState = 'Gas'
    else:
        formatedState = 'Unknown'

    return formatedState

def architecture(userData):
    '''Return a list of formated strings for the architecture'''
    architecture = []
    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove starting and ending blank spaces
            item = item.strip()

            #There are a few main types of acrcitercures
            if item.lower() in ['nip', 'n-i-p']:
                architecture.append('nip')
            elif item.lower() in ['pin', 'p-i-n']:
                architecture.append('pin')
            elif item.lower() in ['back contacted', 'backcontacted']:
                architecture.append('Back contacted')
            elif item.lower() in ['front contacted', 'frontcontacted']:
                architecture.append('Front contacted')
            elif item.lower() in ['schottky']:
                architecture.append('Schottky')
            elif item.lower() in  ['', 'unknown', 'nan', 'na', '-', 'np.nan']:
                architecture.append('Unknown')

            # If non of the default, add what is given in title case
            else:
                architecture.append(item.title())
        except:
            print(f'faild to extract architecture of {item} on row {i}')
            architecture.append('Unknown')

    return architecture

def atmosphere(userData):
    '''Format the string describing the atmosphere'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several gases in the solution separted by ;

    environment = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    gases = depositionStep.split(';')

                    for k, gas in enumerate(gases):
                        # Enforse proper formating
                        gases[k] = atmosphereFormating(gas)

                    depositionSteps[j] = '; '.join(gases)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            environment.append(item)

        except:
            print(f'faild to extract atmosphere of {item} on row {i}')
            environment.append(item)

    return environment

def atmosphereFormating(atmosphere):
    ''' Check atmosphere againast known formating variations 
    and return the standard formating for the atmosphere '''

    # Remove starting and ending blank spaces
    atmosphere = atmosphere.strip()

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in atmosphereFormating')
  
    elif atmosphere.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        formatedAtmosphere = 'Unknown'

    elif atmosphere.lower() in ['air']:
        formatedAtmosphere = 'Air'
    elif atmosphere.lower() in ['ambient', 'anbient atmosphere', 'ambient atmosphere', 'ambient air', 'ambient environment']:
        formatedAtmosphere = 'Ambient'
    elif atmosphere.lower() in ['argon', 'ar']:
        formatedAtmosphere = 'Ar'
    elif atmosphere.lower() in ['dry air', 'drybox', 'dry box']:
        formatedAtmosphere = 'Dry air'
    elif atmosphere.lower() in ['inert']:
        formatedAtmosphere = 'Inert'
    elif atmosphere.lower() in ['glovebox', 'glove box']:
        formatedAtmosphere = 'Glovebox'
    elif atmosphere.lower() in ['ma', 'methylamin']:
        formatedAtmosphere = 'Methylamin'
    elif atmosphere.lower() in ['n2', 'nitrogen']:
        formatedAtmosphere = 'N2'
    elif atmosphere.lower() in ['vacuum', 'vacum', 'vaccum']:
        formatedAtmosphere = 'Vacuum'

    # If no known formating variations
    else: 
        formatedAtmosphere = atmosphere

    return formatedAtmosphere

def averageOverNumberOfCells(userData):
    '''Convert values to int or 1 for missing values.'''
    values = []
    for item in userData:
        # To make it simple, the imput is converted to a string (regardless if it is or not)
        item = str(item)

        # Remove all blank spaces
        item = item.strip().replace(" ","")

        # Enfors the use of decimal point
        item = item.replace(',', '.')

        # If given corectly as a float
        if is_number(item):
            # in the special case of nan-values
            if np.isnan(float(item)):
                values.append(1)
            # cast the value as an int    
            else:
                values.append(int(float(item)))

        # If not given corectly or missing, set value as 1
        else:
            values.append(1)

    return values

def chemicalsFormating(chemical):
    ''' Check cemicals in solution againast known formating variations 
    and return the standard formating for the chemcial'''

    # Remove leading and tailing blank spaces
    chemical = chemical.strip()

    # If not stated
    if chemical.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'nan'

    # TODO. Fill upp with common formating variations to be corected for

    return chemical

def certificationIstitute(userData):
    '''Format the string describing the certification institute'''
    institute = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            if item.lower() == 'nan':
                item = ''
            elif item.lower() in ['nrel,usa']:
                item = 'NREL'

            institute.append(item)
        except:
            print(f'faild to extract CertificationIstitute of {item} on row {i}')
            institute.append(item)

    return institute

def coefficientsFormating(coefficient):
    '''Format the coefficient '''

    # Remove all blank spaces
    coefficient = coefficient.replace(' ','')

    # Separate out the number from the unit (which should not be there)
    number, unit = stringToNumberAndUnit(coefficient)

    # If not stated
    if coefficient.lower() in  ['unknown', 'x']:
        return 'x'
    elif coefficient.lower() in ['','non', 'none', 'nan', 'na', '-', 'np.nan']:
        return ''

    # If the coefficient corectly is given as a number
    elif len(number) == len(coefficient):
        coefficient =  number
    else:
        coefficient = 'x'

    return coefficient

def compounds(userData):
    '''Format the composition of solutions'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several compounds in the solution separted by ;

    chemicals = []
    for item in userData:
        try:
            # Enforce input is a string 
            item = str(item)   

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    compounds = depositionStep.split(';')

                    for k, compound in enumerate(compounds):
                        # Enforse proper formating
                        compounds[k] = chemicalsFormating(compound)

                    depositionSteps[j] = '; '.join(compounds)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            chemicals.append(item)
        except:
            chemicals.append('')
            print(f'Cound not read in compounds on line: {i}')

    return chemicals

def concentrations(userData):
    '''Format the concentrations'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several compounds in the solution separted by ;

    amounts = []
    for item in userData:
        try:
            # Enforce input is a string 
            item = str(item)   

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    compounds = depositionStep.split(';')

                    for k, compound in enumerate(compounds):
                        # Enforse proper formating
                        compounds[k] = concentrationFormating(compound)

                    depositionSteps[j] = '; '.join(compounds)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            amounts.append(item)
        except:
            amounts.append('')
            print(f'Cound not read in concentrations on line: {i}')

    return amounts

def concentrationFormating(compound):
    ''' Check concentrations againast known formating variations 
    and return the standard formating for the concentration'''

    # Remove all blank spaces
    compound = compound.replace(' ','')

    # If not stated
    if compound.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'nan'

    # Separate out the number from the unit
    number, unit = stringToNumberAndUnit(compound)
  
    # If there is no unit, retun the number as it is
    if len(number) == len(compound):
        return number
    
    # If there is a unit, Format the units with respect to known formating variations
    if unit.lower() in ['wt%', 'weight%', 'wt %', 'mass%', 'mass %']:
        unit = 'wt%'
    elif unit.lower() in ['v%', 'vol%', 'v/v', 'v/v%']:
        unit = 'vol%'
    elif unit.lower() in ['ppt', 'pph']:
        unit = 'ppt'
    elif unit.lower() in ['ppm']:
        unit = 'ppm'
    elif unit.lower() in ['ppb']:
        unit = 'ppb'
    elif unit.lower() in ['M', 'mol/dm3', 'moldm-3', 'mol/dm^3', 'moldm^-3']:
        unit = 'M'
    elif unit.lower() in ['mM', 'mmol/dm3', 'mmoldm-3', 'mmol/dm^3', 'mmoldm^-3', 'mmol L-1']:
        unit = 'mM'
    elif unit.lower() in ['mol%', 'mol %', '%mol', '% mol']:
        unit = 'mol%'
    elif unit.lower() in ['molal']:
        unit = 'molal'
    elif unit.lower() in ['g/ml', 'gml-1', 'gml^-1', 'g/cm^3', 'gcm-3', 'g/cm^3', 'gcm^-3']:
        unit = 'g/ml'
    elif unit.lower() in ['mg/ml', 'mgml-1', 'mgml^-1', 'mg/cm^3', 'mgcm-3', 'mg/cm^3', 'mgcm^-3', 'mg ml-1']:
        unit = 'mg/ml'
    elif unit.lower() in ['µg/ml', 'µgml-1', 'µgml^-1', 'µg/cm^3', 'µgcm-3', 'µg/cm^3', 'µgcm^-3']:
        unit = 'µg/ml'
    else:
        unit = unit.strip()

    # Concatenate the number and the unit
    compound = ' '.join([number, unit])

    return compound

def convertToDateTime(item):
    # To make it simple, the imput is converted to a string (regardless if it is or not)
    item = str(item)

    # Remove starting and ending blank spaces
    item = item.strip()

    # convert to a date
    item = pd.to_datetime(item)
    item = datetime.date(item)

    return item

def convertToFloat(item):
    # To make it simple, the imput is converted to a string (regardless if it is or not)
    item = str(item)

    # Remove all blank spaces
    item = item.strip().replace(" ","")

    # Enfors the use of decimal point
    item = item.replace(',', '.')

    # If given corectly as a float
    if is_number(item):
        return float(item)

    # If not given corectly or missing, set value as empty
    else:
        return np.nan

def convertToString(userData):
    '''Convert all entries to strings'''
    newStrings = []
    for item in userData:
        # Enforce that input is a string 
        item = str(item)

        # Remove leading and tailing blank spaces
        item = item.strip()

        # Replace nan with emty string
        if item.lower() in ['nan', 'non', 'none', '', 'na', '-']:
            item = ''
        elif item.lower() in ['unknown']:
            item = 'Unknown'
        
        newStrings.append(item)

    return newStrings

def dataColumnFormating(columnNames):
    ''' Format the column names. remove new line characters 
    and corect for miss spellings and inconsistecies in various template versions. 
    Returns a list of formated column names'''

    newNames = []
    for item in columnNames:
        # Remove new lines characters
        item = item.replace('\n', ' ')

        # Remove dubbel spaces
        item = item.replace('  ', ' ')

        # Remove initial and ending blank spaces
        item = item.strip()

        # Corect some miss spelings
        if item == 'Cell area [cm^2] (active masured area)':
            item = 'Cell area [cm^2] (active measured area)'
        elif item == 'Certification Institute':
            item = 'Certification Istitute'
        elif item == 'Voc [V] (reverse scan)':
            item = 'Voc [V] (reverce scan)'
        elif item == 'Jsc [mA/cm^2] (reverse scan)':
            item = 'Jsc [mA/cm^2] (reverce scan)'
        elif item == 'Jsc [mA/cm^2] (reverse scan)':
            item = 'Jsc [mA/cm^2] (reverce scan)'
        elif item == 'PCE [%] (reverse scan)':
            item = 'PCE [%] (reverce scan)'
        elif item == 'Perovskite. Dimension. 1D (Quantum dot) [TRUE/FALSE]':
            item = 'Perovskite. Dimension. 0D (Quantum dot) [TRUE/FALSE]'
        elif item == 'Add. Lay. Backcontact side [TRUE/FALSE]':
            item = 'Add. Lay. Backside [TRUE/FALSE]'
        elif item == 'Add. Lay. Backcontact side. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]':
            item = 'Add. Lay. Backside. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]'
        elif item == 'Add. Lay. Backcontact side. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]':
            item = 'Add. Lay. Backside. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'
        elif item == 'Add. Lay. Backcontact side. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]':
            item = 'Add. Lay. Backside. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]'

        # Change frontside to front and backside to back
        item = item.replace('Frontside', 'Front')
        item = item.replace('Backside', 'Back')

        newNames.append(item)

    return newNames

def dateTime(userData):
    '''Format date time to the format year:mm:dd:hh:mm'''
    data = []
    for item in userData:
        try:
             # Enforce that input is a string 
            item = str(item)

            # Remove starting en ending blank spaces
            item = item.strip()

            # Split on :
            timeBits = item.split(':')

            # Extract numbers of every part (in case ther are nun numerical signs given)
            for i, timeBit in enumerate(timeBits):
                timeBits[i], unit = stringToNumberAndUnit(timeBit)

            # Format the year
            if len(timeBits) > 0:
                # given corectly
                if len(timeBits[0]) == 4:
                    pass
                # Given as a two digit number. Asumes teh start data is after year 2000
                elif len(timeBits[0]) == 2:
                    timeBits[0] = ''.join(['20', timeBits[0]])
                else:
                    timeBits[0] = '0000'
            else:
                timeBits.append('0000')

            # format month
            if len(timeBits) > 1:
                if len(timeBits[1]) == 2 and float(timeBits[1]) < 13:
                    pass
                elif len(timeBits[1]) == 1:
                    timeBits[1] = ''.join(['0', timeBits[1]])
                else:
                    timeBits[1] = '00'
            else:
                timeBits.append('00')

            # format hour
            if len(timeBits) > 2:
                if len(timeBits[2]) == 2 and float(timeBits[2]) < 25:
                    pass
                elif len(timeBits[2]) == 1:
                    timeBits[2] = ''.join(['0', timeBits[2]])
                else:
                    timeBits[2] = '00'
            else:
                timeBits.append('00')

            # format min
            if len(timeBits) > 3:
                if len(timeBits[3]) == 2 and float(timeBits[3]) < 61:
                    pass
                elif len(timeBits[3]) == 1:
                    timeBits[3] = ''.join(['0', timeBits[3]])
                else:
                    timeBits[3] = '00'
            else:
                timeBits.append('00')

            # format sec
            if len(timeBits) > 4:
                if len(timeBits[4]) == 2 and float(timeBits[4]) < 61:
                    pass
                elif len(timeBits[4]) == 1:
                    timeBits[4] = ''.join(['0', timeBits[4]])
                else:
                    timeBits[4] = '00'
            else:
                timeBits.append('00')


            item = ':'.join(timeBits[0:5])

            data.append(item)

        except:
            print(f'faild to extract dateTime of {item} on row {i}')
            data.append('np.nan')
     
    return data

def depositionProcedure(userData):
    '''Format the deposition proceadure data'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    depositionList = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove starting en ending blank spaces
            item = item.strip()

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionProcedures = layer.split('>>')

                for j, depositionProcedure in enumerate(depositionProcedures):
                    # Enforse proper formating
                    depositionProcedures[j] = depositionProcedureFormating(depositionProcedure)
                
                # Concatenate additives for each layer with proper spacing
                layers[i] = " >> ".join(depositionProcedures)

            # Concatenate all parts with proper spacing
            item = " | ".join(layers)

            depositionList.append(item)
        except:
            print(f'faild to extract depositionProcedure of {item} on row {i}')
            depositionList.append(item)

    return depositionList

def depositionProcedureFormating(methode):
    ''' Check deposition proceadures againast known formating variations 
        and return the standard formating for the methode '''

    # Remove starting and ending blank spaces
    methode = methode.strip()

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in depositionProcedureFormating')

    elif methode.lower() in ['air brush', 'air brush spray', 'air brush spray-coating']:
        formatedMethode = 'Air brush spray'
    elif methode.lower() in ['ald', 'atomic layer deposition', 'peald', 'plasma enhanced ald']:
        formatedMethode = 'ALD' 

    elif methode.lower() in ['brush painting', 'brush-painting', 'brushing']:
        formatedMethode = 'Brush painting'

    elif methode.lower() in ['candle burning']:
        formatedMethode = 'Candle burning'
    elif methode.lower() in ['bath deposition', 'bath-deposition', 'cbd', 'chemical bath', 'chemical bath deposition', 'chemical bath depostion', 'chemical bath method', 'chemical deposition', 'chemical-bath']:
        formatedMethode = 'CBD' 
    elif methode.lower() in ['close-spaced sublimation', 'closed space sublimatio', 'closed space sublimation', 'css']:
        formatedMethode = 'Closed space sublimation' 
    elif methode.lower() in ['co evaporation', 'co-evaporation', 'coevaporation']:
        formatedMethode = 'Co-evaporation'
    elif methode.lower() in ['crystalisation']:
        formatedMethode = 'Crystalisation'
    elif methode.lower() in ['chemical vapor deposition', 'chemical vapour deposition', 'cvd', 'p-cvd']:
        formatedMethode = 'CVD' 
 
    elif methode.lower() in ['dc magnetron sputter', 'dc magnetron sputtering']:
        formatedMethode = 'DC Magnetron Sputtering' 
    elif methode.lower() in ['dc sputter', 'dc sputtering', 'dc-sputtering']:
        formatedMethode = 'DC Sputtering'         
    elif methode.lower() in ['dc reactive magnetron sputtering']:
        formatedMethode = 'DC Reactive Magnetron Sputtering' 
    elif methode.lower() in ['diffusion']:
        formatedMethode = 'Diffusion' 
    elif methode.lower() in ['diffusion gas reaction', 'diffusion-gas reaction']:
        formatedMethode = 'Diffusion-gas reaction'  
    elif methode.lower() in ['dip -coating', 'dip coating', 'dip-coating', 'dipcoating', 'diping', 'dipp coating', 'dipp-coating', 'dippcoating', 'dipping']:
        formatedMethode = 'Dipp-coating'     
    elif methode.lower() in ['bald coating', 'bald-coating', 'bar coating', 'bar-coating', 'blad coating', 'blad-coating', 'blade coated', 'blade coating', 'blade printing', 'blade-coating', 'bladecoating', 'blading coating', 'doctor blade', 'doctor blade-coating', 'doctor blade coating', 'doctor blading', 'doctor-blade', 'doctor-blade coating', 'doctor-blading', 'doctorblade', 'doctorblading']:
        formatedMethode = 'Doctor blading'
    elif methode.lower() in ['dop-infiltration', 'drop infiltration', 'drop-infiltration', 'dropinfiltration', 'dropp infiltration', 'dropp-infiltration', 'infiltrate']:
        formatedMethode = 'Drop-infiltration' 
    elif methode.lower() in ['drop casting', 'drop coating', 'drop-cast', 'drop-casting', 'drop-coating', 'dropcast', 'dropcasting', 'dropcoating', 'dropp coating']:
        formatedMethode = 'Dropcasting' 

    elif methode.lower() in ['e beam evaporation', 'e-beam', 'e-beam deposition', 'e-beam evaporation', 'ebeam evaporation', 'ebeam evporation', 'ebeam-evaporation', 'electro beam evaporation', 'electron beam deposition', 'electron beam evaporated', 'electron beam evaporation', 'electronbeam evaporation', 'reactive e-beam evaporation']:
        formatedMethode = 'E-beam evaporation'
    elif methode.lower() in ['electro-spray', 'electrospray', 'electrospray coating', 'electrospraying']:
        formatedMethode = 'Electrospraying'        
    elif methode.lower() in ['evaporate', 'evaporated', 'evaporatio', 'evaporation', 'thermal deposition', 'thermal evaporated', 'thermal evaporation', 'thermal vaporation', 'vaccum deposited', 'vacumn deposition', 'vacuum evaporation', 'vacuum thermal deposition']:
        formatedMethode = 'Evaporation'
    elif methode.lower() in ['anodization', 'electrochemical anodization', 'potentiostatic anoidzation']:
        formatedMethode = 'Electrochemical anodization'
    elif methode.lower() in ['anodically electrodeposition', 'ecd', 'electro deposition', 'electrocdeposition', 'electrochemical', 'electrochemical deposition', 'electrodeposited', 'electrodeposition', 'electrophoretic deposition', 'electro-deposition']:
        formatedMethode = 'Electrodeposition'
    elif methode.lower() in ['electrochemical polymerisation', 'electrochemical polymerization', 'electropolymerization']:
        formatedMethode = 'Electropolymerization'
    elif methode.lower() in ['electrospinning', 'electro-spinning', 'electrostatic spinning']:
        formatedMethode = 'Electrospinning'

    elif methode.lower() in ['flash evaporation']:
        formatedMethode = 'Flash evaporation'

    elif methode.lower() in ['gelation']:
        formatedMethode = 'Gelation'
    elif methode.lower() in ['gas reaction', 'vasp']:
        formatedMethode = 'Gas reaction'
      
    elif methode.lower() in ['hot casting', 'hot-casting']:
        formatedMethode = 'Hot-casting'
    elif methode.lower() in ['hot pressed', 'hot-pressed']:
        formatedMethode = 'Hot-pressed'
    elif methode.lower() in ['hydrotherma', 'hydrothermal', 'hydrothermal deposition', 'hydrothermal growth', 'hydrothermal method', 'hydrothermal process', 'hydrothermal synthesis', 'hydrotrmal']:
        formatedMethode = 'Hydrothermal'

    elif methode.lower() in ['injet printing', 'inkjet printing', 'inkjet-printing']:
        formatedMethode = 'Inkjet printing'
    elif methode.lower() in ['ion exchange', 'ion-exchange']:
        formatedMethode = 'Ion exchange'
       
    elif methode.lower() in ['dry press-transfer', 'film transfer', 'film transfer lamination', 'laminating', 'lamination', 'transfer lamination technique', 'transfer printing', 'wrapping']:
        formatedMethode = 'Lamination'        
    elif methode.lower() in ['langmuir-blodgett deposition', 'langmuir-blodgett film deposition']:
        formatedMethode = 'Langmuir-Blodgett deposition'
    elif methode.lower() in ['layer by layer adsorption and reaction', 'lblar']:
        formatedMethode = 'LBLAR'

    elif methode.lower() in ['magneton sputtering', 'magnetron sputtering', 'magnetron-sputtering']:
        formatedMethode = 'Magnetron sputtering'

    elif methode.lower() in ['pld', 'pulsed laser deposition']:
        formatedMethode = 'Pulsed laser deposition'
    elif methode.lower() in ['pvd', 'ebpvd']:
        formatedMethode = 'PVD'

    elif methode.lower() in ['reactive sputtering']:
        formatedMethode = 'Reactive sputtering'
    elif methode.lower() in ['recrystalisation']:
        formatedMethode = 'Recrystalisation'
    elif methode.lower() in ['rf sputtering', 'rf-sputtering', 'rf magnetic sputtering']:
        formatedMethode = 'RF sputtering'
    elif methode.lower() in ['grooved roller coating', 'roll to roll microgravure printing', 'roller coating']:
        formatedMethode = 'Roller coating'
    elif methode.lower() in ['rfms', 'frequency magnetron sputteirng(fms)', 'radio-frequency magnetron sputtering', 'rf magneton sputtering', 'magnetron rf sputtering']:
        formatedMethode = 'RF Magnetron Sputtering' 
        
    elif methode.lower() in ['clamping', 'sandwich', 'sandwiched', 'sandwiching', 'sandwitched']:
        formatedMethode = 'Sandwiching'
    elif methode.lower() in ['screan printing', 'screan-printing', 'screanprinting', 'screen-printing', 'screen prinitng', 'screen-prining', 'screen-prinitng', 'screen-printed', 'screen printed', 'screen printing',  'screenprinting', 'screnprinting', 'silk-screen-printing', 'sreanprinting']:
        formatedMethode = 'Screen printing' 
    elif methode.lower() in ['silar']:
        formatedMethode = 'SILAR'
    elif methode.lower() in ['single crystal growth']:
        formatedMethode = 'Single crystal growth'
    elif methode.lower() in ['r2r slot-die coating', 'roll-to-roll slot-die coating', 'slot die', 'slot die coating', 'slot dye coating', 'slot-die coating', 'slot-dye coating', 'slotdie coating']:
        formatedMethode = 'Slot-die coating'
    elif methode.lower() in ['sol-gel', 'solgel']:
        formatedMethode = 'Sol-gel'
    elif methode.lower() in ['auto-clave', 'autoclave', 'microwave-assisted reaction', 'solvothermal', 'solvothermal growth']:
        formatedMethode = 'Solvothermal' 
    elif methode.lower() in ['space-limited inverse temperature crystallization']:
        formatedMethode = 'Space-limited inverse temperature crystallization'
    elif methode.lower() in ['spi-coating', 'spin -coating', 'spin casting', 'spin casted', 'spin coated', 'spin coating', 'spin coatng', 'spin-caoting', 'spin-caoting', 'spin-cast', 'spin-casting', 'spin-cating', 'spin-coated', 'spin-coatin', 'spin-coating', 'spin.coating', 'spincaoting', 'spincoaing', 'spincoating', 'sping coating', 'spun-coating']:
        formatedMethode = 'Spin-coating'
    elif methode.lower() in ['gun-spraying', 'spray', 'spray coating', 'spray depositing', 'spray deposition', 'spray-coating', 'spraycoating']:
        formatedMethode = 'Spray-coating' 
    elif methode.lower() in ['pray-pyrolysis', 'spary pyrolysis', 'spra-pyrolys', 'spray pirolisis', 'spray pirolysis', 'spray pyolysis', 'spray pyrilysis', 'spray pyrolisis', 'spray pyrolys', 'spray pyrolysis', 'spray-pyrolisis', 'spray-pyrolys', 'spray-pyrolysis', 'spraypyrolysis']:
        formatedMethode = 'Spray-pyrolys' 
    elif methode.lower() in ['springkling']:
        formatedMethode = 'Springkling' 
    elif methode.lower() in ['dputtering', 'ion beam sputtering', 'plasma sputtering', 'sputter', 'sputtered', 'sputtering']:
        formatedMethode = 'Sputtering' 

    elif methode.lower() in ['thermal oxidization']:
        formatedMethode = 'Thermal oxidation'

    elif methode.lower() in ['ultrasonic spray deposition', 'ultrasonic spray-coating']:
        formatedMethode = 'Ultrasonic spray' 
    elif methode.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        formatedMethode = 'Unknown'

    elif methode.lower() in ['vacuum flash evaporation']:
        formatedMethode = 'Vacuum flash evaporation' 
    elif methode.lower() in ['vacuum sublimation']:
        formatedMethode = 'Vacuum sublimation' 

    # If no known formating variations
    else: 
        formatedMethode = methode

    return formatedMethode

def depositionProcedureOld(userData):
    '''Format the deposition proceadure data'''
    deposition = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove starting en ending blank spaces
            item = item.strip()

            # Remove nan
            if item.lower() == 'nan':
                item = ''

            # If the first or the last character is a |
            if len(item) > 0:
                if item[0] == '|':
                    item = 'nan' + item
                if item[-1] == '|':
                    item = item + 'nan'

            # Split on |
            itemList = item.split('|')

            for i, depositionMethode in enumerate(itemList):
                # Remove blank spaces
                depositionMethode = depositionMethode.strip()

                # Capitalize the element (but keap upper case for solvents etc.)
                if len(depositionMethode) > 0:
                    depositionMethode = depositionMethode[0].upper() + depositionMethode[1:]

                # Enforse proper formating (based on the variations I have seen)
                itemList[i] = depositionProcedureFormating(depositionMethode)                

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            deposition.append(item)
        except:
            print(f'faild to extract depositionProcedure of {item} on row {i}')
            deposition.append(item)

    return deposition

def doiNumbers(userData):
    '''Return a list of formated strings for the DOI numbers'''
    DOI_list = []
    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove starting and ending blank spaces
            item = item.strip()

            #Remove link prefices
            item = item.replace('http://dx.doi.org/','')
            item = item.replace('https://dx.doi.org/','')
            item = item.replace('https://doi.org/','')
            item = item.replace('http://doi.org/','')
            item = item.replace('doi.org/','')
            item = item.replace('doi:','')

            DOI_list.append(item)

        except:
            print(f'faild to format DOI number: {item} on row {i}')
            DOI_list.append('')

    return DOI_list

def dopandsAndAdditives(userData):
    '''Format dopands and additives '''
    listOfAdditives = []
    for i, item in enumerate(userData):
        try:
            # Enforce input as a string 
            item = str(item)

            # Remove starting and ending blank spaces
            item = item.strip()

            # Split on |
            layers = item.split('|')

            for j, layer in enumerate(layers):
                # Split on ;
                dopands = layer.split(';')

                for k, dopand in enumerate(dopands):
                    # Enforse proper formating
                    dopands[k] = dopandsAndAdditivesFormating(dopand)
                
                # Concatenate additives for each layer with proper spacing
                layers[j] = "; ".join(dopands)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            listOfAdditives.append(item)
        except:
            listOfAdditives.append('')
            print(f'Cound not read in dopandsAndAdditives on line: {i}')

    return listOfAdditives

def dopandsAndAdditivesFormating(additive):
    ''' Check dopands and additives againast known formating variations 
    and return the standard formating for the additive '''

    # Remove starting and ending blank spaces
    additive = additive.strip()

    # In text replacements
    additive = additive.replace(" : ",":")
    additive = additive.replace(" :",":")
    additive = additive.replace(": ",":")

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in dopandsAndAdditivesFormating')
  
    elif additive.lower() in  ['', 'nan', 'na']:
        formatedAdditive = 'nan'

    elif additive.lower() in  ['unknown']:
        formatedAdditive = 'Unknown'

    elif additive.lower() in  ['non', 'none', 'undoped']:
        formatedAdditive = 'Undoped'

    elif additive.lower() in ['ascorbicacid']:
        formatedAdditive = 'Ascorbic acid'
    elif additive.lower() in ['phosphatidylcholine']:
        formatedAdditive = 'Phosphatidylcholine'

    elif additive.lower() in ['4-tert-butylpyridine','tbp', 't-bp']:
        formatedAdditive = 'TBP'
    elif additive.lower() in ["litfsi","li-tfsi"]:
        formatedAdditive = 'Li-TFSI'


    # If no known formating variations
    else: 
        formatedAdditive = additive

    return formatedAdditive

def dopandsAndAdditivesOld(userData, perovskite):
    '''Format dopands and aditives '''
    dopands = []
    for j, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove startni and ending blank spaces
            item = item.strip()

            # Du to data template version inconsistensy : should be replaced with |
            item = item.replace(":", "|")

            # Split on |
            itemList = item.split('|')

            for i, element in enumerate(itemList):
                if element.lower() in ['ascorbicacid']:
                    itemList[i] = 'Ascorbic acid'
                if element.lower() in ['phosphatidylcholine']:
                    itemList[i] = 'Phosphatidylcholine'

            # If the perovksite composition indicates Cl-doping, add Cl as a dopand
            ClCompositions = ['Clx', 'xCl3-x', 'xCly', 'CH3NH3PbI2.67Cl0.33', 'CH3NH3PbI2.75Cl0.25' ,'CH3NH3PbI2.7Cl0.30', 'CH3NH3PbI2.81Cl0.19', 'CH3NH3PbI2.89Cl0.11' ]
            for comp in ClCompositions:
                if comp in perovskite[j]:
                    if 'Cl' not in " | ".join(itemList):
                        if item == 'nan':
                            itemList = ['Cl']
                        else:
                            itemList.append('Cl')

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            # Remove nan
            if item.lower() == 'nan':
                item = ''
    
            dopands.append(item)
        except:
            dopands.append('')
            print(f'Cound not read in dopandsAndAdditives on line: {j}')

    return dopands

def dopandsAndAdditivesFractions(userData):
    '''Format the doping fractions'''
    dopands = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)
        
            ## Remove all blank spaces
            #item = item.strip().replace(" ","")     

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Du to data template version inconsistensy : should be replaced with |
            item = item.replace(":", "|")

            # Remove nan
            if item.lower() == 'nan':
                item = ''

            # If the first or the last character is a |
            if len(item) > 0:
                if item[0] == '|':
                    item = 'nan' + item
                if item[-1] == '|':
                    item = item + 'nan'

            # Split on |
            itemList = item.split('|')

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            dopands.append(item)
        except:
            print(f'faild to extract dopandsAndAdditivesFractions of {item} on row {i}')
            dopands.append(item)

    return dopands

def DopingOfContacts(userData):
    ''' Format the text for the ETL and HTL doping'''
    data = []
    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove starting and ending blank spaces
            item = item.strip()

            # Remove nan
            if item.lower() == 'nan':
                item = ''

            # If the first or the last character is a |
            if len(item) > 0:
                if item[0] == '|':
                    item = 'nan' + item
                if item[-1] == '|':
                    item = item + 'nan'

            # Split on |
            itemList = item.split('|')

            for j, element in enumerate(itemList):
                # Remove blank spaces
                element = element.strip()

                # Enforse proper formating (based on the variations I have seen)

                element = element.replace(" : ",":")
                element = element.replace(" :",":")
                element = element.replace(": ",":")

                element = element.replace("4-tert-butylpyridine","TBP")
                element = element.replace("4-tBP","TBP")
                element = element.replace("LiTFSI","Li-TFSI")
                element = element.replace("Li-TFSI, FK209, TBP", "Li-TFSI:TBP:FK209")
                element = element.replace("TBP, LiTFSI","Li-TFSI:TBP")

                itemList[j] = element

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            data.append(item)
        except:
            print(f'faild to extract doping of {item} on row {i}')
            data.append(item)

    return data

def FFData(userData, FF_cutoff = 5):
    '''Format FF data
        FF should be stated as a fraction which goes from 0 to 1 but is sometimes states in % going from 0 to 100 
        If the given values is larger than an abritray value of FF_cutoff, the
        value is asumed to be stated in % and is converted to a fraction
    '''
    values = []
    for item in userData:
        try:
            # To make it simple, the imput is converted to a string (regardless if it is or not)
            item = str(item)

            # Remove all blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Separate the number from the unit (which should not be there)
            number, unit = stringToNumberAndUnit(item)

            # Convert number in string reprecentation to a float
            number = convertToFloat(number)

            # Check if conversion to V should be done
            if float(number) > FF_cutoff:
                number = number/100

            # Round to the third decimal place
            number = np.around(number, decimals = 3)

            values.append(number)
        except:
            values.append(np.nan)
            print(f'Could not process FFData {item} on line {i}')
    return values
 
def is_number(s):
    ''' Simple function to see if a string is a float'''
    try:
        float(s)
        return True
    except ValueError:
        return False

def JscData(userData):
    '''Format Jsc data'''
    values = []
    for item in userData:
        try:
            # To make it simple, the imput is converted to a string (regardless if it is or not)
            item = str(item)

            # Remove all blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Separate the number from the unit (which should not be there)
            number, unit = stringToNumberAndUnit(item)

            # Convert number in string reprecentation to a float
            number = convertToFloat(number)

            # Round to the third decimal place
            number = np.around(number, decimals = 3)

            values.append(number)
        except:
            values.append(np.nan)
            print(f'Could not process JscData {item} on line {i}')
    return values

def mixingRatios(userData):
    '''List of relative humidity '''
    solutionMixtures = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionProcedures = layer.split('>>')

                for j, depositionProcedure in enumerate(depositionProcedures):
                    # Enforse proper formating
                    depositionProcedures[j] = mixingRatiosFormating(depositionProcedure)
                
                # Concatenate additives for each layer with proper spacing
                layers[i] = " >> ".join(depositionProcedures)

            # Concatenate all parts with proper spacing
            item = " | ".join(layers)

            solutionMixtures.append(item)
        except:
            print(f'faild to extract mixingRatios of {item} on row {i}')
            solutionMixtures.append(item)

    return solutionMixtures

def mixingRatiosFormating(ratios):
    ''' Check solventmixing against known formating variations 
    and return the standard formating for the solvent mixture'''

    # Remove all blank spaces
    ratios = ratios.replace(' ','')  
    
    # Enfors the use of decimal point
    ratios = ratios.replace(',', '.')
  
    # Enfors the use of list notation rather than mixing notation
    ratios = ratios.replace(':', ';')    

    # Check for the trivial case of no data
    if ratios.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'nan'

    # Separate out the number (with ; included) from the unit (that should not be there as it not is specified)
    numeric = '0123456789.;'
    j = 0
    for i, caracter in enumerate(ratios):
        if caracter not in numeric:
            break
        j = j+1
    ratiosNumbers = ratios[:j]

    # Empty list
    if len(ratiosNumbers) == 0:
        return 'nan'

    # Split on ;
    volumes = ratiosNumbers.split(';')

    # If there is only one solvent, the ratio is 1
    if len(volumes) == 1:
        return '1'

    for i, volume in enumerate(volumes):
        if is_number(volume):
            volumes[i] = volume
        else:
            volumes[i] = 'nan'
    
    # Return the joind and formated ratios
    return '; '.join(volumes)

def numberHighLowOrConstant(userData):
    '''Format numbers on the form (lowest;highest) or (constant value) 
    alwasy return a list of two values (lowest;highest) or (constant;constant)'''
    data = []

    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')
            
            # Split on ;
            elements = item.split(';')
    
             # Go trough each layer, and set np.nan for missing values
            for i, element in enumerate(elements):
                number, unit = stringToNumberAndUnit(element)
                if is_number(number):
                    elements[i] = number
                else:
                    elements[i] = str(np.nan)
            
            # In case of no values given
            if len(elements) == 0:
                item = 'nan; nan'

            # If only one number is given
            elif len(elements) == 1:
                elements.append(elements[0])
                item = '; '.join(elements)
            
            # If two or more values given
            else:
                item = '; '.join(elements[0:2])

            data.append(item)
        except:
            print(f'Failed to process numberHighLowOrConstant {item} on row {i}')
            data.append(item)

    return data

def numberList(userData):
    '''Returns a string with elements separated by a |'''
    data = []
    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Split on |
            itemList = item.split('|')

            # Go trough each layer, and set np.nan for missing values
            for j, element in enumerate(itemList):

                # Separate numbers from units
                number, unit = stringToNumberAndUnit(element)

                # If given corectly as a float
                if is_number(number):
                    itemList[j] = str(float(number))
                else:
                    itemList[j] = str(np.nan)
            
            # Concatenate all parts into a string with proper spacing
            item = " | ".join(itemList)
            
            # In case of emty cell
            if item == '':
                item = str(np.nan)

            data.append(item)
        except:
            print(f'Failed to process {item} on row {i}')
            data.append(item)

    return data

def numberListUnitless(userData):
    '''Format the volumes'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several elements separted by ;

    amounts = []
    for item in userData:
        try:
            # Enforce input is a string 
            item = str(item)   

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Enforse the list notation rather than the mixing notation
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    elements = depositionStep.split(';')

                    for k, element in enumerate(elements):
                        # Enforse proper formating
                        elements[k] = numberListUnitlessFormating(element)

                    depositionSteps[j] = '; '.join(elements)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            amounts.append(item)
        except:
            amounts.append('')
            print(f'Cound not read in temperature on line: {i}')

    return amounts
  
def numberListUnitlessFormating(element):
    ''' Check element againast known formating variations 
    and return the standard formating'''

    # Remove all blank spaces
    element = element.replace(' ','')

    # If not stated
    if element.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'nan'

    # Separate out the number from the unit (and there should be no unit)
    number, unit = stringToNumberAndUnit(element)
  
    return number

def numericInteger(userData, default = 0):
    '''Convert values to int with specified default value'''
    values = []
    for item in userData:
        # To make it simple, the imput is converted to a string (regardless if it is or not)
        item = str(item)

        # Remove all blank spaces
        item = item.strip().replace(" ","")

        # Enfors the use of decimal point
        item = item.replace(',', '.')

        if item.lower() in ['nan']:
            number = default
        elif is_number(item):
            number = int(float(item))
        else:
            number = default

        values.append(number)

    return values

def numericValues(userData):
    '''Convert values to float or np.nan for noncompliant values'''
    values = []
    for item in userData:
        # To make it simple, the imput is converted to a string (regardless if it is or not)
        item = str(item)

        # Remove all blank spaces
        item = item.strip().replace(" ","")

        # Enfors the use of decimal point
        item = item.replace(',', '.')

        # Separate the number from the unit (which should not be there)
        number, unit = stringToNumberAndUnit(item)

        # If given corectly as a float
        if is_number(number):
            values.append(float(number))

        # If not given corectly or missing, set value as np.nan
        else:
            values.append(np.nan)

    return values

def numericValuesWithEmptyCells(userData):
    '''Convert values to float or np.nan for noncompliant values'''
    values = []
    for i, item in enumerate(userData):
        try:
            # To make it simple, the imput is converted to a string (regardless if it is or not)
            item = str(item)

            # Remove all blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # If given corectly as a float
            if is_number(item):
                if np.isnan(float(item)):
                    values.append('')

                elif is_number(item):
                    values.append(float(item))

            # If not given corectly or missing, set value as empty
            else:
                values.append('')
        except:
            values.append('')
            print(f'Faild to run the numericValuesWithEmptyCells function on line {i} for {item} ')

    return values
    
def numericValuesWithPresission(userData, presission = 3):
    '''Convert values to float wiht given numer of decimals or np.nan for noncompliant values'''
    values = []
    for item in userData:
        # To make it simple, the imput is converted to a string (regardless if it is or not)
        item = str(item)

        # Enfors the use of decimal point
        item = item.replace(',', '.')

        # If given corectly as a float
        if is_number(item):
            # Round to the third decimal place
            item = np.around(float(item), decimals = presission)

            values.append(float(item))

        # If not given corectly or missing, set value as empty
        else:
            values.append(np.nan)

    return values

def PCEData(userData):
    '''Format PCE data'''
    values = []
    for item in userData:
        try:
            # To make it simple, the imput is converted to a string (regardless if it is or not)
            item = str(item)

            # Remove all blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Separate the number from the unit (which should not be there)
            number, unit = stringToNumberAndUnit(item)

            # Convert number in string reprecentation to a float
            number = convertToFloat(number)

            # Round to the second decimal place, unless the device is very unefficient
            if number > 1:
                number = np.around(number, decimals = 2)

            values.append(number)
        except:
            values.append(np.nan)
            print(f'Could not process PCEData {item} on line {i}')
    return values

def perovskiteAfterTreatment(userData):
    data = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove blank spaces
            item = item.strip()
        
            # Replace 'nan' with emty string
            if item.lower() == 'nan':
                item = ''

            item = item.replace("C2-propanol","IPA")

            # Split on |
            itemList = item.split('|')

            for i, element in enumerate(itemList):
                if len(element) > 0:
                    # Capitalize the element (but keap upper case for solvents etc.)
                    element = element[0].upper() + element[1:]
            
                itemList[i] = element

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            data.append(item)
        except:
            print(f'faild to extract perovskiteAfterTreatment of {item} on row {i}')
            data.append(item)

    return data

def perovskiteCoefficients(userData):
    '''Format coefficients in chemical formulas'''
    listOfCoefficients= []
    for item in userData:
        try:
            # Enforce input as a string 
            item = str(item)

            # Remove starting and ending blank spaces
            item = item.strip()

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Enfors the use of list notation rather than mixing notation
            item = item.replace(':', ';')
            
            # In case 1 have been read as True (have happened)
            if item == 'True':
                item = '1'

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on ;
                coefficients = layer.split(';')

                for j, coefficient in enumerate(coefficients):
                    # Enforse proper formating
                    coefficients[j] = coefficientsFormating(coefficient)
                
                # Concatenate additives for each layer with proper spacing
                layers[i] = "; ".join(coefficients)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            listOfCoefficients.append(item)
        except:
            listOfCoefficients.append('')
            print(f'Cound not read in perovskiteCoefficients on line: {j}')

    return listOfCoefficients

def perovskiteComposition(userData):
    '''Format the strings determining the perovskite compoition'''
    composition = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # In case of tempy string
            if item == '':
                item = 'none'

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Ensure that all ions are written with the right casing
            item = item.replace("fa","FA")
            item = item.replace("Fa","FA")
            item = item.replace("ma","MA")
            item = item.replace("Ma","MA")
            item = item.replace("pb","Pb")
            item = item.replace("Gua","GU")
            item = item.replace("CH3NH3","MA")

            item = item.replace("Sn0.5Pb0.5","Pb0.5Sn0.5")
            item = item.replace("Sn0.1Pb0.9","Pb0.9Sn0.1")

            item = item.replace("Sn0.5Ge0.5","Ge0.5Sn0.5")

            item = item.replace("I1.2Br1.8","Br1.8I1.2")
            item = item.replace("I1.5Br1.5","Br1.5I1.5")
            item = item.replace("I1.8Br1.2","Br1.2I1.8")
            item = item.replace("I2.1Br0.9","Br0.9I2.1")
            item = item.replace("I2.2Br0.8","Br0.8I2.2")
            item = item.replace("I2.24Br0.6","Br0.6I2.4")
            item = item.replace("I2.51Br0.49","Br0.49I2.51")
            item = item.replace("I2.55Br0.45","Br0.45I2.55")
            item = item.replace("I2.49Br0.51","Br0.51I2.49")
            item = item.replace("I2.5Br0.5","Br0.5I2.5")
            item = item.replace("I2.59Br0.41","Br0.41I2.59")
            item = item.replace("I2.65Br0.35","Br0.35I2.65")
            item = item.replace("I2.69Br0.31","Br0.31I2.69")
            item = item.replace("I2.7Br0.3","Br0.3I2.7")
            item = item.replace("I2.75Br0.25","Br0.25I2.75")
            item = item.replace("I2.8Br0.2","Br0.2I2.8")
            item = item.replace("I2.85Br0.15","Br0.15I2.85")
            item = item.replace("I2.9Br0.1","Br0.1I2.9")
            item = item.replace("I2.99Br0.01","Br0.01I2.99")

            item = item.replace("MA0.15FA0.75","FA0.75MA0.15")
            item = item.replace("MA0.17FA0.83","FA0.83MA0.17")
            item = item.replace("MA0.2FA0.8","FA0.8MA0.2")
            item = item.replace("MA0.4FA0.6","FA0.6MA0.4")
            item = item.replace("MA0.6FA0.4","FA0.4MA0.6")
            item = item.replace("MA0.7FA0.3","FA0.3MA0.7")
            item = item.replace("MA0.85FA0.15","FA0.15MA0.85")
            item = item.replace("MA0.9FA0.1","FA0.1MA0.9")
            item = item.replace("MA0.05FA0.83","FA0.83MA0.05")

            item = item.replace("MA0.1FA0.75Cs0.15", "Cs0.15FA0.75MA0.1")
            item = item.replace("MA0.6FA0.38Cs0.02", "Cs0.02FA0.38MA0.6")
            item = item.replace("FA0.75MA0.15Cs0.1", "Cs0.1FA0.75MA0.15")

            item = item.replace("MA0.85Cs0.15","Cs0.15MA0.85")

            item = item.replace("FA0.83Cs0.17","Cs0.17FA0.83")
            item = item.replace("FA0.7Cs0.3","Cs0.3FA0.7")
            item = item.replace("FA0.8Cs0.2","Cs0.2FA0.8")
            item = item.replace("FA0.85Cs0.15","Cs0.15FA0.85")
            item = item.replace("FA0.875Cs0.125","Cs0.125FA0.875")
            item = item.replace("FA0.9Cs0.1","Cs0.1FA0.9")
            item = item.replace("FA0.95Cs0.05","Cs0.05FA0.95")

            item = item.replace("FA0.85BA0.15", "BA0.15FA0.85")

            item = item.replace("MA3BA2","BA2MA3")
            item = item.replace("BA0.2MA3","MA3BA0.2")
            item = item.replace("BA0.4MA3","MA3BA0.4")
            item = item.replace("BA0.6MA3","MA3BA0.6")

            item = item.replace("Br1I2","BrI2")
            item = item.replace("I2Br","BrI2")
            item = item.replace("Br2I1","Br2I")

            item = item.replace("(I0.8Br0.2)3","Br0.6I2.4")
            item = item.replace("(I0.85Br0.15)3", "Br0.45I2.55")


            item = item.replace("(I0.75Br0.25)3", "Br0.75I2.25")

            ## Correct known formating mistakes
            #item = item.replace("bP","Pb")
            if item in ['MAPbI3-xClx', 'MAPbI3-xClx', 'MAPbIxCl3-x', 'MAPbI3−xClx', 'MAPbIxCly', 'MAPbi3', 'MAPbI2.67Cl0.33', 'MAPbI2.75Cl0.25' ,'MAPbI2.7Cl0.30', 'MAPbI2.81Cl0.19', 'MAPbI2.89Cl0.11']:
                item = 'MAPbI3'
            elif item in ['FAMAPbI3–xBrx', 'α-FAPbI3']:
                item = 'FAPbI3'
            elif item in ['(FAPbI3)0.7(MAPbBr3)0.3']:
                item = 'FA0.7MA0.3PbBr0.9I2.1'
            elif item in ['(FAPbI3)0.75(MAPbBr3)0.25']:
                item = 'FA0.75MA0.25PbBr0.75I2.25'
            elif item in ['(FAPbI3)0.8(MAPbBr3)0.2']:
                item = 'FA0.8MA0.2PbBr0.6I2.4'
            elif item in ['(FAPbI3)0.85(MAPbBr3)0.15', 'FAI)0.85(PbI2)0.85(MABr)0.15(PbBr2)0.15']:
                item = 'FA0.85MA0.15PbBr0.45I2.55'
            elif item in ['(FAPbI3)0.9(MAPbBr3)0.1']:
                item = 'FA0.9MA0.1PbBr0.3I2.7'
            elif item in ['(FAPbI3)0.95(MAPbBr3)0.05']:
                item = 'FA0.95MA0.05PbBr0.15I2.85'

            elif item in ['CsPbI2Br']:
                item = 'CsPbBrI2'

            elif item in ['(FAPbI3)10(BAPbI4)']:
                item = 'BAFA10Pb11I34'
            elif item in ['(FAPbI3)40(BAPbI4)']:
                item = 'BAFA40Pb41I124'
            elif item in ['(FAPbI3)60(BAPbI4)']:
                item = 'BAFA60Pb61I184'

            elif item in ['(MA)3Bi2I9']:
                item = 'MA3Bi2I9'
             
            elif item in ['Cs0.05FA0.81MA0.14PbI2.55Br0.45']:
                item = 'Cs0.05FA0.81MA0.14PbBr0.45I2.55'

            elif item in ['PEA0.15FA0.85SnI3:SnF2']:
                item = 'FA0.85PEA0.015SnI3'


            elif item in ['(CH3NH3)3Bi2I9']:
                item = 'MA3Bi2I9'

            elif item in ['MA0.9Cs0.1PbBr1.2I1.8']:
                item = 'Cs0.1MA0.9PbBr1.2I1.8'

            # Split on |
            itemList = item.split('|')

            for i, element in enumerate(itemList):
                # Remove leading and tailing blank spaces
                itemList[i] = element.strip()

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            # TO DO
            # Deal with parantesises

            # TO DO
            # Deal with the order of the ions

            composition.append(item)
        except:
            print(f'faild to extract perovskiteComposition of {item} on row {i}')
            composition.append(item)

    return composition

def perovskiteIons(userData):
    '''Format list of perovsktie ions'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several ions separted by ;

    listOfIons = []
    for item in userData:
        try:
            # Enforce input as a string 
            item = str(item)

            # Remove starting and ending blank spaces
            item = item.strip()

            # Enfors the use of list notation rather than mixing notation
            item = item.replace(':', ';') 

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on ;
                ions = layer.split(';')

                for j, ion in enumerate(ions):
                    # Enforse proper formating
                    ions[j] = perovskiteIonFormating(ion)
                
                # Concatenate additives for each layer with proper spacing
                layers[i] = "; ".join(ions)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            listOfIons.append(item)
        except:
            listOfIons.append('')
            print(f'Cound not read in dopandsAndAdditives on line: {j}')

    return listOfIons

def perovskiteIonFormating(ion):
    ''' Check pervskite ions againast known formating variations 
        and return the standard formating for the ion '''

    # Remove starting and ending blank spaces
    ion = ion.strip()

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in depositionProcedureFormating')
    elif ion.lower() in ['br']:
        ion = 'Br'
    elif ion.lower() in ['cs']:
        ion = 'Cs'
    elif ion.lower() in ['fa', 'ch5n2', 'ch(nh2)2']:
        ion = 'FA'
    elif ion.lower() in ['ma', 'ch3nh3']:
        ion = 'MA'
    elif ion.lower() in ['pb']:
        ion = 'Pb'
    elif ion.lower() in ['sn']:
        ion = 'Sn'
    elif ion.lower() in ['', 'nan', 'non', 'none', 'np.nan', 'unknown']:
        ion = 'nan'


    return ion

def perovskiteLongForm(userData):
    '''Format the peroskite short form '''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several perovskite mixed with each other separated by ;
    compositionList = []
    for item in userData:
        try:
            # Enforce input as a string 
            item = str(item)

            # Remove starting and ending blank spaces
            item = item.strip()

            # Enfors the use of list notation rather than mixing notation
            item = item.replace(':', ';') 

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on ;
                perovskites = layer.split(';')

                for j, perovskite in enumerate(perovskites):
                    # Enforse proper formating
                    perovskites[j] = perovskiteLongFormFormating(perovskite)
                
                # Concatenate additives for each layer with proper spacing
                layers[i] = "; ".join(perovskites)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            compositionList.append(item)
        except:
            compositionList.append('')
            print(f'Cound not read in perovskiteShortForm on line: {j}')

    return compositionList

def perovskiteLongFormFormating(perovskite):
    ''' Check perovskite againast known formating variations 
    and return the standard formating for the perovskite'''

    # If stated as Unknown it will be determined from the information given from the A, B, and C ions

    # Remove all blank spaces
    perovskite = perovskite.replace(' ','')

    # If not stated
    if perovskite.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'Unknown'

    # Ensure that all ions are written with the right casing
    perovskite = perovskite.replace("fa","FA")
    perovskite = perovskite.replace("Fa","FA")
    perovskite = perovskite.replace("ma","MA")
    perovskite = perovskite.replace("Ma","MA")
    perovskite = perovskite.replace("CH3NH3","MA")
    perovskite = perovskite.replace("pb","Pb")

    return perovskite

def perovskiteNonStoichiometry(userData):
    '''Format the strings determining the perovskite components in excess'''
    composition = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove leading and tailing blank spaces
            item = item.strip()

            # Remove blank spaces
            item = item.replace(" ","")

            if item.lower() == 'nan':
                item = ''

            composition.append(item)
        except:
            print(f'faild to extract perovskiteNonStoichiometry of {item} on row {i}')
            composition.append(item)

    return composition

def PerovskitePrecursorState(userData):
    '''Format the textstring describing the precursor state'''
    states = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove all blank spaces
            item = item.strip().replace(" ","")

            # Remove nan
            if item.lower() == 'nan':
                item = ''

            # Split on |
            itemList = item.split('|')
    
            for i, element in enumerate(itemList):
                if element.lower() in ['vapor']:
                    element = 'Vapour'     
                if element.lower() in ['solution', 'solutionn', 'soultion', 'solutions']:
                    element = 'Solution'                 
                itemList[i] = element.title()

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)
    
            states.append(item)
        except:
            print(f'faild to extract PerovskitePrecursorState of {item} on row {i}')
            states.append(item)

    return states

def perovskiteShortForm(userData):
    '''Format the peroskite short form '''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several perovskite mixed with each other separated by ;
    compositionList = []
    for item in userData:
        try:
            # Enforce input as a string 
            item = str(item)

            # Remove starting and ending blank spaces
            item = item.strip()

            # Enfors the use of list notation rather than mixing notation
            item = item.replace(':', ';') 

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on ;
                perovskites = layer.split(';')

                for j, perovskite in enumerate(perovskites):
                    # Enforse proper formating
                    perovskites[j] = perovskiteShortFormFormating(perovskite)
                
                # Concatenate additives for each layer with proper spacing
                layers[i] = "; ".join(perovskites)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            compositionList.append(item)
        except:
            compositionList.append('')
            print(f'Cound not read in perovskiteShortForm on line: {j}')

    return compositionList

def perovskiteShortFormFormating(perovskite):
    ''' Check perovskite againast known formating variations 
    and return the standard formating for the perovskite'''

    # Remove all blank spaces
    perovskite = perovskite.replace(' ','')

    # If not stated
    if perovskite.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'Unknown'

    # Ensure that all ions are written with the right casing
    perovskite = perovskite.replace("fa","FA")
    perovskite = perovskite.replace("Fa","FA")
    perovskite = perovskite.replace("ma","MA")
    perovskite = perovskite.replace("Ma","MA")
    perovskite = perovskite.replace("CH3NH3","MA")
    perovskite = perovskite.replace("pb","Pb")

    return perovskite

def potentialBias(userData):
    '''Format text string describing potential bias in stability measurements'''
    bias = []
    for item in userData:
        try:
            # Enforce input as a string 
            item = str(item)
    
            # Remove starting and ending blank spaces
            item = item.strip()

            # Go trough known formating variations
            if False:   # To start the elif cascade
                Print(f'Problem in elif cascade in potentialBias')

            elif item.lower() in ['constant', 'bias']:
                item = 'Constant'
            elif item.lower() in ['mpp', 'mppt', 'maximum power point']:
                item = 'MPPT'
            elif item.lower() in ['non', 'none', 'oc', 'open circuit', 'open-circuit']:
                item = 'Open circuit'
            elif item.lower() in ['sc', 'short circuit', 'short-circuit']:
                item = 'Short circuit'
            elif item.lower() in ['']:
                item = ''
            else:
                item = item

            bias.append(item)
        except:
            bias.append('')
            print(f'Cound not read in potentialBias on line: {j}')


    return bias

def preconditioningProtocoll(userData):
    '''Format the text strings for the preconditioning protocolls'''
    protocoll = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove leading and tailing blank spaces
            item = item.strip()

            # Split on @
            itemList = item.split('@')

            # Enforse proper formating (based on the variations I have seen)
            for i, element in enumerate(itemList):
                # Remove leading and tailing blank spaces
                element = element.strip()
            
                if element.lower() == 'nan':
                    itemList[i] = ''
                elif element.lower() in ['light soaking', 'bias light', 'light bias']:
                    itemList[i] = 'Light soaking'
                elif element.lower() in ['open circut']:
                    itemList[i] = 'Open circut'
                elif element.lower() in ['potential biasing']:
                    itemList[i] = 'Potential biasing'
                else:
                    itemList[i] = element.title()

            # Concatenate all parts with proper spacing
            item = " @ ".join(itemList)

            protocoll.append(item)
        except:
            print(f'faild to extract preconditioningProtocoll of {item} on row {i}')
            protocoll.append(item)

    return protocoll

def pressure(userData):
    # list of pressures    
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several pressures separted by ;
    environment = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Change from notation of mixtures to notation of lists
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    gases = depositionStep.split(';')

                    for k, gas in enumerate(gases):
                        # Enforse proper formating
                        gases[k] = pressureFormating(gas)

                    depositionSteps[j] = '; '.join(gases)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            environment.append(item)
        except:
            print(f'faild to extract pressure of {item} on row {i}')
            environment.append(item)

    return environment

def pressureFormating(pressure):
    ''' Check amounts againast known formating variations 
    and return the standard formating for the amount'''

    # Remove all blank spaces
    pressure = pressure.replace(' ','')

    # If not stated
    if pressure.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'nan'

    # Separate out the number from the unit
    number, unit = stringToNumberAndUnit(pressure)
 
    # If there is no unit, retun the number as it is
    if len(pressure) == len(number):
        return number
    
    ## If there is a unit, Format the units with respect to known formating variations
    if unit.lower() in ['atm', 'atmosphere', 'atm.']:
        unit = 'atm'
    elif unit.lower() in ['bar']:
        unit = 'bar'
    elif unit.lower() in ['mbar']:
        unit = 'mbar'
    elif unit.lower() in ['mmhg']:
        unit = 'mmHg'
    elif unit.lower() in ['pa', 'pascal']:
        unit = 'Pa'
    elif unit.lower() in ['torr']:
        unit = 'Torr'
    elif unit.lower() in ['psi']:
        unit = 'psi'
    else: 
        unit = unit

    # Concatenate the number and the unit
    pressure = ' '.join([number, unit])

    return pressure

def purity(userData):
    '''Format the string describing the purity for the chemcials'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several solvents/chemicals separted by ;
    supplierList = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Change from notation of mixtures to notation of lists
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    purities = depositionStep.split(';')

                    for k, purity in enumerate(purities):
                        # Enforse proper formating
                        purities[k] = purityFormating(purity)

                    depositionSteps[j] = '; '.join(purities)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            supplierList.append(item)
        except:
            print(f'faild to extract supplier of {item} on row {i}')
            supplierList.append(item)

    return supplierList

def purityFormating(purity):
    ''' Check suppliers againast known formating variations 
    and return the standard formating for the supplier'''

    # Remove starting and ending blank spaces
    purity = purity.strip()

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in atmosphereFormating')
  
    elif purity.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        purity = 'Unknown'

    return purity

def quenchingMedia(userData):
    '''Format the description of the quenching media'''
    media = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove starting and ending blank spaces
            item = item.strip()
        
            # Replace 'nan' with emty string
            if item.lower() == 'nan':
                item = ''

            # Go through all known formating variations and convert them to the corect one

            # Split on |
            itemList = item.split('|')

            for i, element in enumerate(itemList):

                element = element.strip()

                # Proper spaceing around '@'
                # Split on @
                elementList = element.split('@')

                # Remove blank spaces
                for k, x in enumerate(elementList):         
                    elementList[k] = x.strip()

                # Concatenate all parts with proper spacing
                element = " @ ".join(elementList)

                # Go through all known formating variations and convert them to the corect one
                if element.lower() in ['gas', 'gas blowing', 'gas quench', 'gas-assisted']:
                    itemList[i] = 'Gas'
                elif element.lower() in ['dry air', 'dry-air']:
                    itemList[i] = 'Dry air'
                elif element.lower() in ['anisole', 'methyl phenoxide', 'methoxybenzene']:
                    itemList[i] = 'Anisole'
                elif element.lower() in ['antisolvent', 'nonhalogenated antisolvent', 'polar solvent', 'nonpolar solvent scouring']:
                    itemList[i] = 'Antisolvent'

                elif element.lower() in ['sec-butyl alcohol', '2-buthanol', 'sec butyl alcohol', 'sba']:
                    itemList[i] = '2-Butanol'
                elif element.lower() in ['butyl acetate']:
                    itemList[i] = 'Butyl acetate'

                elif element.lower() in ['dcm', 'dichloromethane']:
                    itemList[i] = 'Dichloromethane'
                elif element.lower() in ['dichlorobenzene']:
                    itemList[i] = 'Dichlorobenzene'

                elif element.lower() in ['2-propanol','isopropanol', 'isopropylalcohol', 'ipa', 'iso-propanol']:
                    itemList[i] = 'IPA'
                elif element.lower() in ['chlorobenzene', 'cb', 'cbz', 'chlorobenze', 'chlorobenzenene', 'chlorobenzenene', 'chlorobenzenenez', 'clorobenzene', 'anhydrous chlorobenzene', 'cholorobenzene', 'chloro benzene']:
                    itemList[i] = 'Chlorobenzene'
                elif element.lower() in ['chloroform', 'chloroform-d']:
                    itemList[i] = 'Chloroform'
                elif element.lower() in ['dee', 'diethyl ether', 'dieathyl  ether', 'diethylether', 'ethoxyethane', 'anhydrous diethyl ether', 'anhydrous diethyl ether', 'de']:
                    itemList[i] = 'Diethyl ether'
                elif element.lower() in ['diphenylether']:
                    itemList[i] = 'Diphenyl ether'
                elif element.lower() in ['ether', 'anhydrous ether']:
                    itemList[i] = 'Ether'
                elif element.lower() in ['ethanol']:
                    itemList[i] = 'Ethanol'
                elif element.lower() in ['ethyl acetate', 'ethylacetate', 'ea', 'ethylene acetate', 'ethylacetate']:
                    itemList[i] = 'Ethyl acetate'
                elif element.lower() in ['ethyl ether', 'eth']:
                    itemList[i] = 'Ethyl ether'

                elif element.lower() in ['fira', 'flash infrared annealling (fira)', 'flash infrared annealling']:
                    itemList[i] = 'Flash infrared annealling'

                elif element.lower() in ['hot air']:
                    itemList[i] = 'Hot air'

                elif element.lower() in ['methyl acetate']:
                    itemList[i] = 'Methyl acetate'

                elif element.lower() in ['n2', 'n2 blowing', 'n2-gas']:
                    itemList[i] = 'N2'

                elif element.lower() in ['propyl acetate']:
                    itemList[i] = 'Propyl acetate'

                elif element.lower() in ['tetrachloroethane']:
                    itemList[i] = 'Tetrachloroethane'
                elif element.lower() in ['trifluorotoluene', 'α, α, α-trifluorotoluene']:
                    itemList[i] = 'Trifluorotoluene'
                elif element.lower() in ['toulene', 'toluene', 'methylbenzene', 'tolune', 'anhydrous toulene']:
                    itemList[i] = 'Toluene'
                elif element.lower() in ['tetrafluorotoluene']:
                    itemList[i] = 'Tetrafluorotoluene'

                elif element.lower() in ['tetraethyl orthosilicate']:
                    itemList[i] = 'Tetraethyl orthosilicate'
                elif element.lower() in ['vacuum']:
                    itemList[i] = 'Vacuum'

                else:
                    itemList[i] = element

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            media.append(item)

        except:
            print(f'faild to extract quenchingMedia of {item} on row {i}')
            media.append(item)

    return media

def relativeHumidity(userData):
    '''List of relative humidity '''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several humidites separted by ;
    environment = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    humidities = depositionStep.split(';')

                    for k, humidity in enumerate(humidities):
                        # Enforse proper formating
                        humidities[k] = relativeHumidityFormating(humidity)

                    depositionSteps[j] = '; '.join(humidities)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            environment.append(item)
        except:
            print(f'faild to extract relativeHumidity of {item} on row {i}')
            environment.append(item)

    return environment

def relativeHumidityFormating(humidity):
    ''' Check relative humidity againast known formating variations 
    and return the standard formating for the atmosphere '''

    # Remove unit
    humidity = humidity.replace("%","")

    # Remove starting and ending blank spaces
    humidity = humidity.strip()

    if is_number(humidity):
        return humidity
    elif humidity.lower() in ['ambient']:
        humidity = 'Ambient'
    else: 
        humidity = 'nan'

    return humidity

def relativeHumidityOld(userData):
    '''Convert all entries to strings and fomrat non merical entries'''
    newStrings = []
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Replace nan with emty string
            if item == 'nan':
                item = ''

            if item.lower() in ['ambient']:
                item = 'Ambient'
        
            newStrings.append(item)
        except:
            print(f'faild to extract relativeHumidity of {item} on row {i}')
            newStrings.append(item)

    return newStrings

def responsiblePerson(userData):
    '''Return the name given as responsible for entering the data '''
    person = []
    for item in userData:
        # Enforce that input is a string 
        item = str(item)
        
        # Remove starting and ending blank spaces
        item = item.strip()
        
        # Replace 'nan' with emty string
        if item.lower() == 'nan':
            item = ''

        person.append(item)
    return person

def solvents(userData):
    '''Format the string describing the solvents'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several solvents in the solution separted by ;
    reactionSolutions = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Change from notation of mixtures to notation of lists
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    solvents = depositionStep.split(';')

                    for k, solvent in enumerate(solvents):
                        # Enforse proper formating
                        solvents[k] = solventFormating(solvent)

                    depositionSteps[j] = '; '.join(solvents)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            reactionSolutions.append(item)
        except:
            print(f'faild to extract solvents of {item} on row {i}')
            reactionSolutions.append(item)

    return reactionSolutions

def solventFormating(solvent):
    ''' Check solvent againast known formating variations 
    and return the standard formating for the solvent 
    Inculdes special cases for gas based antisolvents'''

    # Remove starting and ending blank spaces
    solvent = solvent.strip()

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in atmosphereFormating')
  
    elif solvent.lower() in  ['', 'unknown', 'nan', 'na', '-', 'np.nan']:
        formatedSolvent = 'Unknown'

    elif solvent.lower() in ['2-methoxyethanol', '2-me']:
        formatedSolvent = '2-methoxyethanol'

    elif solvent.lower() in ['acn', 'acetonitrile']:
        formatedSolvent = 'acetonitrile'
    elif solvent.lower() in ['anisole', 'methoxybenzene', 'methyl phenoxide']:
        formatedSolvent = 'Anisole'
    elif solvent.lower() in ['antisolvent', 'nonhalogenated antisolvent', 'nonpolar solvent scouring', 'polar solvent']:
        formatedSolvent = 'Antisolvent'

    elif solvent.lower() in ['2-buthanol', 'sba', 'sec butyl alcohol', 'sec-butyl alcohol']:
        formatedSolvent = '2-Butanol'
    elif solvent.lower() in ['butyl acetate']:
        formatedSolvent = 'Butyl acetate'

    elif solvent.lower() in ['anhydrous chlorobenzene', 'cb', 'cbz', 'chloro benzene', 'chlorobenze', 'chlorobenzene', 'chlorobenzenene', 'chlorobenzenene', 'chlorobenzenenez', 'cholorobenzene', 'clorobenzene']:
        formatedSolvent = 'Chlorobenzene'
    elif solvent.lower() in ['chloroform', 'chloroform-d']:
        formatedSolvent = 'Chloroform'

    elif solvent.lower() in ['dcm', 'dichloromethane']:
        formatedSolvent = 'Dichloromethane'
    elif solvent.lower() in ['dichlorobenzene']:
        formatedSolvent = 'Dichlorobenzene'
    elif solvent.lower() in ['anhydrous diethyl ether', 'anhydrous diethyl ether', 'de', 'dee', 'dieathyl  ether', 'diethyl ether', 'diethylether', 'ethoxyethane']:
        formatedSolvent = 'Diethyl ether'
    elif solvent.lower() in ['diphenylether']:
        formatedSolvent = 'Diphenyl ether'
    elif solvent.lower() in ['(ch3)2nc(o)h', 'dimethylformamide', 'dimetylformamid', 'dmf', 'n,n-dimethylformamide']:
        formatedSolvent = 'DMF'
    elif solvent.lower() in ['(ch3)2so', 'dimethyl sulfoxide', 'dimethylsulfoxide', 'dmso']:
        formatedSolvent = 'DMSO'

    elif solvent.lower() in ['anhydrous ether', 'ether']:
        formatedSolvent = 'Ether'
    elif solvent.lower() in ['ethanol', 'etoh']:
        formatedSolvent = 'Ethanol'
    elif solvent.lower() in ['ea', 'ethyl acetate', 'ethylacetate', 'ethylacetate', 'ethylene acetate']:
        formatedSolvent = 'Ethyl acetate'
    elif solvent.lower() in ['eth', 'ethyl ether']:
        formatedSolvent = 'Ethyl ether'

    elif solvent.lower() in ['butyrolactetone', 'butyrolactone', 'gamma-butyrolactone', 'gamma-gbl', 'gbl', 'γ-butyrolactone', 'γ-gbl']:
        formatedSolvent = 'GBL'

    elif solvent.lower() in ['2-propanol', 'ipa', 'iso-propanol', 'isopropanol', 'isopropylalcohol']:
        formatedSolvent = 'IPA'

    elif solvent.lower() in ['methanol', 'meoh']:
        formatedSolvent = 'Methanol'
    elif solvent.lower() in ['methyl acetate']:
        formatedSolvent = 'Methyl acetate'
    elif solvent.lower() in ['methylamine']:
        formatedSolvent = 'Methylamine'

    elif solvent.lower() in ['n-methylpyrrolidone', 'nmp', 'n‐methyl‐2‐pyrrolidinone']:
        formatedSolvent = 'NMP'

    elif solvent.lower() in ['non', 'none']:
        formatedSolvent = 'none'
        
    elif solvent.lower() in ['octane']:
        formatedSolvent = 'Octane'

    elif solvent.lower() in ['pei', 'polyethylenimine']:
        formatedSolvent = 'PEI'
    elif solvent.lower() in ['propyl acetate']:
        formatedSolvent = 'Propyl acetate'

    elif solvent.lower() in ['tetrachloroethane']:
        formatedSolvent = 'Tetrachloroethane'
    elif solvent.lower() in ['tetraethyl orthosilicate']:
        formatedSolvent = 'Tetraethyl orthosilicate'
    elif solvent.lower() in ['tetrafluorotoluene']:
        formatedSolvent = 'Tetrafluorotoluene'
    elif solvent.lower() in ['α, α, α-trifluorotoluene', 'trifluorotoluene']:
        formatedSolvent = 'Trifluorotoluene'
    elif solvent.lower() in ['anhydrous toulene', 'methylbenzene', 'toluene', 'tolune', 'toulene']:
        formatedSolvent = 'Toluene'

    elif solvent.lower() in  ['unknown']:
        formatedSolvent = 'Unknown'

    # Special cases for non solvent based antisolvet treatments
    elif solvent.lower() in ['argon', 'ar']:
        formatedSolvent = 'Ar'
    elif solvent.lower() in ['dry air', 'dry-air']:
        formatedSolvent = 'Dry air'
    elif solvent.lower() in ['fira', 'flash infrared annealling (fira)', 'flash infrared annealling']:
        formatedSolvent = 'Flash infrared annealling'
    elif solvent.lower() in ['gas', 'gas blowing', 'gas quench', 'gas-assisted']:
        formatedSolvent = 'Gas'
    elif solvent.lower() in ['hot air']:
        formatedSolvent = 'Hot air'
    elif solvent.lower() in ['n2', 'n2 blowing', 'n2-gas', 'nitrogen']:
        formatedSolvent = 'N2'
    elif solvent.lower() in ['vacuum']:
        formatedSolvent = 'Vacuum'

    # If no known formating variations
    else: 
        formatedSolvent = solvent

    return formatedSolvent

def solventsOld(userData):
    ''' Format the solvents description'''
    solvents = []

    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove blank spaces
            item = item.strip().replace(" ","")

            # Replace 'nan' with emty string
            if item.lower() == 'nan':
                item = ''

            # Corect or formatingvariations
            
            item = item.replace(" : ",":")
            item = item.replace(" :",":")
            item = item.replace(": ",":")
            item = item.replace("ACN","Acetonitrile")
            item = item.replace("2-Propanol","IPA")
            item = item.replace("Isopropanol","IPA")
            item = item.replace("2-propanol","IPA")
            item = item.replace("isopropanol","IPA")
            item = item.replace("EtOH","Ethanol")    
            item = item.replace("butyrolactetone", "GBL")
            item = item.replace("butyrolactone","GBL")
            item = item.replace("Butyrolactone","GBL")
            item = item.replace("gamma-GBL","GBL")         
            item = item.replace("gamma-butyrolactone","GBL")
            item = item.replace("γ-butyrolactone","GBL")
            item = item.replace("γ-GBL","GBL")
            item = item.replace("γ‐GBL","GBL")
            item = item.replace("GBL","GBL")
            item = item.replace("acetonitrile","Acetonitrile")
            item = item.replace("CB","Chlorobenzene")
            item = item.replace("Chlorobenze","Chlorobenzene")
            item = item.replace("chlorobenzene","Chlorobenzene")
            item = item.replace("dimethylformamide","DMF")
            item = item.replace("methanol","Methanol")
            item = item.replace("2-ME", '2-methoxyethanol')
            item = item.replace('methylamine','Methylamine')
            item = item.replace('diethylether', 'Diethyl ether')
            item = item.replace('octane','Octane')

            # Split on |
            itemList = item.split('|')

            tempList = []
            for element in itemList:
                # Split on @
                elementList = element.split('@')

                # Remove blank spaces
                for k, x in enumerate(elementList):         
                    elementList[k] = x.strip()

                # Concatenate all parts with proper spacing
                elementList = " @ ".join(elementList)

                tempList.append(elementList)

            # Concatenate all parts with proper spacing
            item = " | ".join(tempList)

            solvents.append(item)

        except:
            solvents.append(item)
            print(f'Could not process solvent on line {i}')

    return solvents

def stackSequence(userData):
    '''Format the string describing stack sequences'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several elements separted by ;
    # For each element there could be a mixtures of materials separated by a : 
    stack = []
    
    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on ;
                elements = layer.split(';')

                for j, element in enumerate(elements):
                    # Split on :
                    materials = element.split(':')

                    for k, material in enumerate(materials):
                        # Enforse proper formating
                        materials[k] = stackSequenceFormating(material)

                   # Concatenate all parts with proper spacing
                    elements[j] = ':'.join(materials)

               # Concatenate all parts with proper spacing
                layers[i] = '; '.join(elements)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            stack.append(item)

        except:
            print(f'faild to extract stackSequence of {item} on row {i}')
            stack.append(item)

    return stack

def stackSequenceFormating(stackElement):
    ''' Check stack element againast known formating variations 
        and return the standard formating for the stack element'''

    # Remove starting and ending blank spaces
    stackElement = stackElement.strip()

    # In string formating
    stackElement = stackElement.replace(" : ",":")
    stackElement = stackElement.replace(" :",":")
    stackElement = stackElement.replace(": ",":")
    stackElement = stackElement.replace(" NPs","-np")

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in stackElementFormating')
  
    elif stackElement.lower() in  ['', 'unknown', 'nan', 'na', '-', 'np.nan']:
        formatedStackElement = 'Unknown'

    elif stackElement.lower() in ['ag np', 'ag-np', 'ag nps', 'ag-nps']:
        formatedStackElement = 'Ag-np'
    elif stackElement.lower() in ['ag - nws', 'ag nano wires', 'ag nanowires', 'ag nw', 'ag nws', 'ag-nanowire', 'ag-nanowires', 'ag-nr', 'ag-nw', 'agnr', 'agnw', 'agnws']:
        formatedStackElement = 'Ag-nw'
    elif stackElement.lower() in ['al2o3-m', 'al2o3-ms', 'm-al2o3', 'mp-al2o3', 'm-alo2']:
        formatedStackElement = 'Al2O3-mp'
    elif stackElement.lower() in ['a.r.c.', 'arc', 'a.r.c']:
        formatedStackElement = 'A.R.C.'
    elif stackElement.lower() in ['au np', 'au nps', 'au-np', 'au-nps']:
        formatedStackElement = 'Au-np'
    elif stackElement.lower() in ['azo', 'al:zno', 'zno:al']:
        formatedStackElement = 'AZO'
    elif stackElement.lower() in ['al:zno np', 'al:zno-np', 'azo-np', 'azo np', 'azo nanoparticles', 'zno:al np', 'zno:al-np']:
        formatedStackElement = 'AZO-np'

    elif stackElement.lower() in ['barrier foil']:
        formatedStackElement = 'Barrier foil' 
    elif stackElement.lower() in ['bathocuproine', 'bcp']:
        formatedStackElement = 'BCP' 
    elif stackElement.lower() in ['bis-c60']:
        formatedStackElement = 'bis-C60'
    elif stackElement.lower() in ['bphen']:
        formatedStackElement = 'Bphen'          
    elif stackElement.lower() in ['mp-bso']:
        formatedStackElement = 'BSO-mp'   
 
    elif stackElement.lower() in ['c60']:
        formatedStackElement = 'C60'        
    elif stackElement.lower() in ['c', 'carbon' ,'carbon electrode']:
        formatedStackElement = 'Carbon'  
    elif stackElement.lower() in ['c-mp', 'carbon-mp']:
        formatedStackElement = 'Carbon-mp' 
    elif stackElement.lower() in ['c nanotube', 'c-nanotube', 'c-nt', 'carbon nanotube', 'carbon-nanotube', 'carbon-nt', 'cnt']: 
        formatedStackElement = 'Carbon-nt' 
    elif stackElement.lower() in ['c qds', 'c-qds', 'carbon-qds', 'cqds']:
        formatedStackElement = 'Carbon-QDs'
    elif stackElement.lower() in ['cover glass']:
        formatedStackElement = 'Cover glass-QDs'
    elif stackElement.lower() in ['cu:niox']:
        formatedStackElement = 'Cu:NiO' 

    elif stackElement.lower() in ['epoxy']:
        formatedStackElement = 'Epoxy' 
    elif stackElement.lower() in ['epoxy resin']:
        formatedStackElement = 'Epoxy resin' 
    elif stackElement.lower() in ['etl', 'etm']:
        formatedStackElement = 'ETM' 

    elif stackElement.lower() in ['fto', 'f:sno2']:
        formatedStackElement = 'FTO' 

    elif stackElement.lower() in ['glas']:
        formatedStackElement = 'Glass' 
    elif stackElement.lower() in ['graphene']:
        formatedStackElement = 'Graphene' 
    elif stackElement.lower() in ['graphene oxide', 'go']:
        formatedStackElement = 'Graphene oxide'
    elif stackElement.lower() in ['gns']:
        formatedStackElement = 'Graphene-ns' 
    elif stackElement.lower() in ['graphite']:
        formatedStackElement = 'Graphite' 

    elif stackElement.lower() in ['htl', 'htm']:
        formatedStackElement = 'HTM' 

    elif stackElement.lower() in ['ito', 'in:sno2']:
        formatedStackElement = 'ITO' 

    elif stackElement.lower() in ['metal', 'metall']:
        formatedStackElement = 'Metal' 
    elif stackElement.lower() in ['mwcnt', 'mwcnts']:
        formatedStackElement = 'MWCNTs' 

    elif stackElement.lower() in ['ngns']:
        formatedStackElement = 'N-Graphene-ns' 
    elif stackElement.lower() in ['nio', 'niox']:
        formatedStackElement = 'NiO' 
    elif stackElement.lower() in ['nio-c', 'niox-c']:
        formatedStackElement = 'NiO-c'
    elif stackElement.lower() in ['nio np', 'nio-np', 'nionp', 'niox -np', 'niox np', 'niox-nc', 'niox-np']:
        formatedStackElement = 'NiO-np'
    elif stackElement.lower() in ['nio-mp', 'niox-m', 'niox-mp']:
        formatedStackElement = 'NiO-mp'
    elif stackElement.lower() in ['non', 'none']:
        formatedStackElement = 'none'

    elif stackElement.lower() in ['pbs qds', 'PbS-qd']:
        formatedStackElement = 'PbS-QDs'
    elif stackElement.lower() in ['pc60bm', 'pc61bm', 'pcbm', 'pcbm-60', 'pcbm-61', 'pcbm-c60', 'pcbm-c61', 'pcbm60', 'pcbm61']:
        formatedStackElement = 'PCBM-60' 
    elif stackElement.lower() in ['pc70bm', 'pc71bm', 'pcb71m', 'pcbm-70', 'pcbm-71', 'pcbm-c70', 'pcbm-c71', 'pcbm70', 'pcbm71']:
        formatedStackElement = 'PCBM-70'
    elif stackElement.lower() in ['pedot']:
        formatedStackElement = 'PEDOT'
    elif stackElement.lower() in ['pedot:pss', 'pedot : pss', 'pedot-pss']:
        formatedStackElement = 'PEDOT:PSS'
    elif stackElement.lower() in ['pei', 'polyetherimide']:
        formatedStackElement = 'PEI'
    elif stackElement.lower() in ['peg']:
        formatedStackElement = 'PEG'
    elif stackElement.lower() in ['peg']:
        formatedStackElement = 'PEG'
    elif stackElement.lower() in ['ito-pen']:
        formatedStackElement = 'PEN | ITO'
    elif stackElement.lower() in ['pet']:
        formatedStackElement = 'PET'
    elif stackElement.lower() in ['perovksite', 'perovskite', 'perovskites', 'pervoskite', 'prevskite', 'provskite', 'psk']:
        formatedStackElement = 'Perovskite'
    elif stackElement.lower() in ['polymer']:
        formatedStackElement = 'Polymer'
    elif stackElement.lower() in ['poly-tpd', 'polytpd']:
        formatedStackElement = 'PolyTPD'
    elif stackElement.lower() in ['poly(triaryl amine)', 'poly(triarylamine)', 'poly[bis(4-phenyl)(2,4,6-trimethylphenyl)amine]]', 'polytriaryl amine', 'polytriarylamine', 'ptaa',]:
        formatedStackElement = 'PTAA'
    elif stackElement.lower() in ['pss']:
        formatedStackElement = 'PSS'

    elif stackElement.lower() in ['fused quartz', 'fused silica', 'quartz', 'quartz glass']:
        formatedStackElement = 'Quartz'

    elif stackElement.lower() in ['r-go', 'rgo']:
        formatedStackElement = 'rGO' 
    elif stackElement.lower() in ['rhodamine101', 'rhodamine 101', 'rhb101']:
        formatedStackElement = 'Rhodamine 101'

    elif stackElement.lower() in ['si-nanorods', 'si-nr', 'si-nw']:
        formatedStackElement = 'Si-nw'
    elif stackElement.lower() in ['glass', 'ngo', 'ngo10', 'pilkington', 'sgl', 'slf', 'slg', 'tec']:
        formatedStackElement = 'SLG'
    elif stackElement.lower() in ['sno2', 'snox']:
        formatedStackElement = 'SnO2'
    elif stackElement.lower() in ['c-sno2', 'sno2-bl', 'sno2-c']:
        formatedStackElement = 'SnO2-c'
    elif stackElement.lower() in ['m-sno2', 'mp-sno2', 'sno2 m', 'sno2 mp', 'sno2-m', 'sno2-mp']:
        formatedStackElement = 'SnO2-mp'
    elif stackElement.lower() in ['np-sno2', 'sno2 -np', 'sno2 np', 'sno2-ncs', 'sno2-np']:
        formatedStackElement = 'SnO2-np'
    elif stackElement.lower() in ['sno2 nanorods', 'sno2 nanowires', 'sno2-nanorods', 'sno2-nanowires', 'sno2-nr', 'sno2-nw']:
        formatedStackElement = 'SnO2-nw'
    elif stackElement.lower() in ['sno2-qd', 'sno2-qds']:
        formatedStackElement = 'SnO2-QDs'
    elif stackElement.lower() in ['spiiro', 'spiro', 'spiro ometad', 'spiro ometad', 'spiro-meotad', 'spiro-ometad', 'spiromeotad', 'spirometad', 'spiroometad', 'spiroometad', 'spiro‐meotad', 'spiro‐ometad', 'sprio', 'sprio-ometad']:
        formatedStackElement = 'Spiro-MeOTAD'
    elif stackElement.lower() in ['srtio3', 'srxti1-xo3']:
        formatedStackElement = 'SrTiO3'
    elif stackElement.lower() in ['surlyn']:
        formatedStackElement = 'Surlyn'
    elif stackElement.lower() in ['sw-c-nt', 'swcnt', 'swcnts', 'swnts']:
        formatedStackElement = 'SWCNTs'

    elif stackElement.lower() in ['ti foil', 'ti-foil']:
        formatedStackElement = 'Ti-foil'
    elif stackElement.lower() in ['tio2', 'tio2x', 'tiox']:
        formatedStackElement = 'TiO2'
    elif stackElement.lower() in ['bk-tio2', 'bl-tio2', 'c tio2', 'c-tio', 'c-tio2', 'cp-tio2', 'ctio', 'ctio2', 'd-tio2', 'tio-c', 'tio2 - c', 'tio2 -c', 'tio2-b', 'tio2-bl', 'tio2-c', 'tio2-cp', 'tio2c', 'tiox-c']:
        formatedStackElement = 'TiO2-c'
    elif stackElement.lower() in ['tio2-mp', 'tio2- mp', 'tio2 - mp', 'm-tio2', 'mp-tio2', 'ml-tio2', 'tio2 nps', 'tio2-m', 'tio2mp', 'tio2 mp', 'tio2 -m', 'meso-tio2', 'tio2 nanoporous', 'tio2 meso', 'tio2 m', 'm- tio2', 'mtio2']:
        formatedStackElement = 'TiO2-mp'
    elif stackElement.lower() in ['tio2-io', 'tio2 invers opal']:
        formatedStackElement = 'TiO2-IO'
    elif stackElement.lower() in ['tio2 nfs', 'tio2-nfs', 'tio2-nanofibres']:
        formatedStackElement = 'TiO2-nanofibres'
    elif stackElement.lower() in ['np- tio2', 'np-tio2', 'tio2 nanocrystals', 'tio2 nanoparticles', 'tio2-nanoparticles', 'tio2 np', 'tio2-np', 'tio2-nps']:
        formatedStackElement = 'TiO2-np'
    elif stackElement.lower() in ['tio2 nanosheet', 'tio2 nanosheets', 'tio2-nanosheet', 'tio2-nanosheets', 'tio2-ns']:
        formatedStackElement = 'TiO2-ns'
    elif stackElement.lower() in ['nt-tio2', 'tio2 nanotube', 'tio2 nanotubes', 'tio2-nanotube', 'tio2-nanotubes', 'tio2-nt']:
        formatedStackElement = 'TiO2-nt'
    elif stackElement.lower() in ['nanorods-tio2', 'tio2 nanorod', 'tio2 nanorod array', 'tio2 nanorod arrays', 'tio2 nanorods', 'tio2 nanowires', 'tio2 nr', 'tio2 nrs', 'tio2 nws', 'tio2-na', 'tio2-nanocolumns', 'tio2-nanorod', 'tio2-nanorods', 'tio2-nanowire', 'tio2-nanowires', 'tio2-nr', 'tio2-nrs', 'tio2-nws']:
        formatedStackElement = 'TiO2-nw'

    elif stackElement.lower() in ['mp-zn2sno4', 'zn2sno4-mp']:
        formatedStackElement = 'Zn2SnO4-mp' 
    elif stackElement.lower() in ['zno']:
        formatedStackElement = 'ZnO'
    elif stackElement.lower() in ['c-zno', 'zno-c']:
        formatedStackElement = 'ZnO-c'
    elif stackElement.lower() in ['npzno', 'zno np', 'zno nps', 'zno-np', 'zno-nps']:
        formatedStackElement = 'ZnO-np'
    elif stackElement.lower() in ['nr- zno', 'nr-zno', 'zno nanorod', 'zno nanorods', 'zno nanowire', 'zno nanowires', 'zno nr', 'zno nrs', 'zno-nanorod', 'zno-nanorods', 'zno-nanowire ', 'zno-nanowires', 'zno-nr', 'zno-nrs']:
        formatedStackElement = 'ZnO-nw'
    elif stackElement.lower() in ['zno qd', 'zno qds', 'zno-qd', 'zno-qds']:
        formatedStackElement = 'ZnO-QDs'
    elif stackElement.lower() in ['m-zro2', 'zro-mp', 'zro2-m ', 'zro2-mp']:
        formatedStackElement = 'ZrO2-mp'

    elif stackElement.lower() in ['willow glass', 'corning willow glass', 'wg']:
        formatedStackElement = 'Willow glass'
    elif stackElement.lower() in ['wox']:
        formatedStackElement = 'WOx'  

    # If no known formating variations
    else: 
        formatedStackElement = stackElement

    return formatedStackElement

def stackSequenceForSealing(userData):
    ''' Format stack sequences '''
    stack = []
    for k, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove startin gand ending blank spaces
            item = item.strip()

            # Replace nan with emty strings
            if item.lower() == 'nan':
                item = ''

            # Split on |
            itemList = item.split('|')

            for i, stackElement in enumerate(itemList):
                # Remove blank spaces
                stackElement = stackElement.strip()

                # Enforse proper formating (based on the variations I have seen)
                itemList[i] = stackSequenceFormating(stackElement)

            # Concatenate all parts with proper spacing
            item = " | ".join(itemList)

            stack.append(item)
        except:
            stack.append(item)
            print(f'Could not process stackSequence {item} on line {k}')

    return stack

def stringToNumberAndUnit(string):
    '''Takes a string that is suposed to contain a number followed by a unit 
    and returns the number (as a string) and the unit (as a string)'''
    
    # Enforce that input is a string 
    string = str(string)

    # Enfors the use of decimal point
    string = string.replace(',', '.')

    # Remove leading and tailing blank spaces
    string = string.strip()    

    numeric = '-0123456789.'
    
    # Separate out the number
    j = 0
    for i, caracter in enumerate(string):
        if caracter not in numeric:
            break
        j = j+1
    number = string[:j]

    # Separate out the unit
    unit = string[j:].strip() 

    return number, unit

def supplier(userData):
    '''Format the string describing the supplier for the chemcials'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several solvents/chemicals separted by ;
    supplierList = []

    for item in userData:
        try:
            # Enforce that input is a string 
            item = str(item)

            # Remove leading and tailing blank spaces
            item = item.strip()

            # Change from notation of mixtures to notation of lists
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    suppliers = depositionStep.split(';')

                    for k, supplier in enumerate(suppliers):
                        # Enforse proper formating
                        suppliers[k] = supplierFormating(supplier)

                    depositionSteps[j] = '; '.join(suppliers)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            supplierList.append(item)
        except:
            print(f'faild to extract supplier of {item} on row {i}')
            supplierList.append(item)

    return supplierList

def supplierFormating(supplier):
    ''' Check suppliers againast known formating variations 
    and return the standard formating for the supplier'''

    # Remove starting and ending blank spaces
    supplier = supplier.strip()

    # Go through all known formating variations and convert them to the corect one
    if False:   # To start the elif cascade
        Print(f'Problem in elif cascade in atmosphereFormating')
  
    elif supplier.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        supplier = 'Unknown'

    return supplier

def temperature(userData):
    '''Format the volumes'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several compounds in the solution separted by ;

    amounts = []
    for item in userData:
        try:
            # Enforce input is a string 
            item = str(item)   

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Enforse the use of corect separator
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    compounds = depositionStep.split(';')

                    for k, compound in enumerate(compounds):
                        # Enforse proper formating
                        compounds[k] = temperatureFormating(compound)

                    depositionSteps[j] = '; '.join(compounds)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            amounts.append(item)
        except:
            amounts.append('')
            print(f'Cound not read in temperature on line: {i}')

    return amounts
  
def temperatureFormating(temperature):
    ''' Check volumes againast known formating variations 
    and return the standard formating for the concentration
    Acording to instructions, volumes should be stated in ml without a unit, but if someone should give units this rutines deals with that'''

    # Remove all blank spaces
    temperature = temperature.replace(' ','')

    # If not stated
    if temperature.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'Unknown'

    # Separate out the number from the unit (and there should be no unit)
    number, unit = stringToNumberAndUnit(temperature)
  
    return number

def thickness(userData, givenUnit, desiredUnit):
    '''Format Thickesses'''
    # For each item, there may be several layers separated by |
    thickesses = []
    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Enforse proper formating
                layers[i] = thickessesFormating(layer, givenUnit, desiredUnit)

            item = " | ".join(layers)
             
            thickesses.append(item)
        except:
            print(f'Failed to process: thickesses for {item} on row {i}')
            thickesses.append(item)

    return thickesses

def thickness_corection(userData):
    '''Cleaning function used only for coreting data already in the database '''
    thickesses = []
    for i, item in enumerate(userData):
        try:
            # Enforce that input is a string 
            item = str(item)
        
            # Remove blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Split on |
            layers = item.split('|')

            # Go trough each layer, and set np.nan for missing values
            for j, element in enumerate(layers):

                # Separate numbers from units
                number, unit = stringToNumberAndUnit(element)

                # If given corectly as a float
                if is_number(number):
                    layers[j] = str(float(number))
                else:
                    layers[j] = str(np.nan)

            item = " | ".join(layers)
             
            thickesses.append(item)
        except:
            print(f'Failed to process: thickesses for {item} on row {i}')
            thickesses.append(item)

    return thickesses

def thickessesFormating(string, givenUnit, desiredUnit):
    ''' Check thicknesses againast known formating variations 
    and return the standard formating for the thickness
    Acording to instructions, thickness should be stated in nm without a unit, but if someone should give units this rutines deals with that'''

    # Remove all blank spaces
    string = string.replace(' ','')

    # If not stated
    if string.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'nan'

    # Separate out the number from the unit
    number, userUnit = stringToNumberAndUnit(string)
  
    # Convert from givenUnit to desiredUnit. Uses nm as base unit
    if givenUnit == 'µm':
        conversionFactorGiven = 1000
    elif givenUnit == 'mm':
        conversionFactorGiven = 1000000
    else:
        conversionFactorGiven = 1

    if desiredUnit == 'µm':
        conversionFactorDesired = 1/1000
    elif desiredUnit == 'mm':
        conversionFactorDesired = 1/1000000
    else:
        conversionFactorDesired = 1

    if userUnit.lower() in ['µm', 'micro meter', 'micrometer', 'micrometre']:
        userUnit = 'µm'
        conversionFactorUser = 1000
    elif userUnit.lower() in ['mm']:
        userUnit = 'mm'
        conversionFactorUser = 1000000
    else:    
        conversionFactorUser = 1

    # Combined conversion factor
    conversionFactor = conversionFactorGiven*conversionFactorDesired*conversionFactorUser  
    number = str(float(number)*conversionFactor)

    return number

def time_corection(userData):
    '''Format the times '''
    # Cleaning function used only for coreting data already in the database

    amounts = []
    for item in userData:
        try:
            # Enforce input is a string 
            item = str(item)   

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Enforse the use of corect separator
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    compounds = depositionStep.split(';')

                    for k, compound in enumerate(compounds):
                        # Enforse proper formating
                        # Separate numbers from units
                        number, unit = stringToNumberAndUnit(compound)

                        compounds[k] = number

                    depositionSteps[j] = '; '.join(compounds)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            amounts.append(item)
        except:
            amounts.append('')
            print(f'Cound not read in volumes on line: {i}')

    return amounts

def time(userData, givenUnit, desiredUnit):
    '''Format the times'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several times separted by ;

    amounts = []
    for item in userData:
        try:
            # Enforce input is a string 
            item = str(item)   

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Enforse the use of corect separator
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    compounds = depositionStep.split(';')

                    for k, compound in enumerate(compounds):
                        # Enforse proper formating
                        compounds[k] = timeFormating(compound, givenUnit, desiredUnit)

                    depositionSteps[j] = '; '.join(compounds)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            amounts.append(item)
        except:
            amounts.append('')
            print(f'Cound not read in volumes on line: {i}')

    return amounts
  
def timeFormating(time, givenUnit, desiredUnit):
    ''' Check times againast known formating variations 
    and return the standard formating for the time'''

    # Remove all blank spaces
    time = time.replace(' ','')

    # If not stated
    if time.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'Unknown'

    # Separate out the number from the unit
    number, userUnit = stringToNumberAndUnit(time)

    if is_number(number) == False:
        return 'Unknown'
  
    # Convert from givenUnit to desiredUnit. Uses h as base unit
    if givenUnit == 's':
        conversionFactorGiven = 1/3600
    elif givenUnit == 'min':
        conversionFactorGiven = 1/60
    elif givenUnit == 'h':
        conversionFactorGiven = 1
    elif givenUnit == 'days':
        conversionFactorGiven = 24
    else:
        conversionFactorGiven = 1

    if desiredUnit == 's':
        conversionFactorDesired = 3600
    elif desiredUnit == 'min':
        conversionFactorDesired = 60
    elif desiredUnit == 'h':
        conversionFactorDesired = 1
    elif desiredUnit == 'days':
        conversionFactorDesired = 1/24
    else:
        conversionFactorDesired = 1

    if userUnit.lower() in ['s', 'second']:
        userUnit = 's'
        conversionFactorUser = 1/3600
    elif userUnit.lower() in ['min', 'm', 'mm', 'minute']:
        userUnit = 'min'
        conversionFactorUser = 1/60
    elif userUnit.lower() in ['h', 'hour', 'hours']:
        userUnit = 'h'
        conversionFactorUser = 1
    elif userUnit.lower() in ['days', 'day', 'd']:
        userUnit = 'days'
        conversionFactorUser = 24
    else:    
        conversionFactorUser = 1

    # Combined conversion factor
    conversionFactor = conversionFactorGiven*conversionFactorDesired*conversionFactorUser  
    number = str(float(number)*conversionFactor)

    return number

def titleCaseString(userData):
    '''Returns list of strings with title case'''
    string = []
    for item in userData:
        # Enforce that input is a string with title case
        item = str(item).title().strip()
                  
        if item.lower() == 'nan':
            item = ''

        string.append(item)

    return string

def trueOrFalse(userData):
    '''Check if the values in the column are True or not'''
    asessment = []
    for item in userData:
        # Enforce input as a string 
        item = str(item)

        # Remove starting and ending blank spaces
        item = item.strip()

        # Check for true or false
        answer = trueOrFalseListElement(item) 

        asessment.append(answer)     
    return asessment

def trueOrFalseList(userData):
    '''Bolean string list separated by | with false as default'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several elemets separated by ;
    asessment = []
    for item in userData:
        try:
            # Enforce input as a string 
            item = str(item)

            # Remove starting and ending blank spaces
            item = item.strip()

            # List notation rather than mixing notation
            item = item.replace(':', ';')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on ;
                boleans = layer.split(';')

                for j, bolean in enumerate(boleans):
                    # Enforse proper formating
                    boleans[j] = str(trueOrFalseListElement(bolean))
                
                # Concatenate additives for each layer with proper spacing
                layers[i] = "; ".join(boleans)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)

            asessment.append(item)
        except:
            asessment.append('')
            print(f'Cound not read in trueOrFalseList')

    return asessment

def trueOrFalseListElement(boleanString):
    '''Check if a string represent True or False with False as default '''
    
    # Remove starting and ending blank spaces
    boleanString = boleanString.strip()

    if boleanString.lower() in ['true', 'yes', 'y', '1', '1.0']:
        return True
    else:
        return False

def trueOrFalseOrEmty(userData):
    '''Check if the values in the column are True or not'''
    asessment = []
    for item in userData:
        # Enforce that input is a string
        item = str(item).strip()
                  
        if item.lower() in ['true', 'yes', 'y', '1', '1.0']:
            asessment.append(True)
        elif item.lower() in ['false', 'no', 'n', '0']:
            asessment.append(False)
        else:
            asessment.append('')
            
    return asessment

def VocData(userData, mV_to_V_cutoff = 10):
    '''Format Voc data
        Voc should be stated in V but is sometimes stated in mV
        If the given values is larger than an abritray value of mV_to_V_cutoff, the
        value is asumed to be stated in mV and is converted to V'''

    values = []
    for item in userData:
        try:
            # To make it simple, the imput is converted to a string (regardless if it is or not)
            item = str(item)

            # Remove all blank spaces
            item = item.strip().replace(" ","")

            # Enfors the use of decimal point
            item = item.replace(',', '.')

            # Separate the number from the unit (which should not be there)
            number, unit = stringToNumberAndUnit(item)

            # Convert number in string reprecentation to a float
            number = convertToFloat(number)

            # Check if conversion to V should be done
            if float(number) > mV_to_V_cutoff:
                number = number/1000

            # Round to the third decimal place
            number = np.around(number, decimals = 3)

            values.append(number)
        except:
            values.append(np.nan)
            print(f'Could not process VocData {item} on line {i}')
    return values

def volumes(userData, givenUnit, desiredUnit):
    '''Format the volumes'''
    # For each item, there may be several layers separated by |
    # For each layer, there may be several depostion proceadures separatd by >>
    # For each deposition proceadures, there may be several compounds in the solution separted by ;

    amounts = []
    for item in userData:
        try:
            # Enforce input is a string 
            item = str(item)   

            # Enforse the use of decimal point
            item = item.replace(',', '.')

            # Split on |
            layers = item.split('|')

            for i, layer in enumerate(layers):
                # Split on >>
                depositionSteps = layer.split('>>')

                for j, depositionStep in enumerate(depositionSteps):
                    # Split on ;
                    compounds = depositionStep.split(';')

                    for k, compound in enumerate(compounds):
                        # Enforse proper formating
                        compounds[k] = volumesFormating(compound, givenUnit, desiredUnit)

                    depositionSteps[j] = '; '.join(compounds)

                # Concatenate all parts with proper spacing
                layers[i] = ' >> '.join(depositionSteps)

            # Concatenate all layers with proper spacing
            item = " | ".join(layers)
           
            amounts.append(item)
        except:
            amounts.append('')
            print(f'Cound not read in volumes on line: {i}')

    return amounts
  
def volumesFormating(volume, givenUnit, desiredUnit):
    ''' Check volumes againast known formating variations 
    and return the standard formating for the concentration
    Acording to instructions, volumes should be stated in ml without a unit, but if someone should give units this rutines deals with that'''

    # Remove all blank spaces
    volume = volume.replace(' ','')

    # If not stated
    if volume.lower() in  ['', 'unknown', 'non', 'none', 'nan', 'na', '-', 'np.nan']:
        return 'Unknown'

    # Separate out the number from the unit
    number, userUnit = stringToNumberAndUnit(volume)

    if is_number(number) == False:
        return 'Unknown'
  
    # Convert from givenUnit to desiredUnit. Uses ml as base unit
    if givenUnit == 'µl':
        conversionFactorGiven = 1/1000
    elif givenUnit == 'l':
        conversionFactorGiven = 1000
    else:
        conversionFactorGiven = 1

    if desiredUnit == 'µl':
        conversionFactorDesired = 1000
    elif desiredUnit == 'l':
        conversionFactorDesired = 1/1000
    else:
        conversionFactorDesired = 1

    if userUnit.lower() in ['µl', 'micro litre', 'microlitre', 'microliter']:
        userUnit = 'µl'
        conversionFactorUser = 1/1000
    elif userUnit.lower() in ['l']:
        userUnit = 'ml'
        conversionFactorUser = 1000
    else:    
        conversionFactorUser = 1

    # Combined conversion factor
    conversionFactor = conversionFactorGiven*conversionFactorDesired*conversionFactorUser  
    number = str(float(number)*conversionFactor)

    return number


# Functions in extraction protocoll version 4 and before


###################################################################################################
#%% Unused functions
#%% Substrate
# replaced with stackSequence
def substrate(userData):
    '''Format the substrate text string '''
    substrate = []

    for item in userData:
        # Enforce that input is a string 
        item = str(item)
        
        # Remove blank spaces
        item = item.strip().replace(" ","")

        # Split on |
        itemList = item.split('|')

        # Enforce upper case for SLG, FTO, ITO, PET, AZO
        for i, element in enumerate(itemList):
            if element.upper() == 'SLG':
                itemList[i] = 'SLG'
            if element.upper() == 'FTO':
                itemList[i] = 'FTO'
            if element.upper() == 'ITO':
                itemList[i] = 'ITO'
            if element.upper() == 'AZO':
                itemList[i] = 'AZO'
            if element.upper() == 'PET':
                itemList[i] = 'PET'

        # Concatenate all parts with proper spacing
        item = " | ".join(itemList)

        # Add the substrate to the list
        substrate.append(item)

    return substrate

#%% Cell stack
# replaced with stackSequence
def stack(userData):
    '''Format the text string describing the cell stack '''
    stack = []
    for item in userData:
        # Enforce that input is a string 
        item = str(item)
        
        # Remove blank spaces
        item = item.strip().replace(" ","")

        # Split on |
        itemList = item.split('|')

        # Enforse proper formating (based on the variations I have seen)
        for i, element in enumerate(itemList):
            if element.upper() == 'SLG':
                itemList[i] = 'SLG'
            if element.upper() == 'FTO':
                itemList[i] = 'FTO'
            if element.upper() == 'ITO':
                itemList[i] = 'ITO'
            if element.upper() == 'AZO':
                itemList[i] = 'AZO'
            if element.upper() == 'PET':
                itemList[i] = 'PET'
            if element.upper() == 'BCP':
                itemList[i] = 'BCP'
            if element.lower() == 'perovskite':
                itemList[i] = 'Perovskite'
            if element.lower() == 'spiro':
                itemList[i] = 'Spiro-MeOTAD'
            if element.upper() == 'PCBM':
                itemList[i] = 'PCBM-60'
            if element.upper() == 'PCBM-70':
                itemList[i] = 'PCBM-70'
            if element.upper() == 'PCBM70':
                itemList[i] = 'PCBM-70'
            if element.lower() == 'polytpd':
                itemList[i] = 'PolyTPD'
            if element.lower() == 'pedot:pss':
                itemList[i] = 'PEDOT:PSS'
            if element.upper() == 'PTAA':
                itemList[i] = 'PTAA'

        # Concatenate all parts with proper spacing
        item = " | ".join(itemList)

        stack.append(item)

    return stack

#%% Cell area
def area(userData, defaultArea):
    '''Format the cell area. defaultArea in cm^2 '''
    area = []
    for i, item in enumerate(userData):
        # To make it simple the imput is converted to a string (regardless if it is or not)
        item = str(item)

        # Enfors the use of decimal point
        item.replace(',', '.')

        # If given corectly as a float
        if is_number(item):
            area.append(float(item))
        # If not given corectly or missing, set area as defaultArea
        else:
            area.append(defaultArea)

        # Replace NaN with defaultArea
        if np.isnan(area[i]):
            area[i] = defaultArea

    return area

    return area

#%% Module area
def moduleArea(userData):
    '''The area in cm^2 of the module '''
    moduleArea = []
    for i, item in enumerate(userData):
        # To make it simple the imput is converted to a string (regardless if it is or not)
        item = str(item)

        # Enfors the use of decimal point
        item.replace(',', '.')

        # If given corectly
        if is_number(item):
            moduleArea.append(float(item))
        # If not given corectly or missing, set is as an empty string
        else:
            moduleArea.append('')

        # Replace NaN with an empty string
        if np.isnan(moduleArea[i]):
            moduleArea[i] = ''

    return moduleArea

#%% Encapsulation materials; Edge sealing materias
# replaced with stackSequence
def encapsulationMaterials(userData):
    '''The stack sequence for the encapsulation materials'''
    stack = []
    for item in userData:
        # Enforce that input is a string 
        item = str(item)

        # Remove leading and tailing blank spaces
        item = item.strip()

        # Split on |
        itemList = item.split('|')

        # Enforse proper formating (based on the variations I have seen)
        for i, element in enumerate(itemList):
            if element.upper() == 'SLG':
                itemList[i] = 'SLG'
            if element.lower() == 'glass':
                itemList[i] = 'Glass'
            if element.lower() == 'polymer':
                itemList[i] = 'Polymer'
            if element.lower() == 'epoxy':
                itemList[i] = 'Epoxy'
            if element.lower() == 'barrier foil':
                itemList[i] = 'Barrier foil'
            if element.lower() == 'surlyn':
                itemList[i] = 'Surlyn'
            if element.lower() == 'nan':
                itemList[i] = ''
        
        # Concatenate all parts with proper spacing
        item = " | ".join(itemList)

        stack.append(item)

    return stack

#%% synthesisAtmosphere
def synthesisAtmosphere(userData):
    '''Format the syntesis atmosphere'''
    atmosphere = []

    for item in userData:
        # Enforce that input is a string 
        item = str(item)
        
        # Remove blank spaces
        item = item.strip().replace(" ","")

        # Split on |
        itemList = item.split('|')

        for element in itemList:
            if element.lower() == 'air':
                element = 'Air'
            if element.lower() == 'dryair':
                element = 'Dry air'
            if element.lower() == 'vacuum':
                element = 'Vaccum'
            if 'air' in element:
                element.replace('air', 'Air')

        # Concatenate all parts with proper spacing
        item = " | ".join(itemList)

        atmosphere.append(item)
    return atmosphere

#%% Simple list with | spacing
def barSpacedList(userData):
    data = []
    for item in userData:
        # Enforce that input is a string 
        item = str(item)
        
        # Remove blank spaces
        item = item.strip().replace(" ","")

        # Split on |
        itemList = item.split('|')

        # Concatenate all parts with proper spacing
        item = " | ".join(itemList)

        data.append(item)
    return data

#%% ETL stack
def eTLStack(userData):
    ''' Format the ETH stack '''
    data = []
    for item in userData:
        # Enforce that input is a string 
        item = str(item)
        
        # Remove blank spaces
        item = item.strip()

        # Replace empty strings with non
        if element == '':
            element = 'non'

        # Split on |
        itemList = item.split('|')

        for stackElement in itemList:
            # Remove starting and ending blank spaces
            stackElement = stackElement.strip()

            # Enforse proper formating (based on the variations I have seen)
            stackElement = stackElementFormating(stackElement)

        # Concatenate all parts with proper spacing
        item = " | ".join(itemList)

        data.append(item)
    return data

