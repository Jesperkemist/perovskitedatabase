# =============================================================================
# cleanUserData
# Accepting a pandas datafram with user data
# returns a datafram with cleaned and formated data
#
# Jesper Jacobsson
# 2020 05
# =============================================================================

import os
import numpy as np
import pandas as pd

#import CleanDataFunctions as cdf
import UtilityFunctions.CleanDataFunctions as cdf


def cleanUserData(userData, fileName):
    '''Takes a pandas datafram with user data and return a datafram with formated data. 
    Targets Extraction protocoll version 5.3'''
    
    print(f'Initiated data cleaning procedure for {fileName}')

    #%% Correct formating errors in the column names of the data template
    try:
        userData.columns = cdf.dataColumnFormating(list(userData.columns))
    except:           
        print(f'Faild with dataColumnFormating')

    #%% Initiate an empty datafram to fill with cleaned data
    data = pd.DataFrame()

    #%% Ref_ID_temp
    data['Ref_ID_temp'] = list(range(1,len(userData) + 1))

    #%% Ref. Name of person entering the data
    try:
        data['Ref_name_of_person_entering_the_data'] = cdf.responsiblePerson(userData['Ref. Name of person entering the data'])
    except:           
        print(f'Cound not read in: Ref. Name of person entering the data from: {fileName}')
        data['Ref_name_of_person_entering_the_data'] = '' 

    #%% Ref. Data entered by author
    try:
        data['Ref_data_entered_by_author'] = cdf.trueOrFalse(userData['Ref. Data entered by author [TRUE/FALSE]'])
    except:           
        print(f'Cound not read in: Ref. Data entered by author [TRUE/FALSE]')
        data['Ref_data_entered_by_author'] = ''

    #%% Ref. DOI number
    try:
        data['Ref_DOI_number'] = cdf.doiNumbers(userData['Ref. DOI number'])
    except:           
        print(f'Cound not read in: Ref. DOI number from: {fileName}')
        data['Ref_DOI_number'] = ''

    #%% Ref. Lead Author
    try:
        # Will later be chcked against crossref with the DOI number
        data['Ref_lead_author'] = list(userData['Ref. Lead author'])
    except:
        print(f'Cound not read in: Ref. Lead author from: {fileName}')
        data['Ref_lead_author'] = ''

    #%% Ref. Publication date [year:mm:dd]
    try:
        # Will later be checked against crossref with the DOI number
        data['Ref_publication_date'] = list(userData['Ref. Publication date [year:mm:dd]'])
    except:
        print(f'Cound not read in: Ref. Publication date [year:mm:dd] from: {fileName}')
        data['Ref_publication_date'] = pd.to_datetime('')

    #%% Ref. Free text comment (max 280 characters)
    try:
        data['Ref_free_text_comment'] = cdf.convertToString(userData['Ref. Free text comment (max 280 characters)'])
    except: 
        print(f'Cound not read in: Ref. Free text comment (max 280 characters) from: {fileName}')
        data['Ref_free_text_comment'] = ''

    #%% Ref. Internal sample ID [free text]
    try:
        data['Ref_internal_sample_id'] = cdf.convertToString(userData['Ref. Internal sample ID [free text]'])
    except: 
        print(f'Cound not read in: Ref. Internal sample ID [free text] from: {fileName}')
        data['Ref_internal_sample_id'] = ''

    #%% Cell. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Cell_stack_sequence'] = cdf.stackSequence(userData['Cell. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Cell. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Cell_stack_sequence'] = ''

    #%% Cell. Area. Total [cm^2]
    try:
        data['Cell_area_total'] = cdf.numericValues(userData['Cell. Area. Total [cm^2]'])
    except:
        print(f'Cound not read in: Cell. Area. Total [cm^2] from: {fileName}')
        data['Cell_area_total'] = ''
        
    #%% Cell. Area. Measured [cm^2]
    try:
        data['Cell_area_measured'] = cdf.numericValues(userData['Cell. Area. Measured [cm^2]'])
    except:
        print(f'Cound not read in: Cell. Area. Measured [cm^2] from: {fileName}')
        data['Cell_area_measured'] = ''

    #%% Cell. Number of cells per substrate
    try:
        data['Cell_number_of_cells_per_substrate'] = cdf.numericInteger(userData['Cell. Number of cells per substrate'], default = 0)
    except:
        print(f'Cound not read in: Cell. Number of cells per substrate from: {fileName}')
        data['Cell_number_of_cells_per_substrate'] = ''

    #%% Cell. Architecture [nip/pin/ …]
    try:
        data['Cell_architecture'] = cdf.architecture(userData['Cell. Architecture [nip/pin/ …]'])
    except: 
        print(f'Cound not read in: Cell. Architecture [nip/pin/ …] from: {fileName}')
        data['Cell_architecture'] = ''

    #%% Cell. Flexible [TRUE/FALSE]
    try:
        data['Cell_flexible'] = cdf.trueOrFalse(userData['Cell. Flexible [TRUE/FALSE]'])
    except:
        print(f'Cound not read in: Cell. Flexible [TRUE/FALSE] from: {fileName}')
        data['Cell_flexible'] = ''

    #%% Cell. Flexible. Minimum bending radius [cm]
    try:
        data['Cell_flexible_min_bending_radius'] = cdf.numericValues(userData['Cell. Flexible. Minimum bending radius [cm]'])
    except:
        print(f'Cound not read in: Cell. Flexible. Minimum bending radius [cm] from: {fileName}')
        data['Cell_flexible_min_bending_radius'] = ''

    #%% Cell. Semitransparent [TRUE/FALSE]
    try:
        data['Cell_semitransparent'] = cdf.trueOrFalse(userData['Cell. Semitransparent [TRUE/FALSE]'])
    except:
        print(f'Cound not read in: Cell. Semitransparent [TRUE/FALSE] from: {fileName}')
        data['Cell_semitransparent'] = ''      

    #%% Cell. Semitransparent. Average visible transmittance [%]
    try:
        data['Cell_semitransparent_AVT'] = cdf.numericValues(userData['Cell. Semitransparent. Average visible transmittance [%]'])
    except:
        print(f'Cound not read in: Cell. Semitransparent. Average visible transmittance [%] from: {fileName}')
        data['Cell_semitransparent_AVT'] = ''

    #%% Cell. Semitransparent. Average visible transmittance. Wavelength range [lambda_min; lambda_max]
    try:
        data['Cell_semitransparent_wavelength_range'] = cdf.numberHighLowOrConstant(userData['Cell. Semitransparent. Average visible transmittance. Wavelength range [lambda_min; lambda_max]'])
    except: 
        print(f'Cound not read in: Cell. Semitransparent. Average visible transmittance. Wavelength range [lambda_min; lambda_max] from: {fileName}')
        data['Cell_semitransparent_wavelength_range'] = ''
   
    #%% Cell. Semitransparent. Transmittance. Link. Raw data
    try:
        data['Cell_semitransparent_raw_data'] = cdf.convertToString(userData['Cell. Semitransparent. Transmittance. Link. Raw data'])
    except: 
        print(f'Cound not read in: Cell. Semitransparent. Transmittance. Link. Raw data from: {fileName}')
        data['Cell_semitransparent_raw_data'] = '' 

    #%% Module [TRUE/FALSE]
    try:
        data['Module'] = cdf.trueOrFalse(userData['Module [TRUE/FALSE]'])
    except:
        print(f'Cound not read in: Module [TRUE/FALSE] from: {fileName}')
        data['Module'] = ''  

    #%% Module. Number of cells in module
    try:
        data['Module_number_of_cells_in_module'] = cdf.numericInteger(userData['Module. Number of cells in module'], default = 0)
    except:
        print(f'Cound not read in:Module. Number of cells in module: {fileName}')
        data['Module_number_of_cells_in_module'] = ''

    #%% Module. Area. Total [cm^2] 
    try:
        data['Module_area_total'] = cdf.numericValues(userData['Module. Area. Total [cm^2]'])
    except:
        print(f'Cound not read in: Module. Area. Total [cm^2] from: {fileName}')
        data['Module_area_total'] = ''

    #%% Module. Area. Effective [cm^2]
    try:
        data['Module_area_effective'] = cdf.numericValues(userData['Module. Area. Effective [cm^2]'])
    except:
        print(f'Cound not read in: Module. Area. Effective [cm^2] from: {fileName}')
        data['Module_area_effective'] = ''

    #%% Module. JV data recalculated per cell [TRUE/FALSE]
    try:
        data['Module_JV_data_recalculated_per_cell'] = cdf.trueOrFalse(userData['Module. JV data recalculated per cell [TRUE/FALSE]'])
    except:
        print(f'Cound not read in: Module. JV data recalculated per cell [TRUE/FALSE] from: {fileName}')
        data['Module_JV_data_recalculated_per_cell'] = '' 

    #%% Substrate. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Substrate_stack_sequence'] = cdf.stackSequence(userData['Substrate. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Substrate. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Substrate_stack_sequence'] = ''

    #%% Substrate. Thickness. [Th.1 | Th.2 | … | Th.n ] [mm]
    try:
        data['Substrate_thickness'] = cdf.thickness(userData['Substrate. Thickness [Th.1 | Th.2 | … | Th.n ] [mm]'], givenUnit = 'mm', desiredUnit = 'mm')
    except: 
        print(f'Cound not read in: Substrate. Thickness [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['Substrate_thickness'] = ''

    #%% Substrate. Area [cm^2]
    try:
        data['Substrate_area'] = cdf.numericValues(userData['Substrate. Area [cm^2]'])
    except:
        print(f'Cound not read in: Substrate. Area [cm^2] from: {fileName}')
        data['Substrate_area'] = ''

    #%% Substrate. Supplier
    try:
        data['Substrate_supplier'] = cdf.convertToString(userData['Substrate. Supplier'])
    except: 
        print(f'Cound not read in: Substrate. Supplier from: {fileName}')
        data['Substrate_supplier'] = ''

    #%% Substrate. Brand name
    try:
        data['Substrate_brand_name'] = cdf.convertToString(userData['Substrate. Brand name'])
    except: 
        print(f'Cound not read in: Substrate. Brand name from: {fileName}')
        data['Substrate_brand_name'] = ''

    #%% Substrate. Deposition procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['Substrate_deposition_procedure'] = cdf.depositionProcedure(userData['Substrate. Deposition procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Substrate. Deposition procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['Substrate_deposition_procedure'] = ''

    #%% Substrate. Surface roughness. Rms [nm]
    try:
        data['Substrate_surface_roughness_rms'] = cdf.numericValues(userData['Substrate. Surface roughness. Rms [nm]'])
    except:
        print(f'Cound not read in: Substrate. Surface roughness. Rms [nm] from: {fileName}')
        data['Substrate_surface_roughness_rms'] = ''

    #%% Substrate. Etching procedure
    try:
        data['Substrate_etching_procedure'] = cdf.convertToString(userData['Substrate. Etching procedure'])
    except: 
        print(f'Cound not read in: Substrate. Etching procedure from: {fileName}')
        data['Substrate_etching_procedure'] = ''

    #%% Substrate. Cleaning procedure
    try:
        data['Substrate_cleaning_procedure'] = cdf.convertToString(userData['Substrate. Cleaning procedure'])
    except: 
        print(f'Cound not read in: Substrate. Cleaning procedure from: {fileName}')
        data['Substrate_cleaning_procedure'] = ''

    #%% ETL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['ETL_stack_sequence'] = cdf.stackSequence(userData['ETL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: ETL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['ETL_stack_sequence'] = ''

    #%% ETL. Thickness [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['ETL_thickness'] = cdf.thickness(userData['ETL. Thickness [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: ETL. Thickness [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['ETL_thickness'] = ''

    #%% ETL. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]
    try:
        data['ETL_additives_compounds'] = cdf.dopandsAndAdditives(userData['ETL. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ] from: {fileName}')
        data['ETL_additives_compounds'] = ''

    #%% ETL. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]
    try:
        data['ETL_additives_concentrations'] = cdf.concentrations(userData['ETL. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]'])
    except: 
        print(f'Cound not read in: ETL. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...] from: {fileName}')
        data['ETL_additives_concentrations'] = ''

    #%% ETL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['ETL_deposition_procedure'] = cdf.depositionProcedure(userData['ETL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['ETL_deposition_procedure'] = ''
 
    #%% ETL. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]
    try:
        data['ETL_deposition_aggregation_state_of_reactants'] = cdf.aggregationStates(userData['ETL. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ] from: {fileName}')
        data['ETL_deposition_aggregation_state_of_reactants'] = ''

    #%% ETL. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['ETL_deposition_synthesis_atmosphere'] = cdf.atmosphere(userData['ETL. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['ETL_deposition_synthesis_atmosphere'] = ''

    #%% ETL. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['ETL_deposition_synthesis_atmosphere_pressure_total'] = cdf.pressure(userData['ETL. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['ETL_deposition_synthesis_atmosphere_pressure_total'] = ''

    #%% ETL. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['ETL_deposition_synthesis_atmosphere_pressure_partial'] = cdf.pressure(userData['ETL. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['ETL_deposition_synthesis_atmosphere_pressure_partial'] = ''

    #%% ETL. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]
    try:
        data['ETL_deposition_synthesis_atmosphere_relative_humidity'] = cdf.relativeHumidity(userData['ETL. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%] from: {fileName}')
        data['ETL_deposition_synthesis_atmosphere_relative_humidity'] = ''

    #%% ETL. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]
    try:
        data['ETL_deposition_solvents'] = cdf.solvents(userData['ETL. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ] from: {fileName}')
        data['ETL_deposition_solvents'] = ''

    #%% ETL. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]
    try:
        data['ETL_deposition_solvents_mixing_ratios'] = cdf.mixingRatios(userData['ETL. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ] from: {fileName}')
        data['ETL_deposition_solvents_mixing_ratios'] = ''

    #%% ETL. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['ETL_deposition_solvents_supplier'] = cdf.supplier(userData['ETL. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['ETL_deposition_solvents_supplier'] = ''

    #%% ETL. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['ETL_deposition_solvents_purity'] = cdf.purity(userData['ETL. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['ETL_deposition_solvents_purity'] = ''

    #%% ETL. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]
    try:
        data['ETL_deposition_reaction_solutions_compounds'] = cdf.compounds(userData['ETL. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...] from: {fileName}')
        data['ETL_deposition_reaction_solutions_compounds'] = ''

    #%% ETL. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['ETL_deposition_reaction_solutions_compounds_supplier'] = cdf.supplier(userData['ETL. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['ETL_deposition_reaction_solutions_compounds_supplier'] = ''

    #%% ETL. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['ETL_deposition_reaction_solutions_compounds_purity'] = cdf.purity(userData['ETL. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['ETL_deposition_reaction_solutions_compounds_purity'] = ''

    #%% ETL. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]
    try:
        data['ETL_deposition_reaction_solutions_concentrations'] = cdf.concentrations(userData['ETL. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...] from: {fileName}')
        data['ETL_deposition_reaction_solutions_concentrations'] = ''

    #%% ETL. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]
    try:
        data['ETL_deposition_reaction_solutions_volumes'] = cdf.volumes(userData['ETL. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]'], givenUnit = 'ml', desiredUnit = 'ml')
    except: 
        print(f'Cound not read in: ETL. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml] from: {fileName}')
        data['ETL_deposition_reaction_solutions_volumes'] = ''

    #%% ETL. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]
    try:
        data['ETL_deposition_reaction_solutions_age'] = cdf.time(userData['ETL. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: ETL. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h] from: {fileName}')
        data['ETL_deposition_reaction_solutions_age'] = ''

    #%% ETL. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['ETL_deposition_reaction_solutions_temperature'] = cdf.temperature(userData['ETL. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['ETL_deposition_reaction_solutions_temperature'] = ''

    #%% ETL. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['ETL_deposition_substrate_temperature'] = cdf.temperature(userData['ETL. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['ETL_deposition_substrate_temperature'] = ''

    #%% ETL. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['ETL_deposition_thermal_annealing_temperature'] = cdf.temperature(userData['ETL. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['ETL_deposition_thermal_annealing_temperature'] = ''

    #%% ETL. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]
    try:
        data['ETL_deposition_thermal_annealing_time'] = cdf.time(userData['ETL. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: ETL. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min] from: {fileName}')
        data['ETL_deposition_thermal_annealing_time'] = ''

    #%% ETL. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['ETL_deposition_thermal_annealing_atmosphere'] = cdf.atmosphere(userData['ETL. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: ETL. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['ETL_deposition_thermal_annealing_atmosphere'] = ''

    #%% ETL. Storage. Time until next deposition step [h]
    try:
        data['ETL_storage_time_until_next_deposition_step'] = cdf.numericValues(userData['ETL. Storage. Time until next deposition step [h]'])
    except: 
        print(f'Cound not read in: ETL. Storage. Time until next deposition_step [h] from: {fileName}')
        data['ETL_storage_time_until_next_deposition_step'] = ''

    #%% ETL. Storage. Atmosphere [Gas1; Gas2; ...]
    try:
        data['ETL_storage_atmosphere'] = cdf.atmosphere(userData['ETL. Storage. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: ETL. Storage. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['ETL_storage_atmosphere'] = ''

    #%% ETL. Storage. Relative humidity [%] 
    try:
        data['ETL_storage_relative_humidity'] = cdf.numericValues(userData['ETL. Storage. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: ETL. Storage. Relative humidity [%] from: {fileName}')
        data['ETL_storage_relative_humidity'] = ''

    #%% ETL. Surface treatment before next depositionstep 
    try:
        data['ETL_surface_treatment_before_next_deposition_step'] = cdf.convertToString(userData['ETL. Surface treatment before next deposition step'])
    except: 
        print(f'Cound not read in: ETL. Surface treatment before next deposition step from: {fileName}')
        data['ETL_surface_treatment_before_next_deposition_step'] = ''

    #%% Perovskite. Single crystal [TRUE/FALSE] 
    try:
        data['Perovskite_single_crystal'] = cdf.trueOrFalse(userData['Perovskite. Single crystal [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Single crystal [TRUE/FALSE] from: {fileName}')
        data['Perovskite_single_crystal'] = ''

    #%% Perovskite. Dimension. 0D (Quantum dot) [TRUE/FALSE] 
    try:
        data['Perovskite_dimension_0D'] = cdf.trueOrFalse(userData['Perovskite. Dimension. 0D (Quantum dot) [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Dimension. 0D (Quantum dot) [TRUE/FALSE] from: {fileName}')
        data['Perovskite_dimension_0D'] = ''

    #%% Perovskite. Dimension. 2D [TRUE/FALSE]
    try:
        data['Perovskite_dimension_2D'] = cdf.trueOrFalse(userData['Perovskite. Dimension. 2D [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Dimension. 2D [TRUE/FALSE] from: {fileName}')
        data['Perovskite_dimension_2D'] = ''

    #%% Perovskite. Dimension. 2D/3D mixture [TRUE/FALSE]
    try:
        data['Perovskite_dimension_2D3D_mixture'] = cdf.trueOrFalse(userData['Perovskite. Dimension. 2D/3D mixture [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Dimension. 2D/3D mixture [TRUE/FALSE] from: {fileName}')
        data['Perovskite_dimension_2D3D_mixture'] = ''

    #%% Perovskite. Dimension. 3D [TRUE/FALSE]
    try:
        data['Perovskite_dimension_3D'] = cdf.trueOrFalse(userData['Perovskite. Dimension. 3D [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Dimension. 23D [TRUE/FALSE] from: {fileName}')
        data['Perovskite_dimension_3D'] = ''

    #%% Perovskite. Dimension. 3D with 2D capping layer [TRUE/FALSE]
    try:
        data['Perovskite_dimension_3D_with_2D_capping_layer'] = cdf.trueOrFalse(userData['Perovskite. Dimension. 3D with 2D capping layer [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Dimension. 3D with 2D capping layer [TRUE/FALSE] from: {fileName}')
        data['Perovskite_dimension_3D_with_2D_capping_layer'] = ''

    #%% Perovskite. Dimension. List of layers [Dim.1 | Dim.2 | …]
    try:
        data['Perovskite. Dimension. List of layers'] = cdf.numberList(userData['Perovskite. Dimension. List of layers [Dim.1 | Dim.2 | …]'])
    except: 
        print(f'Cound not read in: Perovskite. Dimension. List of layers [Dim.1 | Dim.2 | …] from: {fileName}')
        data['Perovskite. Dimension. List of layers'] = ''

    #%% Perovskite. Composition. Perovskite ABC3 structure [TRUE/FALSE] 
    try:
        data['Perovskite_composition_perovskite_ABC3_structure'] = cdf.trueOrFalse(userData['Perovskite. Composition. Perovskite ABC3 structure [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. Perovskite ABC3 structure [TRUE/FALSE] from: {fileName}')
        data['Perovskite_composition_perovskite_ABC3_structure'] = ''

    #%% Perovskite. Composition. Perovskite inspired structure [TRUE/FALSE] 
    try:
        data['Perovskite_composition_perovskite_inspired_structure'] = cdf.trueOrFalse(userData['Perovskite. Composition. Perovskite inspired structure [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. Perovskite inspired structure [TRUE/FALSE] from: {fileName}')
        data['Perovskite_composition_perovskite_inspired_structure'] = ''

    #%% Perovskite. Composition. A-ions [Ion.1; Ion.2; … | Ion.3; … | ...]
    try:
        data['Perovskite_composition_a_ions'] = cdf.perovskiteIons(userData['Perovskite. Composition. A-ions [Ion.1; Ion.2; … | Ion.3; … | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. A-ions [Ion.1; Ion.2; … | Ion.3; … | ...] from: {fileName}')
        data['Perovskite_composition_a_ions'] = ''

    #%% Perovskite. Composition. A-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]
    try:
        data['Perovskite_composition_a_ions_coefficients'] = cdf.perovskiteCoefficients(userData['Perovskite. Composition. A-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. A-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...] from: {fileName}')
        data['Perovskite_composition_a_ions_coefficients'] = ''

    #%% Perovskite. Composition. B-ions [Ion.1; Ion.2; … | Ion.3; … | ...]
    try:
        data['Perovskite_composition_b_ions'] = cdf.perovskiteIons(userData['Perovskite. Composition. B-ions [Ion.1; Ion.2; … | Ion.3; … | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. B-ions [Ion.1; Ion.2; … | Ion.3; … | ...] from: {fileName}')
        data['Perovskite_composition_b_ions'] = ''

    #%% Perovskite. Composition. B-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]
    try:
        data['Perovskite_composition_b_ions_coefficients'] = cdf.perovskiteCoefficients(userData['Perovskite. Composition. B-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. B-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...] from: {fileName}')
        data['Perovskite_composition_b_ions_coefficients'] = ''

    #%% Perovskite. Composition. C-ions [Ion.1; Ion.2; … | Ion.3; … | ...]
    try:
        data['Perovskite_composition_c_ions'] = cdf.perovskiteIons(userData['Perovskite. Composition. C-ions [Ion.1; Ion.2; … | Ion.3; … | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. C-ions [Ion.1; Ion.2; … | Ion.3; … | ...] from: {fileName}')
        data['Perovskite_composition_c_ions'] = ''

    #%% Perovskite. Composition. C-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]
    try:
        data['Perovskite_composition_c_ions_coefficients'] = cdf.perovskiteCoefficients(userData['Perovskite. Composition. C-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. C-ions. Coefficients [Cof.1; Cof.2; … | Cof.3; … | ...] from: {fileName}')
        data['Perovskite_composition_c_ions_coefficients'] = ''

    #%% Perovskite. Composition. None-stoichiometry. Components in excess [Com.1; Com.2; … | Com.3; … | ...]
    try:
        data['Perovskite_composition_none_stoichiometry_components_in_excess'] = cdf.perovskiteIons(userData['Perovskite. Composition. None-stoichiometry. Components in excess [Com.1; Com.2; … | Com.3; … | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. None-stoichiometry. Components in excess [Com.1; Com.2; … | Com.3; … | ...] from: {fileName}')
        data['Perovskite_composition_none_stoichiometry_components_in_excess'] = ''

    #%% Perovskite. Composition. Assumption [Solution composition/Experimental verification/Literature/ …]
    try:
        data['Perovskite_composition_assumption'] = cdf.convertToString(userData['Perovskite. Composition. Assumption [Solution composition/Experimental verification/Literature/ …]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. Assumption [Solution composition/Experimental verification/Literature/ …]: {fileName}')
        data['Perovskite_composition_assumption'] = ''

    #%% Perovskite. Composition. Inorganic perovskite [TRUE/FALSE]
    try:
        data['Perovskite_composition_inorganic'] = cdf.trueOrFalse(userData['Perovskite. Composition. Inorganic perovskite [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. Inorganic perovskite [TRUE/FALSE] from: {fileName}')
        data['Perovskite_composition_inorganic'] = ''

    #%% Perovskite. Composition. Lead free [TRUE/FALSE]
    try:
        data['Perovskite_composition_leadfree'] = cdf.trueOrFalse(userData['Perovskite. Composition. Lead free [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. Lead free [TRUE/FALSE] from: {fileName}')
        data['Perovskite_composition_leadfree'] = ''

    #%% Perovskite. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]
    try:
        data['Perovskite_additives_compounds'] = cdf.dopandsAndAdditives(userData['Perovskite. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ] from: {fileName}')
        data['Perovskite_additives_compounds'] = ''

    #%% Perovskite. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]
    try:
        data['Perovskite_additives_concentrations'] = cdf.concentrations(userData['Perovskite. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...] from: {fileName}')
        data['Perovskite_additives_concentrations'] = ''

    #%% Perovskite. Thickness [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['Perovskite_thickness'] = cdf.thickness(userData['Perovskite. Thickness [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: Perovskite. Thickness [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['Perovskite_thickness'] = ''

    #%% Perovskite. Band gap [Eg.1 | Eg.2 | ...] [eV]
    try:
        data['Perovskite_band_gap'] = cdf.numberListUnitless(userData['Perovskite. Band gap [Eg.1 | Eg.2 | ...] [eV]'])
    except: 
        print(f'Cound not read in: Perovskite. Band gap [Eg.1 | Eg.2 | ...] [eV] from: {fileName}')
        data['Perovskite_band_gap'] = ''

    #%% Perovskite. Band gap. Graded [TRUE/FALSE | TRUE/FALSE | ...]
    try:
        data['Perovskite_band_gap_graded'] = cdf.trueOrFalseList(userData['Perovskite. Band gap. Graded [TRUE/FALSE | TRUE/FALSE | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Band gap. Graded [TRUE/FALSE | TRUE/FALSE | ...] from: {fileName}')
        data['Perovskite_band_gap_graded'] = ''

    #%% Perovskite. Band gap. Estimation basis [Absorption/Composition/Literature/EQE/…]
    try:
        data['Perovskite_band_gap_estimation_basis'] = cdf.convertToString(userData['Perovskite. Band gap. Estimation basis [Absorption/Composition/Literature/EQE/…]'])
    except: 
        print(f'Cound not read in: PPerovskite. Band gap. Estimation basis [Absorption/Composition/Literature/EQE/…]: {fileName}')
        data['Perovskite_band_gap_estimation_basis'] = ''

    #%% Perovskite. Pl max [PL.1; PL.2; … | PL.3; … | ...] [nm]
    try:
        data['Perovskite_pl_max'] = cdf.numberListUnitless(userData['Perovskite. Pl max [PL.1; PL.2; … | PL.3; … | ...] [nm]'])
    except: 
        print(f'Cound not read in: Perovskite. Pl max [PL.1; PL.2; … | PL.3; … | ...] [nm] from: {fileName}')
        data['Perovskite_pl_max'] = ''

    #%% Perovskite. Deposition. Number of deposition steps
    try:
        data['Perovskite_deposition_number_of_deposition_steps'] = cdf.numericInteger(userData['Perovskite. Deposition. Number of deposition steps'], default = 0)
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Number of deposition steps from: {fileName}')
        data['Perovskite_deposition_number_of_deposition_steps'] = ''

    #%% Perovskite. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['Perovskite_deposition_procedure'] = cdf.depositionProcedure(userData['Perovskite. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['Perovskite_deposition_procedure'] = ''

    #%% Perovskite. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]
    try:
        data['Perovskite_deposition_aggregation_state_of_reactants'] = cdf.aggregationStates(userData['Perovskite. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ] from: {fileName}')
        data['Perovskite_deposition_aggregation_state_of_reactants'] = ''
        
    #%% Perovskite. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Perovskite_deposition_synthesis_atmosphere'] = cdf.atmosphere(userData['Perovskite. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Perovskite. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Perovskite_deposition_synthesis_atmosphere'] = ''

    #%% Perovskite. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Perovskite_deposition_synthesis_atmosphere_pressure_total'] = cdf.pressure(userData['Perovskite. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Perovskite_deposition_synthesis_atmosphere_pressure_total'] = ''

    #%% Perovskite. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Perovskite_deposition_synthesis_atmosphere_pressure_partial'] = cdf.pressure(userData['Perovskite. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Perovskite_deposition_synthesis_atmosphere_pressure_partial'] = ''

    #%% Perovskite. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]
    try:
        data['Perovskite_deposition_synthesis_atmosphere_relative_humidity'] = cdf.relativeHumidity(userData['Perovskite. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%] from: {fileName}')
        data['Perovskite_deposition_synthesis_atmosphere_relative_humidity'] = ''

    #%% Perovskite. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]
    try:
        data['Perovskite_deposition_solvents'] = cdf.solvents(userData['Perovskite. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ] from: {fileName}')
        data['Perovskite_deposition_solvents'] = ''

    #%% Perovskite. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]
    try:
        data['Perovskite_deposition_solvents_mixing_ratios'] = cdf.mixingRatios(userData['Perovskite. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ] from: {fileName}')
        data['Perovskite_deposition_solvents_mixing_ratios'] = ''

    #%% Perovskite. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Perovskite_deposition_solvents_supplier'] = cdf.supplier(userData['Perovskite. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Perovskite_deposition_solvents_supplier'] = ''

    #%% Perovskite. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Perovskite_deposition_solvents_purity'] = cdf.purity(userData['Perovskite. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Perovskite_deposition_solvents_purity'] = ''

    #%% Perovskite. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]
    try:
        data['Perovskite_deposition_reaction_solutions_compounds'] = cdf.compounds(userData['Perovskite. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...] from: {fileName}')
        data['Perovskite_deposition_reaction_solutions_compounds'] = ''

    #%% Perovskite. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Perovskite_deposition_reaction_solutions_compounds_supplier'] = cdf.supplier(userData['Perovskite. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Perovskite_deposition_reaction_solutions_compounds_supplier'] = ''

    #%% Perovskite. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Perovskite_deposition_reaction_solutions_compounds_purity'] = cdf.purity(userData['Perovskite. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Perovskite_deposition_reaction_solutions_compounds_purity'] = ''

    #%% Perovskite. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]
    try:
        data['Perovskite_deposition_reaction_solutions_concentrations'] = cdf.concentrations(userData['Perovskite. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...] from: {fileName}')
        data['Perovskite_deposition_reaction_solutions_concentrations'] = ''

    #%% Perovskite. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]
    try:
        data['Perovskite_deposition_reaction_solutions_volumes'] = cdf.volumes(userData['Perovskite. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]'], givenUnit = 'ml', desiredUnit = 'ml')
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml] from: {fileName}')
        data['Perovskite_deposition_reaction_solutions_volumes'] = ''

    #%% Perovskite. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]
    try:
        data['Perovskite_deposition_reaction_solutions_age'] = cdf.time(userData['Perovskite. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h] from: {fileName}')
        data['Perovskite_deposition_reaction_solutions_age'] = ''

    #%% Perovskite. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Perovskite_deposition_reaction_solutions_temperature'] = cdf.temperature(userData['Perovskite. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Perovskite_deposition_reaction_solutions_temperature'] = ''

    #%% Perovskite. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Perovskite_deposition_substrate_temperature'] = cdf.temperature(userData['Perovskite. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Perovskite_deposition_substrate_temperature'] = ''

    #%% Perovskite. Deposition. Quenching induced crystallisation [TRUE/FALSE]
    try:
        data['Perovskite_deposition_quenching_induced_crystallisation'] = cdf.trueOrFalse(userData['Perovskite. Deposition. Quenching induced crystallisation [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Quenching induced crystallisation [TRUE/FALSE] from: {fileName}')
        data['Perovskite_deposition_quenching_induced_crystallisation'] = ''

    #%% Perovskite. Deposition. Quenching media [Sol.1; Sol.2; …]
    try:
        data['Perovskite_deposition_quenching_media'] = cdf.solvents(userData['Perovskite. Deposition. Quenching media [Sol.1; Sol.2; …]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Quenching media [Sol.1; Sol.2; …] from: {fileName}')
        data['Perovskite_deposition_quenching_media'] = ''

    #%% Perovskite. Deposition. Quenching media. Mixing ratios [V1; V2: ...]
    try:
        data['Perovskite_deposition_quenching_media_mixing_ratios'] = cdf.mixingRatios(userData['Perovskite. Deposition. Quenching media. Mixing ratios [V1; V2: ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Quenching media. Mixing ratios [V1; V2: ...] from: {fileName}')
        data['Perovskite_deposition_quenching_media_mixing_ratios'] = ''

    #%% Perovskite. Deposition. Quenching media. Volume [µl]
    try:
        data['Perovskite_deposition_quenching_media_volume'] = cdf.volumes(userData['Perovskite. Deposition. Quenching media. Volume [µl]'], givenUnit = 'µl', desiredUnit = 'µl')
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Quenching media. Volume [µl] from: {fileName}')
        data['Perovskite_deposition_quenching_media_volume'] = ''

    #%% Perovskite. Deposition. Quenching media. Additives. Compounds [Addt.1; Addt.2; ... ]
    try:
        data['Perovskite_deposition_quenching_media_additives_compounds'] = cdf.dopandsAndAdditives(userData['Perovskite. Deposition. Quenching media. Additives. Compounds [Addt.1; Addt.2; ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Quenching media. Additives. Compounds [Addt.1; Addt.2; ... ] from: {fileName}')
        data['Perovskite_deposition_quenching_media_additives_compounds'] = ''

    #%% Perovskite. Deposition. Quenching media. Additives. Concentrations [c1 M; c2 wt%; c3 mg/ml; ...]
    try:
        data['Perovskite_deposition_quenching_media_additives_concentrations'] = cdf.concentrations(userData['Perovskite. Deposition. Quenching media. Additives. Concentrations [c1 M; c2 wt%; c3 mg/ml; ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Quenching media. Additives. Concentrations [c1 M; c2 wt%; c3 mg/ml; ...] from: {fileName}')
        data['Perovskite_deposition_quenching_media_additives_concentrations'] = ''

    #%% Perovskite. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Perovskite_deposition_thermal_annealing_temperature'] = cdf.temperature(userData['Perovskite. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Perovskite_deposition_thermal_annealing_temperature'] = ''

    #%% Perovskite. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]
    try:
        data['Perovskite_deposition_thermal_annealing_time'] = cdf.time(userData['Perovskite. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min] from: {fileName}')
        data['Perovskite_deposition_thermal_annealing_time'] = ''

    #%% Perovskite. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Perovskite_deposition_thermal_annealing_atmosphere'] = cdf.atmosphere(userData['Perovskite. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Perovskite_deposition_thermal_annealing_atmosphere'] = ''

    #%% Perovskite. Deposition. Thermal annealing. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]
    try:
        data['Perovskite_deposition_thermal_annealing_relative_humidity'] = cdf.relativeHumidity(userData['Perovskite. Deposition. Thermal annealing. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Perovskite. Deposition. Thermal annealing. [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%] from: {fileName}')
        data['Perovskite_deposition_thermal_annealing_relative_humidity'] = ''

    #%% Perovskite. Deposition. Thermal annealing. Pressure [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Perovskite_deposition_thermal_annealing_pressure'] = cdf.pressure(userData['Perovskite. Deposition. Thermal annealing. Pressure [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Thermal annealing. Pressure [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Perovskite_deposition_thermal_annealing_pressure'] = ''

    #%% Perovskite. Deposition. Solvent annealing [TRUE/FALSE]
    try:
        data['Perovskite_deposition_solvent_annealing'] = cdf.trueOrFalse(userData['Perovskite. Deposition. Solvent annealing [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvent annealing [TRUE/FALSE] from: {fileName}')
        data['Perovskite_deposition_solvent_annealing'] = ''

    #%% Perovskite. Deposition. Solvent annealing. Time vs thermal annealing [Before/Under/After/...]
    try:
        data['Perovskite_deposition_solvent_annealing_time_vs_thermal_annealing'] = cdf.convertToString(userData['Perovskite. Deposition. Solvent annealing. Time vs thermal annealing [Before/Under/After/...]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvent annealing. Time vs thermal annealing [Before/Under/After/...] from: {fileName}')
        data['Perovskite_deposition_solvent_annealing_time_vs_thermal_annealing'] = ''

    #%% Perovskite. Deposition. Solvent annealing. Solvent atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Perovskite_deposition_solvent_annealing_solvent_atmosphere'] = cdf.atmosphere(userData['Perovskite. Deposition. Solvent annealing. Solvent atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvent annealing. Solvent atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Perovskite_deposition_solvent_annealing_solvent_atmosphere'] = ''

    #%% Perovskite. Deposition. Solvent annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]
    try:
        data['Perovskite_deposition_solvent_annealing_time'] = cdf.time(userData['Perovskite. Deposition. Solvent annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvent annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min] from: {fileName}')
        data['Perovskite_deposition_solvent_annealing_time'] = ''

    #%% Perovskite. Deposition. Solvent annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Perovskite_deposition_solvent_annealing_temperature'] = cdf.temperature(userData['Perovskite. Deposition. Solvent annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. Solvent annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Perovskite_deposition_solvent_annealing_temperature'] = ''

    #%% Perovskite. Deposition. After treatment of formed perovskite
    try:
        data['Perovskite_deposition_after_treatment_of_formed_perovskite'] = cdf.convertToString(userData['Perovskite. Deposition. After treatment of formed perovskite'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. After treatment of formed perovskite from: {fileName}')
        data['Perovskite_deposition_after_treatment_of_formed_perovskite'] = ''

    #%% Perovskite. Deposition. After treatment of formed perovskite. Metrics
    try:
        data['Perovskite_deposition_after_treatment_of_formed_perovskite_metrics'] = cdf.convertToString(userData['Perovskite. Deposition. After treatment of formed perovskite. Metrics'])
    except: 
        print(f'Cound not read in: Perovskite. Deposition. After treatment of formed perovskite. Metrics from: {fileName}')
        data['Perovskite_deposition_after_treatment_of_formed_perovskite_metrics'] = ''

    #%% Perovskite. Storage. Time until next deposition step [h]
    try:
        data['Perovskite_storage_time_until_next_deposition_step'] = cdf.time(userData['Perovskite. Storage. Time until next deposition step [h]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: Perovskite. Storage. Time until next deposition step [h] from: {fileName}')
        data['Perovskite_storage_time_until_next_deposition_step'] = ''

    #%% Perovskite. Storage. Atmosphere [Gas1; Gas2; ...]
    try:
        data['Perovskite_storage_atmosphere'] = cdf.atmosphere(userData['Perovskite. Storage. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: Perovskite. Storage. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['Perovskite_storage_atmosphere'] = ''

    #%% Perovskite. Storage. Relative humidity [%] 
    try:
        data['Perovskite_storage_relative_humidity'] = cdf.relativeHumidity(userData['Perovskite. Storage. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: Perovskite. Storage. Relative humidity [%] from: {fileName}')
        data['Perovskite_storage_relative_humidity'] = ''

    #%% Perovskite. Surface treatment before next depositionstep 
    try:
        data['Perovskite_surface_treatment_before_next_deposition_step'] = cdf.convertToString(userData['Perovskite. Surface treatment before next deposition step'])
    except: 
        print(f'Cound not read in: Perovskite. Surface treatment before next deposition step from: {fileName}')
        data['Perovskite_surface_treatment_before_next_deposition_step'] = ''

    #%% HTL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['HTL_stack_sequence'] = cdf.stackSequence(userData['HTL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: HTL. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['HTL_stack_sequence'] = ''

    #%% HTL. Thickness [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['HTL_thickness_list'] = cdf.thickness(userData['HTL. Thickness [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: HTL. Thickness [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['HTL_thickness_list'] = ''

    #%% HTL. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]
    try:
        data['HTL_additives_compounds'] = cdf.dopandsAndAdditives(userData['HTL. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ] from: {fileName}')
        data['HTL_additives_compounds'] = ''

    #%% HTL. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]
    try:
        data['HTL_additives_concentrations'] = cdf.concentrations(userData['HTL. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]'])
    except: 
        print(f'Cound not read in: HTL. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...] from: {fileName}')
        data['HTL_additives_concentrations'] = ''

    #%% HTL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['HTL_deposition_procedure'] = cdf.depositionProcedure(userData['HTL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['HTL_deposition_procedure'] = ''

    #%% HTL. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]
    try:
        data['HTL_deposition_aggregation_state_of_reactants'] = cdf.aggregationStates(userData['HTL. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ] from: {fileName}')
        data['HTL_deposition_aggregation_state_of_reactants'] = ''

    #%% HTL. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['HTL_deposition_synthesis_atmosphere'] = cdf.atmosphere(userData['HTL. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['HTL_deposition_synthesis_atmosphere'] = ''

    #%% HTL. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['HTL_deposition_synthesis_atmosphere_pressure_total'] = cdf.pressure(userData['HTL. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['HTL_deposition_synthesis_atmosphere_pressure_total'] = ''

    #%% HTL. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['HTL_deposition_synthesis_atmosphere_pressure_partial'] = cdf.pressure(userData['HTL. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['HTL_deposition_synthesis_atmosphere_pressure_partial'] = ''

    #%% HTL. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]
    try:
        data['HTL_deposition_synthesis_atmosphere_relative_humidity'] = cdf.relativeHumidity(userData['HTL. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%] from: {fileName}')
        data['HTL_deposition_synthesis_atmosphere_relative_humidity'] = ''

    #%% HTL. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]
    try:
        data['HTL_deposition_solvents'] = cdf.solvents(userData['HTL. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ] from: {fileName}')
        data['HTL_deposition_solvents'] = ''

    #%% HTL. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]
    try:
        data['HTL_deposition_solvents_mixing_ratios'] = cdf.mixingRatios(userData['HTL. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ] from: {fileName}')
        data['HTL_deposition_solvents_mixing_ratios'] = ''

    #%% HTL. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['HTL_deposition_solvents_supplier'] = cdf.supplier(userData['HTL. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['HTL_deposition_solvents_supplier'] = ''

    #%% HTL. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['HTL_deposition_solvents_purity'] = cdf.purity(userData['HTL. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['HTL_deposition_solvents_purity'] = ''

    #%% HTL. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]
    try:
        data['HTL_deposition_reaction_solutions_compounds'] = cdf.compounds(userData['HTL. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...] from: {fileName}')
        data['HTL_deposition_reaction_solutions_compounds'] = ''

    #%% HTL. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['HTL_deposition_reaction_solutions_compounds_supplier'] = cdf.supplier(userData['HTL. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['HTL_deposition_reaction_solutions_compounds_supplier'] = ''

    #%% HTL. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['HTL_deposition_reaction_solutions_compounds_purity'] = cdf.purity(userData['HTL. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['HTL_deposition_reaction_solutions_compounds_purity'] = ''

    #%% HTL. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]
    try:
        data['HTL_deposition_reaction_solutions_concentrations'] = cdf.concentrations(userData['HTL. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...] from: {fileName}')
        data['HTL_deposition_reaction_solutions_concentrations'] = ''

    #%% HTL. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]
    try:
        data['HTL_deposition_reaction_solutions_volumes'] = cdf.volumes(userData['HTL. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]'], givenUnit = 'ml', desiredUnit = 'ml')
    except: 
        print(f'Cound not read in: HTL. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml] from: {fileName}')
        data['HTL_deposition_reaction_solutions_volumes'] = ''

    #%% HTL. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]
    try:
        data['HTL_deposition_reaction_solutions_age'] = cdf.time(userData['HTL. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: HTL. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h] from: {fileName}')
        data['HTL_deposition_reaction_solutions_age'] = ''

    #%% HTL. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['HTL_deposition_reaction_solutions_temperature'] = cdf.temperature(userData['HTL. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['HTL_deposition_reaction_solutions_temperature'] = ''

    #%% HTL. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['HTL_deposition_substrate_temperature'] = cdf.temperature(userData['HTL. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['HTL_deposition_substrate_temperature'] = ''

    #%% HTL. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['HTL_deposition_thermal_annealing_temperature'] = cdf.temperature(userData['HTL. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['HTL_deposition_thermal_annealing_temperature'] = ''

    #%% HTL. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]
    try:
        data['HTL_deposition_thermal_annealing_time'] = cdf.time(userData['HTL. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: HTL. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min] from: {fileName}')
        data['HTL_deposition_thermal_annealing_time'] = ''

    #%% HTL. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['HTL_deposition_thermal_annealing_atmosphere'] = cdf.atmosphere(userData['HTL. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: HTL. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['HTL_deposition_thermal_annealing_atmosphere'] = ''

    #%% HTL. Storage. Time until next deposition step [h]
    try:
        data['HTL_storage_time_until_next_deposition_step'] = cdf.time(userData['HTL. Storage. Time until next deposition step [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: HTL. Storage. Time until next deposition step [h] from: {fileName}')
        data['HTL_storage_time_until_next_deposition_step'] = ''

    #%% HTL. Storage. Atmosphere [Gas1; Gas2; ...]
    try:
        data['HTL_storage_atmosphere'] = cdf.atmosphere(userData['HTL. Storage. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: HTL. Storage. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['HTL_storage_atmosphere'] = ''

    #%% HTL. Storage. Relative humidity [%] 
    try:
        data['HTL_storage_relative_humidity'] = cdf.relativeHumidity(userData['HTL. Storage. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: HTL. Storage. Relative humidity [%] from: {fileName}')
        data['HTL_storage_relative_humidity'] = ''

    #%% HTL. Surface treatment before next depositionstep 
    try:
        data['HTL_surface_treatment_before_next_deposition_step'] = cdf.convertToString(userData['HTL. Surface treatment before next deposition step'])
    except: 
        print(f'Cound not read in: HTL. Surface treatment before next deposition step from: {fileName}')
        data['HTL_surface_treatment_before_next_deposition_step'] = ''

    #%% Backcontact. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Backcontact_stack_sequence'] = cdf.stackSequence(userData['Backcontact. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Backcontact. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Backcontact_stack_sequence'] = ''

    #%% Backcontact. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['Backcontact_thickness_list'] = cdf.thickness(userData['Backcontact. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: Backcontact. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['Backcontact_thickness_list'] = ''

    #%% Backcontact. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]
    try:
        data['Backcontact_additives_compounds'] = cdf.dopandsAndAdditives(userData['Backcontact. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ] from: {fileName}')
        data['Backcontact_additives_compounds'] = ''

    #%% Backcontact. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]
    try:
        data['Backcontact_additives_concentrations'] = cdf.concentrations(userData['Backcontact. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]'])
    except: 
        print(f'Cound not read in: Backcontact. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...] from: {fileName}')
        data['Backcontact_additives_concentrations'] = ''

    #%% Backcontact. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['Backcontact_deposition_procedure'] = cdf.depositionProcedure(userData['Backcontact. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['Backcontact_deposition_procedure'] = ''

    #%% Backcontact. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]
    try:
        data['Backcontact_deposition_aggregation_state_of_reactants'] = cdf.aggregationStates(userData['Backcontact. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ] from: {fileName}')
        data['Backcontact_deposition_aggregation_state_of_reactants'] = ''

    #%% Backcontact. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Backcontact_deposition_synthesis_atmosphere'] = cdf.atmosphere(userData['Backcontact. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Backcontact_deposition_synthesis_atmosphere'] = ''

    #%% Backcontact. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Backcontact_deposition_synthesis_atmosphere_pressure_total'] = cdf.pressure(userData['Backcontact. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Backcontact_deposition_synthesis_atmosphere_pressure_total'] = ''

    #%% Backcontact. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Backcontact_deposition_synthesis_atmosphere_pressure_partial'] = cdf.pressure(userData['Backcontact. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Backcontact_deposition_synthesis_atmosphere_pressure_partial'] = ''

    #%% Backcontact. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]
    try:
        data['Backcontact_deposition_synthesis_atmosphere_relative_humidity'] = cdf.relativeHumidity(userData['Backcontact. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%] from: {fileName}')
        data['Backcontact_deposition_synthesis_atmosphere_relative_humidity'] = ''

    #%% Backcontact. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]
    try:
        data['Backcontact_deposition_solvents'] = cdf.solvents(userData['Backcontact. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ] from: {fileName}')
        data['Backcontact_deposition_solvents'] = ''

    #%% Backcontact. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]
    try:
        data['Backcontact_deposition_solvents_mixing_ratios'] = cdf.mixingRatios(userData['Backcontact. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ] from: {fileName}')
        data['Backcontact_deposition_solvents_mixing_ratios'] = ''

    #%% Backcontact. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Backcontact_deposition_solvents_supplier'] = cdf.supplier(userData['Backcontact. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Backcontact_deposition_solvents_supplier'] = ''

    #%% Backcontact. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Backcontact_deposition_solvents_purity'] = cdf.purity(userData['Backcontact. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Backcontact_deposition_solvents_purity'] = ''

    #%% Backcontact. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]
    try:
        data['Backcontact_deposition_reaction_solutions_compounds'] = cdf.compounds(userData['Backcontact. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...] from: {fileName}')
        data['Backcontact_deposition_reaction_solutions_compounds'] = ''

    #%% Backcontact. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Backcontact_deposition_reaction_solutions_compounds_supplier'] = cdf.supplier(userData['Backcontact. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Backcontact_deposition_reaction_solutions_compounds_supplier'] = ''

    #%% Backcontact. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Backcontact_deposition_reaction_solutions_compounds_purity'] = cdf.purity(userData['Backcontact. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Backcontact_deposition_reaction_solutions_compounds_purity'] = ''

    #%% Backcontact. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]
    try:
        data['Backcontact_deposition_reaction_solutions_concentrations'] = cdf.concentrations(userData['Backcontact. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...] from: {fileName}')
        data['Backcontact_deposition_reaction_solutions_concentrations'] = ''

    #%% Backcontact. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]
    try:
        data['Backcontact_deposition_reaction_solutions_volumes'] = cdf.volumes(userData['Backcontact. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]'], givenUnit = 'ml', desiredUnit = 'ml')
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml] from: {fileName}')
        data['Backcontact_deposition_reaction_solutions_volumes'] = ''

    #%% Backcontact. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]
    try:
        data['Backcontact_deposition_reaction_solutions_age'] = cdf.time(userData['Backcontact. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h] from: {fileName}')
        data['Backcontact_deposition_reaction_solutions_age'] = ''

    #%% Backcontact. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Backcontact_deposition_reaction_solutions_temperature'] = cdf.temperature(userData['Backcontact. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Backcontact_deposition_reaction_solutions_temperature'] = ''

    #%% Backcontact. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Backcontact_deposition_substrate_temperature'] = cdf.temperature(userData['Backcontact. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Backcontact_deposition_substrate_temperature'] = ''

    #%% Backcontact. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Backcontact_deposition_thermal_annealing_temperature'] = cdf.temperature(userData['Backcontact. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Backcontact_deposition_thermal_annealing_temperature'] = ''

    #%% Backcontact. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]
    try:
        data['Backcontact_deposition_thermal_annealing_time'] = cdf.time(userData['Backcontact. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min] from: {fileName}')
        data['Backcontact_deposition_thermal_annealing_time'] = ''

    #%% Backcontact. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Backcontact_deposition_thermal_annealing_atmosphere'] = cdf.atmosphere(userData['Backcontact. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Backcontact. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Backcontact_deposition_thermal_annealing_atmosphere'] = ''

    #%% Backcontact. Storage. Time until next deposition step [h]
    try:
        data['Backcontact_storage_time_until_next_deposition_step'] = cdf.time(userData['Backcontact. Storage. Time until next deposition step [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Backcontact. Storage. Time until next deposition step [h] from: {fileName}')
        data['Backcontact_storage_time_until_next_deposition_step'] = ''

    #%% Backcontact. Storage. Atmosphere [Gas1; Gas2; ...]
    try:
        data['Backcontact_storage_atmosphere'] = cdf.atmosphere(userData['Backcontact. Storage. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: Backcontact. Storage. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['Backcontact_storage_atmosphere'] = ''

    #%% Backcontact. Storage. Relative humidity [%] 
    try:
        data['Backcontact_storage_relative_humidity'] = cdf.relativeHumidity(userData['Backcontact. Storage. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: Backcontact. Storage. Relative humidity [%] from: {fileName}')
        data['Backcontact_storage_relative_humidity'] = ''

    #%% Backcontact. Surface treatment before next depositionstep 
    try:
        data['Backcontact_surface_treatment_before_next_deposition_step'] = cdf.convertToString(userData['Backcontact. Surface treatment before next deposition step'])
    except: 
        print(f'Cound not read in: Backcontact. Surface treatment before next deposition step from: {fileName}')
        data['Backcontact_surface_treatment_before_next_deposition_step'] = ''

    #%% Add. Lay. Front [TRUE/FALSE]
    try:
        data['Add_lay_front'] = cdf.trueOrFalse(userData['Add. Lay. Front [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front [TRUE/FALSE] from: {fileName}')
        data['Add_lay_front'] = ''

    #%% Add. Lay. Front. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]
    try:
        data['Add_lay_front_function'] = cdf.convertToString(userData['Add. Lay. Front. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...] from: {fileName}')
        data['Add_lay_front_function'] = ''

    #%% Add. Lay. Front. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Add_lay_front_stack_sequence'] = cdf.stackSequence(userData['Add. Lay. Front. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Add_lay_front_stack_sequence'] = ''

    #%% Add. Lay. Front. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['Add_lay_front_thickness_list'] = cdf.thickness(userData['Add. Lay. Front. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: Add. Lay. Front. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['Add_lay_front_thickness_list'] = ''

    #%% Add. Lay. Front. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]
    try:
        data['Add_lay_front_additives_compounds'] = cdf.dopandsAndAdditives(userData['Add. Lay. Front. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ] from: {fileName}')
        data['Add_lay_front_additives_compounds'] = ''

    #%% Add. Lay. Front. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]
    try:
        data['Add_lay_front_additives_concentrations'] = cdf.concentrations(userData['Add. Lay. Front. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...] from: {fileName}')
        data['Add_lay_front_additives_concentrations'] = ''

    #%% Add. Lay. Front. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['Add_lay_front_deposition_procedure'] = cdf.depositionProcedure(userData['Add. Lay. Front. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_procedure'] = ''

    #%% Add. Lay. Front. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]
    try:
        data['Add_lay_front_deposition_aggregation_state_of_reactants'] = cdf.aggregationStates(userData['Add. Lay. Front. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_aggregation_state_of_reactants'] = ''

    #%% Add. Lay. Front. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Add_lay_front_deposition_synthesis_atmosphere'] = cdf.atmosphere(userData['Add. Lay. Front. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_synthesis_atmosphere'] = ''

    #%% Add. Lay. Front. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Add_lay_front_deposition_synthesis_atmosphere_pressure_total'] = cdf.pressure(userData['Add. Lay. Front. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Add_lay_front_deposition_synthesis_atmosphere_pressure_total'] = ''

    #%% Add. Lay. Front. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Add_lay_front_deposition_synthesis_atmosphere_pressure_partial'] = cdf.pressure(userData['Add. Lay. Front. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Add_lay_front_deposition_synthesis_atmosphere_pressure_partial'] = ''

    #%% Add. Lay. Front. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]
    try:
        data['Add_lay_front_deposition_synthesis_atmosphere_relative_humidity'] = cdf.relativeHumidity(userData['Add. Lay. Front. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%] from: {fileName}')
        data['Add_lay_front_deposition_synthesis_atmosphere_relative_humidity'] = ''

    #%% Add. Lay. Front. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]
    try:
        data['Add_lay_front_deposition_solvents'] = cdf.solvents(userData['Add. Lay. Front. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_solvents'] = ''

    #%% Add. Lay. Front. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]
    try:
        data['Add_lay_front_deposition_solvents_mixing_ratios'] = cdf.mixingRatios(userData['Add. Lay. Front. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_solvents_mixing_ratios'] = ''

    #%% Add. Lay. Front. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Add_lay_front_deposition_solvents_supplier'] = cdf.supplier(userData['Add. Lay. Front. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_solvents_supplier'] = ''

    #%% Add. Lay. Front. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Add_lay_front_deposition_solvents_purity'] = cdf.purity(userData['Add. Lay. Front. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_solvents_purity'] = ''

    #%% Add. Lay. Front. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]
    try:
        data['Add_lay_front_deposition_reaction_solutions_compounds'] = cdf.compounds(userData['Add. Lay. Front. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...] from: {fileName}')
        data['Add_lay_front_deposition_reaction_solutions_compounds'] = ''

    #%% Add. Lay. Front. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Add_lay_front_deposition_reaction_solutions_compounds_supplier'] = cdf.supplier(userData['Add. Lay. Front. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_reaction_solutions_compounds_supplier'] = ''

    #%% Add. Lay. Front. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Add_lay_front_deposition_reaction_solutions_compounds_purity'] = cdf.purity(userData['Add. Lay. Front. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_reaction_solutions_compounds_purity'] = ''

    #%% Add. Lay. Front. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]
    try:
        data['Add_lay_front_deposition_reaction_solutions_concentrations'] = cdf.concentrations(userData['Add. Lay. Front. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...] from: {fileName}')
        data['Add_lay_front_deposition_reaction_solutions_concentrations'] = ''

    #%% Add. Lay. Front. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]
    try:
        data['Add_lay_front_deposition_reaction_solutions_volumes'] = cdf.volumes(userData['Add. Lay. Front. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]'], givenUnit = 'ml', desiredUnit = 'ml')
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml] from: {fileName}')
        data['Add_lay_front_deposition_reaction_solutions_volumes'] = ''

    #%% Add. Lay. Front. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]
    try:
        data['Add_lay_front_deposition_reaction_solutions_age'] = cdf.time(userData['Add. Lay. Front. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h] from: {fileName}')
        data['Add_lay_front_deposition_reaction_solutions_age'] = ''

    #%% Add. Lay. Front. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Add_lay_front_deposition_reaction_solutions_temperature'] = cdf.temperature(userData['Add. Lay. Front. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Add_lay_front_deposition_reaction_solutions_temperature'] = ''

    #%% Add. Lay. Front. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Add_lay_front_deposition_substrate_temperature'] = cdf.temperature(userData['Add. Lay. Front. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Add_lay_front_deposition_substrate_temperature'] = ''

    #%% Add. Lay. Front. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Add_lay_front_deposition_thermal_annealing_temperature'] = cdf.temperature(userData['Add. Lay. Front. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Add_lay_front_deposition_thermal_annealing_temperature'] = ''

    #%% Add. Lay. Front. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]
    try:
        data['Add_lay_front_deposition_thermal_annealing_time'] = cdf.time(userData['Add. Lay. Front. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min] from: {fileName}')
        data['Add_lay_front_deposition_thermal_annealing_time'] = ''

    #%% Add. Lay. Front. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Add_lay_front_deposition_thermal_annealing_atmosphere'] = cdf.atmosphere(userData['Add. Lay. Front. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Add_lay_front_deposition_thermal_annealing_atmosphere'] = ''

    #%% Add. Lay. Front. Storage. Time until next deposition step [h]
    try:
        data['Add_lay_front_storage_time_until_next_deposition_step'] = cdf.time(userData['Add. Lay. Front. Storage. Time until next deposition step [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Add. Lay. Front. Storage. Time until next deposition step [h] from: {fileName}')
        data['Add_lay_front_storage_time_until_next_deposition_step'] = ''

    #%% Add. Lay. Front. Storage. Atmosphere [Gas1; Gas2; ...]
    try:
        data['Add_lay_front_storage_atmosphere'] = cdf.atmosphere(userData['Add. Lay. Front. Storage. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Storage. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['Add_lay_front_storage_atmosphere'] = ''

    #%% Add. Lay. Front. Storage. Relative humidity [%] 
    try:
        data['Add_lay_front_storage_relative_humidity'] = cdf.relativeHumidity(userData['Add. Lay. Front. Storage. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Storage. Relative humidity [%] from: {fileName}')
        data['Add_lay_front_storage_relative_humidity'] = ''

    #%% Add. Lay. Front. Surface treatment before next depositionstep 
    try:
        data['Add_lay_front_surface_treatment_before_next_deposition_step'] = cdf.convertToString(userData['Add. Lay. Front. Surface treatment before next deposition step'])
    except: 
        print(f'Cound not read in: Add. Lay. Front. Surface treatment before next deposition step from: {fileName}')
        data['Add_lay_front_surface_treatment_before_next_deposition_step'] = ''

    #%% Add. Lay. Back [TRUE/FALSE]
    try:
        data['Add_lay_back'] = cdf.trueOrFalse(userData['Add. Lay. Back [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back [TRUE/FALSE] from: {fileName}')
        data['Add_lay_back'] = ''

    #%% Add. Lay. Back. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]
    try:
        data['Add_lay_back_function'] = cdf.convertToString(userData['Add. Lay. Back. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...] from: {fileName}')
        data['Add_lay_back_function'] = ''

    #%% Add. Lay. Back. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Add_lay_back_stack_sequence'] = cdf.stackSequence(userData['Add. Lay. Back. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Add_lay_back_stack_sequence'] = ''

    #%% Add. Lay. Back. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['Add_lay_back_thickness_list'] = cdf.thickness(userData['Add. Lay. Back. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: Add. Lay. Back. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['Add_lay_back_thickness_list'] = ''

    #%% Add. Lay. Back. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]
    try:
        data['Add_lay_back_additives_compounds'] = cdf.dopandsAndAdditives(userData['Add. Lay. Back. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Additives. Compounds [Addt.1; Addt.2; ... | Addt.3; … | Addt.4 | ... ] from: {fileName}')
        data['Add_lay_back_additives_compounds'] = ''

    #%% Add. Lay. Back. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]
    try:
        data['Add_lay_back_additives_concentrations'] = cdf.concentrations(userData['Add. Lay. Back. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Additives. Concentrations [c1 M; c2 wt%; … | c3 vol%; ... | c4 mg/ml | ...] from: {fileName}')
        data['Add_lay_back_additives_concentrations'] = ''

    #%% Add. Lay. Back. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['Add_lay_back_deposition_procedure'] = cdf.depositionProcedure(userData['Add. Lay. Back. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_procedure'] = ''

    #%% Add. Lay. Back. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]
    try:
        data['Add_lay_back_deposition_aggregation_state_of_reactants'] = cdf.aggregationStates(userData['Add. Lay. Back. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Aggregation state of reactants (Liquid/Gas/Solid) [Agr. 1 >> Agr. 2 >> ... | Agr. 3 >> … | Agr. 4 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_aggregation_state_of_reactants'] = ''

    #%% Add. Lay. Back. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Add_lay_back_deposition_synthesis_atmosphere'] = cdf.atmosphere(userData['Add. Lay. Back. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Synthesis atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_synthesis_atmosphere'] = ''

    #%% Add. Lay. Back. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Add_lay_back_deposition_synthesis_atmosphere_pressure_total'] = cdf.pressure(userData['Add. Lay. Back. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Synthesis atmosphere. Pressure. Total [P.1 >> P.2 >> ... | P.3 >> … | P.4 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Add_lay_back_deposition_synthesis_atmosphere_pressure_total'] = ''

    #%% Add. Lay. Back. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]
    try:
        data['Add_lay_back_deposition_synthesis_atmosphere_pressure_partial'] = cdf.pressure(userData['Add. Lay. Back. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Synthesis atmosphere. Pressure. Partial [P.1; P.2 >> P.3 >> ... | P.4 >> … | P.5 | ... ] [atm/Torr/Pa/bar/mmHg] from: {fileName}')
        data['Add_lay_back_deposition_synthesis_atmosphere_pressure_partial'] = ''

    #%% Add. Lay. Back. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]
    try:
        data['Add_lay_back_deposition_synthesis_atmosphere_relative_humidity'] = cdf.relativeHumidity(userData['Add. Lay. Back. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Synthesis atmosphere. Relative humidity [RH1 >> RH2 >> ... | RH3 >> … | RH4 | ... ] [%] from: {fileName}')
        data['Add_lay_back_deposition_synthesis_atmosphere_relative_humidity'] = ''

    #%% Add. Lay. Back. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]
    try:
        data['Add_lay_back_deposition_solvents'] = cdf.solvents(userData['Add. Lay. Back. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Solvents [Sol.1; Sol.2 >> Sol.3; ... >> ... | Sol.4 >> … | Sol.5 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_solvents'] = ''

    #%% Add. Lay. Back. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]
    try:
        data['Add_lay_back_deposition_solvents_mixing_ratios'] = cdf.mixingRatios(userData['Add. Lay. Back. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Solvents. Mixing ratios [V1; V2 >> V3; V4 >> ... | V5; V6 >> … | 1 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_solvents_mixing_ratios'] = ''

    #%% Add. Lay. Back. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Add_lay_back_deposition_solvents_supplier'] = cdf.supplier(userData['Add. Lay. Back. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Solvents. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_solvents_supplier'] = ''

    #%% Add. Lay. Back. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Add_lay_back_deposition_solvents_purity'] = cdf.purity(userData['Add. Lay. Back. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Solvents. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_solvents_purity'] = ''

    #%% Add. Lay. Back. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]
    try:
        data['Add_lay_back_deposition_reaction_solutions_compounds'] = cdf.compounds(userData['Add. Lay. Back. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Reaction solutions. Compounds [C1; C2 >> C3; … >> … | C4; C5 | C6 | ...] from: {fileName}')
        data['Add_lay_back_deposition_reaction_solutions_compounds'] = ''

    #%% Add. Lay. Back. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]
    try:
        data['Add_lay_back_deposition_reaction_solutions_compounds_supplier'] = cdf.supplier(userData['Add. Lay. Back. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Reaction solutions. Compounds. Supplier [Sup.1; Sup.2 >> Sup.3; ... >> ... | Sup.4 >> … | Sup.5 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_reaction_solutions_compounds_supplier'] = ''

    #%% Add. Lay. Back. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]
    try:
        data['Add_lay_back_deposition_reaction_solutions_compounds_purity'] = cdf.purity(userData['Add. Lay. Back. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Reaction solutions. Compounds. Purity [Pur.1; Pur.2 >> Pur.3; ... >> ... | Pur.4 >> … | Pur.5 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_reaction_solutions_compounds_purity'] = ''

    #%% Add. Lay. Back. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]
    try:
        data['Add_lay_back_deposition_reaction_solutions_concentrations'] = cdf.concentrations(userData['Add. Lay. Back. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Reaction solutions. Concentrations [c1 M; c2 mol/dm3 >> c3 mg/ml; … >> ... | c4 wt%; c5 vol% | c6 ppm |...] from: {fileName}')
        data['Add_lay_back_deposition_reaction_solutions_concentrations'] = ''

    #%% Add. Lay. Back. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]
    try:
        data['Add_lay_back_deposition_reaction_solutions_volumes'] = cdf.volumes(userData['Add. Lay. Back. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml]'], givenUnit = 'ml', desiredUnit = 'ml')
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Reaction solutions. Volumes [V1 >> V2 >> ... | V3 >> … | V4 | ... ] [ml] from: {fileName}')
        data['Add_lay_back_deposition_reaction_solutions_volumes'] = ''

    #%% Add. Lay. Back. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]
    try:
        data['Add_lay_back_deposition_reaction_solutions_age'] = cdf.time(userData['Add. Lay. Back. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Reaction solutions. Age [A1 >> A2 >> ... | A3 >> … | A4 | ... ] [h] from: {fileName}')
        data['Add_lay_back_deposition_reaction_solutions_age'] = ''

    #%% Add. Lay. Back. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Add_lay_back_deposition_reaction_solutions_temperature'] = cdf.temperature(userData['Add. Lay. Back. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Reaction solutions. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Add_lay_back_deposition_reaction_solutions_temperature'] = ''

    #%% Add. Lay. Back. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Add_lay_back_deposition_substrate_temperature'] = cdf.temperature(userData['Add. Lay. Back. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Substrate. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Add_lay_back_deposition_substrate_temperature'] = ''

    #%% Add. Lay. Back. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]
    try:
        data['Add_lay_back_deposition_thermal_annealing_temperature'] = cdf.temperature(userData['Add. Lay. Back. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Thermal annealing. Temperature [T1; T2 >> T3; ... >> ... | T4 >> … | T5 | ... ] [deg. C] from: {fileName}')
        data['Add_lay_back_deposition_thermal_annealing_temperature'] = ''

    #%% Add. Lay. Back. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]
    try:
        data['Add_lay_back_deposition_thermal_annealing_time'] = cdf.time(userData['Add. Lay. Back. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min]'], givenUnit = 'min', desiredUnit = 'min')
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Thermal annealing. Time [t1; t2 >> t3; ... >> ... | t4 >> … | t5 | ... ] [min] from: {fileName}')
        data['Add_lay_back_deposition_thermal_annealing_time'] = ''

    #%% Add. Lay. Back. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]
    try:
        data['Add_lay_back_deposition_thermal_annealing_atmosphere'] = cdf.atmosphere(userData['Add. Lay. Back. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Deposition. Thermal annealing. Atmosphere [Gas1; Gas2 >> Gas3; ... >> ... | Gas4 >> … | Gas5 | ... ] from: {fileName}')
        data['Add_lay_back_deposition_thermal_annealing_atmosphere'] = ''

    #%% Add. Lay. Back. Storage. Time until next deposition step [h]
    try:
        data['Add_lay_back_storage_time_until_next_deposition_step'] = cdf.time(userData['Add. Lay. Back. Storage. Time until next deposition step [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Add. Lay. Back. Storage. Time until next deposition step [h] from: {fileName}')
        data['Add_lay_back_storage_time_until_next_deposition_step'] = ''

    #%% Add. Lay. Back. Storage. Atmosphere [Gas1; Gas2; ...]
    try:
        data['Add_lay_back_storage_atmosphere'] = cdf.atmosphere(userData['Add. Lay. Back. Storage. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Storage. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['Add_lay_back_storage_atmosphere'] = ''

    #%% Add. Lay. Back. Storage. Relative humidity [%] 
    try:
        data['Add_lay_back_storage_relative_humidity'] = cdf.relativeHumidity(userData['Add. Lay. Back. Storage. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Storage. Relative humidity [%] from: {fileName}')
        data['Add_lay_back_storage_relative_humidity'] = ''

    #%% Add. Lay. Back. Surface treatment before next depositionstep 
    try:
        data['Add_lay_back_surface_treatment_before_next_deposition_step'] = cdf.convertToString(userData['Add. Lay. Back. Surface treatment before next deposition step'])
    except: 
        print(f'Cound not read in: Add. Lay. Back. Surface treatment before next deposition step from: {fileName}')
        data['Add_lay_back_surface_treatment_before_next_deposition_step'] = ''

    #%% Encapsulation [TRUE/FALSE]
    try:
        data['Encapsulation'] = cdf.trueOrFalse(userData['Encapsulation [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Encapsulation [TRUE/FALSE] from: {fileName}')
        data['Encapsulation'] = ''

    #%% Encapsulation. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Encapsulation_stack_sequence'] = cdf.stackSequence(userData['Encapsulation. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Encapsulation. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Encapsulation_stack_sequence'] = ''

    #%% Encapsulation. Edge sealing materials [Mat.1; Mat.2; ... ]
    try:
        data['Encapsulation_edge_sealing_materials'] = cdf.stackSequence(userData['Encapsulation. Edge sealing materials [Mat.1; Mat.2; ... ]'])
    except: 
        print(f'Cound not read in: Encapsulation. Edge sealing materials [Mat.1; Mat.2; ... ] from: {fileName}')
        data['Encapsulation_edge_sealing_materials'] = ''

    #%% Encapsulation. Atmosphere for encapsulation [Gas1; Gas2; ...]
    try:
        data['Encapsulation_atmosphere_for_encapsulation'] = cdf.atmosphere(userData['Encapsulation. Atmosphere for encapsulation [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: Encapsulation. Atmosphere for encapsulation [Gas1; Gas2; ...] from: {fileName}')
        data['Encapsulation_atmosphere_for_encapsulation'] = ''

    #%% Encapsulation. Water vapour transmission rate [g/m^2/d]
    try:
        data['Encapsulation_water_vapour_transmission_rate'] = cdf.numericValues(userData['Encapsulation. Water vapour transmission rate [g/m^2/d]'])
    except: 
        print(f'Cound not read in: Encapsulation. Water vapour transmission rate [g/m^2/d] from: {fileName}')
        data['Encapsulation_water_vapour_transmission_rate'] = ''

    #%% Encapsulation. Oxygen transmission rate [cm^3/m^2/d]
    try:
        data['Encapsulation_oxygen_transmission_rate'] = cdf.numericValues(userData['Encapsulation. Oxygen transmission rate [cm^3/m^2/d]'])
    except: 
        print(f'Cound not read in: Encapsulation. Oxygen transmission rate [cm^3/m^2/d] from: {fileName}')
        data['Encapsulation_oxygen_transmission_rate'] = ''

    #%% JV. Measured [TRUE/FALSE]
    try:
        data['JV_measured'] = cdf.trueOrFalse(userData['JV. Measured [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: JV. Measured [TRUE/FALSE] from: {fileName}')
        data['JV_measured'] = ''

    #%% JV. Average over N number of cells
    try:
        data['JV_average_over_n_number_of_cells'] = cdf.numericInteger(userData['JV. Average over N number of cells'], default = 1)
    except: 
        print(f'Cound not read in: JV. Average over N number of cells from: {fileName}')
        data['JV_average_over_n_number_of_cells'] = ''

    #%% JV. Certified values [TRUE/FALSE]
    try:
        data['JV_certified_values'] = cdf.trueOrFalse(userData['JV. Certified values [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: JV. Certified values [TRUE/FALSE] from: {fileName}')
        data['JV_certified_values'] = ''

    #%% JV. Certification Institute
    try:
        data['JV_certification_institute'] = cdf.convertToString(userData['JV. Certification Institute'])
    except: 
        print(f'Cound not read in: JV. Certification Institute from: {fileName}')
        data['JV_certification_institute'] = ''
   
    #%% JV. Storage. Age of cell [days]
    try:
        data['JV_storage_age_of_cell'] = cdf.time(userData['JV. Storage. Age of cell [days]'], givenUnit = 'days', desiredUnit = 'days')
    except: 
        print(f'Cound not read in: JV. Storage. Age of cell [days] from: {fileName}')
        data['JV_storage_age_of_cell'] = ''

    #%% JV. Storage. Atmosphere [Gas1; Gas2; ...]
    try:
        data['JV_storage_atmosphere'] = cdf.atmosphere(userData['JV. Storage. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: JV. Storage. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['JV_storage_atmosphere'] = ''

    #%% JV. Storage. Relative humidity [%] 
    try:
        data['JV_storage_relative_humidity'] = cdf.relativeHumidity(userData['JV. Storage. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: JV. Storage. Relative humidity [%] from: {fileName}')
        data['JV_storage_relative_humidity'] = ''
        
    #%% JV. Test. Atmosphere [Gas1; Gas2; ...]
    try:
        data['JV_test_atmosphere'] = cdf.atmosphere(userData['JV. Test. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: JV. Test. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['JV_test_atmosphere'] = ''

    #%% JV. Test. Relative humidity [%] 
    try:
        data['JV_test_relative_humidity'] = cdf.numericValues(userData['JV. Test. Relative humidity [%]'])
    except: 
        print(f'Cound not read in: JV. Test. Relative humidity [%] from: {fileName}')
        data['JV_test_relative_humidity'] = ''
 
    #%% JV. Test. Temperature [deg. C]
    try:
        data['JV_test_temperature'] = cdf.numericValues(userData['JV. Test. Temperature [deg. C]'])
    except: 
        print(f'Cound not read in: JV. Test. Temperature [deg. C] from: {fileName}')
        data['JV_test_temperature'] = ''      
        
    #%% JV. Light source. Type [Dark/White LED/Metal halide/ ...]
    try:
        data['JV_light_source_type'] = cdf.convertToString(userData['JV. Light source. Type [Dark/White LED/Metal halide/ ...]'])
    except: 
        print(f'Cound not read in: JV. Light source. Type [Dark/White LED/Metal halide/ ...] from: {fileName}')
        data['JV_light_source_type'] = ''       
        
    #%% JV. Light source. Brand name
    try:
        data['JV_light_source_brand_name'] = cdf.convertToString(userData['JV. Light source. Brand name'])
    except: 
        print(f'Cound not read in: JV. Light source. Brand name from: {fileName}')
        data['JV_light_source_brand_name'] = '' 
              
    #%% JV. Light source. Simulator class
    try:
        data['JV_light_source_simulator_class'] = cdf.convertToString(userData['JV. Light source. Simulator class'])
    except: 
        print(f'Cound not read in: JV. Light source. Simulator class from: {fileName}')
        data['JV_light_source_simulator_class'] = ''
        
    #%% JV. Light. Intensity [mW/cm^2]
    try:
        data['JV_light_intensity'] = cdf.numericValues(userData['JV. Light. Intensity [mW/cm^2]'])
    except: 
        print(f'Cound not read in: JV. Light. Intensity [mW/cm^2] from: {fileName}')
        data['JV_light_intensity'] = ''

    #%% JV. Light. Spectra [AM 1.5/UVA/UVB/Monochromatic/ …]
    try:
        data['JV_light_spectra'] = cdf.convertToString(userData['JV. Light. Spectra [AM 1.5/UVA/UVB/Monochromatic/ …]'])
    except: 
        print(f'Cound not read in: JV. Light. Spectra [AM 1.5/UVA/UVB/Monochromatic/ …] from: {fileName}')
        data['JV_light_spectra'] = ''
   
    #%% JV. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm]
    try:
        data['JV_light_wavelength_range'] = cdf.numberHighLowOrConstant(userData['JV. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm]'])
    except: 
        print(f'Cound not read in: JV. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm] from: {fileName}')
        data['JV_light_wavelength_range'] = ''
   
    #%% JV. Light. Illumination direction [Substrate/superstrate]
    try:
        data['JV_light_illumination_direction'] = cdf.convertToString(userData['JV. Light. Illumination direction [Substrate/superstrate]'])
    except: 
        print(f'Cound not read in: JV. Light. Illumination direction [Substrate/superstrate] {fileName}')
        data['JV_light_illumination_direction'] = '' 
   
    #%% JV. Light. Masked cell [TRUE/FALSE]
    try:
        data['JV_light_masked_cell'] = cdf.trueOrFalse(userData['JV. Light. Masked cell [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: JV. Light. Masked cell [TRUE/FALSE] from: {fileName}')
        data['JV_light_masked_cell'] = ''

    #%% JV. Light. Mask area [cm^2]
    try:
        data['JV_light_mask_area'] = cdf.numericValues(userData['JV. Light. Mask area [cm^2]'])
    except: 
        print(f'Cound not read in: JV. Light. Mask area [cm^2] from: {fileName}')
        data['JV_light_mask_area'] = ''

    #%% JV. Scan. Speed [mV/s]
    try:
        data['JV_scan_speed'] = cdf.numericValues(userData['JV. Scan. Speed [mV/s]'])
    except: 
        print(f'Cound not read in: JV. Scan. Speed [mV/s] from: {fileName}')
        data['JV_scan_speed'] = ''

    #%% JV. Scan. Delay time [ms]
    try:
        data['JV_scan_delay_time'] = cdf.numericValues(userData['JV. Scan. Delay time [ms]'])
    except: 
        print(f'Cound not read in: JV. Scan. Delay time [ms] from: {fileName}')
        data['JV_scan_delay_time'] = ''

    #%% JV. Scan. Integration time [ms]
    try:
        data['JV_scan_integration_time'] = cdf.numericValues(userData['JV. Scan. Integration time [ms]'])
    except: 
        print(f'Cound not read in: JV. Scan. Integration time [ms] from: {fileName}')
        data['JV_scan_integration_time'] = ''

    #%% JV. Scan. Voltage step [mV]
    try:
        data['JV._scan_voltage_step'] = cdf.numericValues(userData['JV. Scan. Voltage step [mV]'])
    except: 
        print(f'Cound not read in: JV. Scan. Voltage step [mV] from: {fileName}')
        data['_scan_voltage_step'] = ''

    #%% JV. Preconditioning. Protocol [none/Light soaking/Potential biasing/ …]
    try:
        data['JV_preconditioning_protocol'] = cdf.convertToString(userData['JV. Preconditioning. Protocol [none/Light soaking/Potential biasing/ …]'])
    except: 
        print(f'Cound not read in: JV. Preconditioning. Protocol [none/Light soaking/Potential biasing/ …] {fileName}')
        data['JV_preconditioning_protocol'] = ''   
  
    #%% JV. Preconditioning. Time [s]
    try:
        data['JV_preconditioning_time'] = cdf.numericValues(userData['JV. Preconditioning. Time [s]'])
    except: 
        print(f'Cound not read in: JV. Preconditioning. Time [s] from: {fileName}')
        data['JV_preconditioning_time'] = ''

    #%% JV. Preconditioning. Potential [V]
    try:
        data['JV_preconditioning_potential'] = cdf.numericValues(userData['JV. Preconditioning. Potential [V]'])
    except: 
        print(f'Cound not read in: JV. Preconditioning. Potential [V] from: {fileName}')
        data['JV_preconditioning_potential'] = ''

    #%% JV. Preconditioning. Light intensity [mW/cm^2]
    try:
        data['JV_preconditioning_light_intensity'] = cdf.numericValues(userData['JV. Preconditioning. Light intensity [mW/cm^2]'])
    except: 
        print(f'Cound not read in: JV. Preconditioning. Light intensity [mW/cm^2] from: {fileName}')
        data['JV_preconditioning_light_intensity'] = ''

    #%% JV. Reverse scan. Voc [V]
    try:
        data['JV_reverse_scan_Voc'] = cdf.VocData(userData['JV. Reverse scan. Voc [V]'], mV_to_V_cutoff = 10)
    except: 
        print(f'Cound not read in: JV. Reverse scan. Voc [V] from: {fileName}')
        data['JV_reverse_scan_Voc'] = ''

    #%% JV. Reverse scan. Jsc [mA/cm^2]
    try:
        data['JV_reverse_scan_Jsc'] = cdf.JscData(userData['JV. Reverse scan. Jsc [mA/cm^2]'])
    except: 
        print(f'Cound not read in: JV. Reverse scan. Jsc [mA/cm^2] from: {fileName}')
        data['JV_reverse_scan_Jsc'] = ''

    #%% JV. Reverse scan. FF [number between 0 and 1]
    try:
        data['JV_reverse_scan_FF'] = cdf.FFData(userData['JV. Reverse scan. FF [number between 0 and 1]'], FF_cutoff = 5)
    except: 
        print(f'Cound not read in: JV. Reverse scan. FF [number between 0 and 1] from: {fileName}')
        data['JV_reverse_scan_FF'] = ''

    #%% JV. Reverse scan. PCE [%]
    try:
        data['JV_reverse_scan_PCE'] = cdf.PCEData(userData['JV. Reverse scan. PCE [%]'])
    except: 
        print(f'Cound not read in: JV. Reverse scan. PCE [%] from: {fileName}')
        data['JV_reverse_scan_PCE'] = ''

    #%% JV. Reverse scan. Vmp [V]
    try:
        data['JV_reverse_scan_Vmp'] = cdf.VocData(userData['JV. Reverse scan. Vmp [V]'], mV_to_V_cutoff = 10)
    except: 
        print(f'Cound not read in: JV. Reverse scan. Vmp [V] from: {fileName}')
        data['JV_reverse_scan_Vmp'] = ''

    #%% JV. Reverse scan. Jmp [mA/cm^2]
    try:
        data['JV_reverse_scan_Jmp'] = cdf.JscData(userData['JV. Reverse scan. Jmp [mA/cm^2]'])
    except: 
        print(f'Cound not read in: JV. Reverse scan. Jmp [mA/cm^2] from: {fileName}')
        data['JV_reverse_scan_Jmp'] = ''

    #%% JV. Reverse scan. Series resistance [ohmcm^2]
    try:
        data['JV_reverse_scan_series_resistance'] = cdf.numericValues(userData['JV. Reverse scan. Series resistance [ohmcm^2]'])
    except: 
        print(f'Cound not read in: JV. Reverse scan. Series resistance [ohmcm^2] from: {fileName}')
        data['JV_reverse_scan_series_resistance'] = ''

    #%% JV. Reverse scan. Shunt resistance [ohmcm^2]
    try:
        data['JV_reverse_scan_shunt_resistance'] = cdf.numericValues(userData['JV. Reverse scan. Shunt resistance [ohmcm^2]'])
    except: 
        print(f'Cound not read in: JV. Reverse scan. Shunt resistance [ohmcm^2] from: {fileName}')
        data['JV_reverse_scan_shunt_resistance'] = ''

    #%% JV. Forward scan. Voc [V]
    try:
        data['JV_forward_scan_Voc'] = cdf.VocData(userData['JV. Forward scan. Voc [V]'], mV_to_V_cutoff = 10)
    except: 
        print(f'Cound not read in: JV. Forward scan. Voc [V] from: {fileName}')
        data['JV_forward_scan_Voc'] = ''

    #%% JV. Forward scan. Jsc [mA/cm^2]
    try:
        data['JV_forward_scan_Jsc'] = cdf.JscData(userData['JV. Forward scan. Jsc [mA/cm^2]'])
    except: 
        print(f'Cound not read in: JV. Forward scan. Jsc [mA/cm^2] from: {fileName}')
        data['JV_forward_scan_Jsc'] = ''

    #%% JV. Forward scan. FF [number between 0 and 1]
    try:
        data['JV_forward_scan_FF'] = cdf.FFData(userData['JV. Forward scan. FF [number between 0 and 1]'], FF_cutoff = 5)
    except: 
        print(f'Cound not read in: JV. Forward scan. FF [number between 0 and 1] from: {fileName}')
        data['JV_forward_scan_FF'] = ''

    #%% JV. Forward scan. PCE [%]
    try:
        data['JV_forward_scan_PCE'] = cdf.PCEData(userData['JV. Forward scan. PCE [%]'])
    except: 
        print(f'Cound not read in: JV. Forward scan. PCE [%] from: {fileName}')
        data['JV_forward_scan_PCE'] = ''

    #%% JV. Forward scan. Vmp [V]
    try:
        data['JV_forward_scan_Vmp'] = cdf.VocData(userData['JV. Forward scan. Vmp [V]'], mV_to_V_cutoff = 10)
    except: 
        print(f'Cound not read in: JV. Forward scan. Vmp [V] from: {fileName}')
        data['JV_forward_scan_Vmp'] = ''

    #%% JV. Forward scan. Jmp [mA/cm^2]
    try:
        data['JV_forward_scan_Jmp'] = cdf.JscData(userData['JV. Forward scan. Jmp [mA/cm^2]'])
    except: 
        print(f'Cound not read in: JV. Forward scan. Jmp [mA/cm^2] from: {fileName}')
        data['JV_forward_scan_Jmp'] = ''

    #%% JV. Forward scan. Series resistance [ohmcm^2]
    try:
        data['JV_forward_scan_series_resistance'] = cdf.numericValues(userData['JV. Forward scan. Series resistance [ohmcm^2]'])
    except: 
        print(f'Cound not read in: JV. Forward scan. Series resistance [ohmcm^2] from: {fileName}')
        data['JV_forward_scan_series_resistance'] = ''

    #%% JV. Forward scan. Shunt resistance [ohmcm^2]
    try:
        data['JV_forward_scan_shunt_resistance'] = cdf.numericValues(userData['JV. Forward scan. Shunt resistance [ohmcm^2]'])
    except: 
        print(f'Cound not read in: JV. Forward scan. Shunt resistance [ohmcm^2] from: {fileName}')
        data['JV_forward_scan_shunt_resistance'] = ''

    #%% JV. Link. Raw data
    try:
        data['JV_link_raw_data'] = cdf.convertToString(userData['JV. Link. Raw data'])
    except: 
        print(f'Cound not read in: JV. Link. Raw data from: {fileName}')
        data['JV_link_raw_data'] = '' 

    #%% Stabilised performance. Measured [TRUE/FALSE]
    try:
        data['Stabilised_performance_measured'] = cdf.trueOrFalse(userData['Stabilised performance. Measured [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Stabilised performance. Measured [TRUE/FALSE] from: {fileName}')
        data['Stabilised_performance_measured'] = ''

    #%% Stabilised performance. Procedure [MPPT/Constant potential/Constant current/ …]
    try:
        data['Stabilised_performance_procedure'] = cdf.convertToString(userData['Stabilised performance. Procedure [MPPT/Constant potential/Constant current/ …]'])
    except: 
        print(f'Cound not read in: Stabilised performance. Procedure [MPPT/Constant potential/Constant current/ …] from: {fileName}')
        data['Stabilised_performance_procedure'] = '' 

    #%% Stabilised performance. Procedure. Metrics [Potential in V, Current in mA/cm^2, ...]
    try:
        data['Stabilised_performance_procedure_metrics'] = cdf.convertToString(userData['Stabilised performance. Procedure. Metrics [Potential in V, Current in mA/cm^2, ...]'])
    except: 
        print(f'Cound not read in: Stabilised performance. Procedure. Metrics [Potential in V, Current in mA/cm^2, ...] from: {fileName}')
        data['Stabilised_performance_procedure_metrics'] = ''

    #%% Stabilised performance. Measurement time [min]
    try:
        data['Stabilised_performance_measurement_time'] = cdf.numericValues(userData['Stabilised performance. Measurement time [min]'])
    except: 
        print(f'Cound not read in: Stabilised performance. Measurement time [min] from: {fileName}')
        data['Stabilised_performance_measurement_time'] = ''

    #%% Stabilised performance. PCE [%]
    try:
        data['Stabilised_performance_PCE'] = cdf.PCEData(userData['Stabilised performance. PCE [%]'])
    except: 
        print(f'Cound not read in: Stabilised performance. PCE [%] from: {fileName}')
        data['Stabilised_performance_PCE'] = ''

    #%% Stabilised performance. Vmp [V]
    try:
        data['Stabilised_performance_Vmp'] = cdf.VocData(userData['Stabilised performance. Vmp [V]'], mV_to_V_cutoff = 10)
    except: 
        print(f'Cound not read in: Stabilised performance. Vmp [V] from: {fileName}')
        data['Stabilised_performance_Vmp'] = ''

    #%% Stabilised performance. Jmp [mA/cm^2]
    try:
        data['Stabilised_performance_Jmp'] = cdf.JscData(userData['Stabilised performance. Jmp [mA/cm^2]'])
    except: 
        print(f'Cound not read in: Stabilised performance. Jmp [mA/cm^2] from: {fileName}')
        data['Stabilised_performance_Jmp'] = ''

    #%% Stabilised performance. Link. Raw data
    try:
        data['Stabilised_performance_link_raw_data'] = cdf.convertToString(userData['Stabilised performance. Link. Raw data'])
    except: 
        print(f'Cound not read in: Stabilised performance. Link. Raw data from: {fileName}')
        data['Stabilised_performance_link_raw_data'] = '' 

    #%% EQE. Measured [TRUE/FALSE]
    try:
        data['EQE_measured'] = cdf.trueOrFalse(userData['EQE. Measured [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: EQE. Measured [TRUE/FALSE] from: {fileName}')
        data['EQE_measured'] = ''

    #%% EQE. Light bias [mW/cm^2]
    try:
        data['EQE_light_bias'] = cdf.numericValues(userData['EQE. Light bias [mW/cm^2]'])
    except: 
        print(f'Cound not read in: EQE. Light bias [mW/cm^2] from: {fileName}')
        data['EQE_light_bias'] = ''

    #%% EQE. Integrated Jsc [mA/cm^2]
    try:
        data['EQE_integrated_Jsc'] = cdf.JscData(userData['EQE. Integrated Jsc [mA/cm^2]'])
    except: 
        print(f'Cound not read in: EQE. Integrated Jsc [mA/cm^2] from: {fileName}')
        data['EQE_integrated_Jsc'] = ''

    #%% EQE. Link. Raw data
    try:
        data['EQE_link_raw_data'] = cdf.convertToString(userData['EQE. Link. Raw data'])
    except: 
        print(f'Cound not read in: EQE. Link. Raw data from: {fileName}')
        data['EQE_link_raw_data'] = '' 

    #%% Stability. Measured [TRUE/FALSE]
    try:
        data['Stability_measured'] = cdf.trueOrFalse(userData['Stability. Measured [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Stability. Measured [TRUE/FALSE] from: {fileName}')
        data['Stability_measured'] = ''

    #%% Stability. Protocol [ISOS x/IEC x/ …]
    try:
        data['Stability_protocol'] = cdf.convertToString(userData['Stability. Protocol [ISOS x/IEC x/ …]'])
    except: 
        print(f'Cound not read in: Stability. Protocol [ISOS x/IEC x/ …] from: {fileName}')
        data['Stability_protocol'] = '' 

    #%% Stability. Average over N number of cells
    try:
        data['Stability_average_over_n_number_of_cells'] = cdf.numericInteger(userData['Stability. Average over N number of cells'], default = 1)
    except: 
        print(f'Cound not read in: Stability. Average over N number of cells from: {fileName}')
        data['Stability_average_over_n_number_of_cells'] = ''
    
    #%% Stability. Light source. Type [Dark/White LED/Metal halide/ ...]
    try:
        data['Stability_light_source_type'] = cdf.convertToString(userData['Stability. Light source. Type [Dark/White LED/Metal halide/ ...]'])
    except: 
        print(f'Cound not read in: Stability. Light source. Type [Dark/White LED/Metal halide/ ...] from: {fileName}')
        data['Stability_light_source_type'] = ''       
  
    #%% Stability. Light source. Brand name
    try:
        data['Stability_light_source_brand_name'] = cdf.convertToString(userData['Stability. Light source. Brand name'])
    except: 
        print(f'Cound not read in: Stability. Light source. Brand name from: {fileName}')
        data['Stability_light_source_brand_name'] = '' 
              
    #%% Stability. Light source. Simulator class
    try:
        data['Stability_light_source_simulator_class'] = cdf.convertToString(userData['Stability. Light source. Simulator class'])
    except: 
        print(f'Cound not read in: Stability. Light source. Simulator class from: {fileName}')
        data['Stability_light_source_simulator_class'] = ''
                
    #%% Stability. Light. Intensity [mW/cm^2]
    try:
        data['Stability_light_intensity'] = cdf.numericValues(userData['Stability. Light. Intensity [mW/cm^2]'])
    except: 
        print(f'Cound not read in: Stability. Light. Intensity [mW/cm^2] from: {fileName}')
        data['Stability_light_intensity'] = ''

    #%% Stability. Light. Spectra [AM 1.5/UVA/UVB/Monochromatic/ …]
    try:
        data['Stability_light_spectra'] = cdf.convertToString(userData['Stability. Light. Spectra [AM 1.5/UVA/UVB/Monochromatic/ …]'])
    except: 
        print(f'Cound not read in: Stability. Light. Spectra [AM 1.5/UVA/UVB/Monochromatic/ …] from: {fileName}')
        data['Stability_light_spectra'] = ''
   
    #%% Stability. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm]
    try:
        data['Stability_light_wavelength_range'] = cdf.numberHighLowOrConstant(userData['Stability. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm]'])
    except: 
        print(f'Cound not read in: Stability. Light. Wavelength range [lambda min; lambda max] or [lambda constant] [nm] from: {fileName}')
        data['Stability_light_wavelength_range'] = ''
   
    #%% Stability. Light. Illumination direction [Substrate/superstrate]
    try:
        data['Stability_light_illumination_direction'] = cdf.convertToString(userData['Stability. Light. Illumination direction [Substrate/superstrate]'])
    except: 
        print(f'Cound not read in: Stability. Light. Illumination direction [Substrate/superstrate] {fileName}')
        data['Stability_light_illumination_direction'] = ''   
  
    #%% Stability. Light. Load condition [Continuous/Cycled/Day-nigh/ …]
    try:
        data['Stability_light_load_condition'] = cdf.convertToString(userData['Stability. Light. Load condition [Continuous/Cycled/Day-nigh/ …]'])
    except: 
        print(f'Cound not read in: Stability. Light. Load condition [Continuous/Cycled/Day-nigh/ …] {fileName}')
        data['Stability_light_load_condition'] = ''           

    #%% Stability. Light. Cycling times [time in low light; time in high light] [h]
    try:
        data['Stability_light_cycling_times'] = cdf.time(userData['Stability. Light. Cycling times [time in low light; time in high light] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Stability. Light. Cycling times [time in low light; time in high light] [h] from: {fileName}')
        data['Stability_light_cycling_times'] = ''

    #%% Stability. Light. UV filter [TRUE/FALSE]
    try:
        data['Stability_light_UV_filter'] = cdf.trueOrFalse(userData['Stability. Light. UV filter [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Stability. Light. UV filter [TRUE/FALSE] from: {fileName}')
        data['Stability_light_UV_filter'] = ''

    #%% Stability. Potential bias. Load condition [Open circuit/MPPT/Constant potential/ …]
    try:
        data['Stability_potential_bias_load_condition'] = cdf.potentialBias(userData['Stability. Potential bias. Load condition [Open circuit/MPPT/Constant potential/ …]'])
    except: 
        print(f'Cound not read in: Stability. Potential bias. Load condition [Open circuit/MPPT/Constant potential/ …] {fileName}')
        data['Stability_potential_bias_load_condition'] = ''           

    #%% Stability. Potential bias. Range [U.min; U.max] or [U.constant] [V]
    try:
        data['Stability_potential_bias_range'] = cdf.numberHighLowOrConstant(userData['Stability. Potential bias. Range [U.min; U.max] or [U.constant] [V]'])
    except: 
        print(f'Cound not read in: Stability. Potential bias. Range [U.min; U.max] or [U.constant] [V] from: {fileName}')
        data['Stability_potential_bias_range'] = ''
   
    #%% Stability. Potential bias. Passive resistance [ohm]
    try:
        data['Stability_potential_bias_passive_resistance'] = cdf.numericValues(userData['Stability. Potential bias. Passive resistance [ohm]'])
    except: 
        print(f'Cound not read in: Stability. Potential bias. Passive resistance [ohm] from: {fileName}')
        data['Stability_potential_bias_passive_resistance'] = ''

    #%% Stability. Temperature. Load condition [Constant/Uncontrolled/Cycled/ ...]
    try:
        data['Stability_temperature_load_condition'] = cdf.convertToString(userData['Stability. Temperature. Load condition [Constant/Uncontrolled/Cycled/ ...]'])
    except: 
        print(f'Cound not read in: Stability. Temperature. Load condition [Constant/Uncontrolled/Cycled/ ...] {fileName}')
        data['Stability_temperature_load_condition'] = ''           

    #%% Stability. Temperature. Range [T.min; T.max] or [T.constant] [deg. C]
    try:
        data['Stability_temperature_range'] = cdf.numberHighLowOrConstant(userData['Stability. Temperature. Range [T.min; T.max] or [T.constant] [deg. C]'])
    except: 
        print(f'Cound not read in: Stability. Temperature. Range [T.min; T.max] or [T.constant] [deg. C] from: {fileName}')
        data['Stability_temperature_range'] = ''
   
    #%% Stability. Temperature. Cycling times [t at T.min; t at T.max] [h]
    try:
        data['Stability_temperature_cycling_times'] = cdf.time(userData['Stability. Temperature. Cycling times [t at T.min; t at T.max] [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Stability. Temperature. Cycling times [t at T.min; t at T.max] [h] from: {fileName}')
        data['Stability_temperature_cycling_times'] = ''

    #%% Stability. Temperature. Ramp speed [deg. C/min]
    try:
        data['Stability_temperature_ramp_speed'] = cdf.numericValues(userData['Stability. Temperature. Ramp speed [deg. C/min]'])
    except: 
        print(f'Cound not read in: Stability. Stability. Temperature. Ramp speed [deg. C/min] from: {fileName}')
        data['Stability_temperature_ramp_speed'] = ''

    #%% Stability. Atmosphere [Gas1; Gas2; ...]
    try:
        data['Stability_atmosphere'] = cdf.atmosphere(userData['Stability. Atmosphere [Gas1; Gas2; ...]'])
    except: 
        print(f'Cound not read in: Stability. Atmosphere [Gas1; Gas2; ...] from: {fileName}')
        data['Stability_atmosphere'] = ''

    #%% Stability. Atmosphere. Oxygen concentration [%]
    try:
        data['Stability_atmosphere_oxygen_concentration'] = cdf.numericValues(userData['Stability. Atmosphere. Oxygen concentration [%]'])
    except: 
        print(f'Cound not read in: Stability. Atmosphere. Oxygen concentration [%] from: {fileName}')
        data['Stability_atmosphere_oxygen_concentration'] = ''

    #%% Stability. Relative humidity. Load conditions [Ambient/Controlled/Cycled/ …]
    try:
        data['Stability_relative_humidity_load_conditions'] = cdf.convertToString(userData['Stability. Relative humidity. Load conditions [Ambient/Controlled/Cycled/ …]'])
    except: 
        print(f'Cound not read in: Stability. Relative humidity. Load conditions [Ambient/Controlled/Cycled/ …] {fileName}')
        data['Stability_relative_humidity_load_conditions'] = ''           

    #%% Stability. Relative humidity. Range [RH.min; RH.max] [%]
    try:
        data['Stability_relative_humidity_range'] = cdf.numberHighLowOrConstant(userData['Stability. Relative humidity. Range [RH.min; RH.max] [%]'])
    except: 
        print(f'Cound not read in: Stability. Relative humidity. Range [RH.min; RH.max] [%] from: {fileName}')
        data['Stability_relative_humidity_range'] = ''

    #%% Stability. Relative humidity. Average value [%]
    try:
        data['Stability_relative_humidity_average_value'] = cdf.numericValues(userData['Stability. Relative humidity. Average value [%]'])
    except: 
        print(f'Cound not read in: Stability. Relative humidity. Average value [%] from: {fileName}')
        data['Stability_relative_humidity_average_value'] = ''

    #%% Stability. Time. Total exposure [h]
    try:
        data['Stability_time_total_exposure'] = cdf.numericValues(userData['Stability. Time. Total exposure [h]'])
    except: 
        print(f'Cound not read in: Stability. Time. Total exposure [h] from: {fileName}')
        data['Stability_time_total_exposure'] = '' 
        
    #%% Stability. Periodic JV measurements [TRUE/FALSE]
    try:
        data['Stability_periodic_JV_measurements'] = cdf.trueOrFalse(userData['Stability. Periodic JV measurements [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Stability. Periodic JV measurements [TRUE/FALSE] from: {fileName}')
        data['Stability_periodic_JV_measurements'] = ''

    #%% Stability. Periodic JV measurements. Time between measurements [h]
    try:
        data['Stability_periodic_JV_measurements_time_between_measurements'] = cdf.time(userData['Stability. Periodic JV measurements. Time between measurements [h]'], givenUnit = 'h', desiredUnit = 'h')
    except: 
        print(f'Cound not read in: Stability. Periodic JV measurements. Time between measurements [h] from: {fileName}')
        data['Stability_periodic_JV_measurements_time_between_measurements'] = ''

    #%% Stability. PCE. Initial value [%]
    try:
        data['Stability_PCE_initial_value'] = cdf.numericValues(userData['Stability. PCE. Initial value [%]'])
    except: 
        print(f'Cound not read in: Stability. PCE. Initial value [%] from: {fileName}')
        data['Stability_PCE_initial_value'] = ''
  
    #%% Stability. PCE. Burn in observed [TRUE/FALSE]
    try:
        data['Stability_PCE_burn_in_observed'] = cdf.trueOrFalse(userData['Stability. PCE. Burn in observed [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Stability. PCE. Burn in observed [TRUE/FALSE] from: {fileName}')
        data['Stability_PCE_burn_in_observed'] = ''

    #%% Stability. PCE. End of experiment [% of initial PCE]
    try:
        data['Stability_PCE_end_of_experiment'] = cdf.numericValues(userData['Stability. PCE. End of experiment [% of initial PCE]'])
    except: 
        print(f'Cound not read in: Stability. PCE. End of experiment [% of initial PCE] from: {fileName}')
        data['Stability_PCE_end_of_experiment'] = ''

    #%% Stability. PCE. T95 [h]
    try:
        data['Stability_PCE_T95'] = cdf.numericValues(userData['Stability. PCE. T95 [h]'])
    except: 
        print(f'Cound not read in: Stability. PCE. T95 [h] from: {fileName}')
        data['Stability_PCE_T95'] = ''

    #%% Stability. PCE. Ts95 [h]
    try:
        data['Stability_PCE_Ts95'] = cdf.numericValues(userData['Stability. PCE. Ts95 [h]'])
    except: 
        print(f'Cound not read in: Stability. PCE. Ts95 [h] from: {fileName}')
        data['Stability_PCE_Ts95'] = ''

    #%% Stability. PCE. T80 [h]
    try:
        data['Stability_PCE_T80'] = cdf.numericValues(userData['Stability. PCE. T80 [h]'])
    except: 
        print(f'Cound not read in: Stability. PCE. T80 [h] from: {fileName}')
        data['Stability_PCE_T80'] = ''

    #%% Stability. PCE. Ts80 [h]
    try:
        data['Stability_PCE_Ts80'] = cdf.numericValues(userData['Stability. PCE. Ts80 [h]'])
    except: 
        print(f'Cound not read in: Stability. PCE. Ts80 [h] from: {fileName}')
        data['Stability_PCE_Ts80'] = ''

    #%% Stability. PCE. Te80 [h]
    try:
        data['Stability_PCE_Te80'] = cdf.numericValues(userData['Stability. PCE. Te80 [h]'])
    except: 
        print(f'Cound not read in: Stability. PCE. Te80 [h] from: {fileName}')
        data['Stability_PCE_Te80'] = ''

    #%% Stability. PCE. Tse80 [h]
    try:
        data['Stability_PCE_Tse80'] = cdf.numericValues(userData['Stability. PCE. Tse80 [h]'])
    except: 
        print(f'Cound not read in: Stability. PCE. Tse80 [h] from: {fileName}')
        data['Stability_PCE_Tse80'] = ''

    #%% Stability. PCE. After 1000 h [% of initial PCE]
    try:
        data['Stability_PCE_after_1000_h'] = cdf.numericValues(userData['Stability. PCE. After 1000 h [% of initial PCE]'])
    except: 
        print(f'Cound not read in: Stability. PCE. After 1000 h [% of initial PCE] from: {fileName}')
        data['Stability_PCE_after_1000_h'] = ''
 
    #%% Stability. Lifetime energy yield [kWh/m^2]
    try:
        data['Stability_lifetime_energy_yield'] = cdf.numericValues(userData['Stability. Lifetime energy yield [kWh/m^2]'])
    except: 
        print(f'Cound not read in: Stability. Lifetime energy yield [kWh/m^2] from: {fileName}')
        data['Stability_lifetime_energy_yield'] = ''

    #%% Stability. Flexible cell. Number of bending cycles
    try:
        data['Stability_flexible_cell_number_of_bending_cycles'] = cdf.numericInteger(userData['Stability. Flexible cell. Number of bending cycles'], default = 0)
    except: 
        print(f'Cound not read in: Stability. Flexible cell. Number of bending cycles from: {fileName}')
        data['Stability_flexible_cell_number_of_bending_cycles'] = ''    
        
    #%% Stability. Flexible cell. Bending radius [degrees]
    try:
        data['Stability_flexible_cell_bending_radius'] = cdf.numericValues(userData['Stability. Flexible cell. Bending radius [degrees]'])
    except: 
        print(f'Cound not read in: Stability. Flexible cell. Bending radius [degrees] from: {fileName}')
        data['Stability_flexible_cell_bending_radius'] = ''       

    #%% Stability. Flexible cell. PCE. Initial value [%]
    try:
        data['Stability_flexible_cell_PCE_initial_value'] = cdf.numericValues(userData['Stability. Flexible cell. PCE. Initial value [%]'])
    except: 
        print(f'Cound not read in: Stability. Flexible cell. PCE. Initial value [%] from: {fileName}')
        data['Stability_flexible_cell_PCE_initial_value'] = '' 

    #%% Stability. Flexible cell. PCE. End of experiment [% of initial PCE]
    try:
        data['Stability_flexible_cell_PCE_end_of_experiment'] = cdf.numericValues(userData['Stability. Flexible cell. PCE. End of experiment [% of initial PCE]'])
    except: 
        print(f'Cound not read in: Stability. Flexible cell. PCE. End of experiment [% of initial PCE]: {fileName}')
        data['Stability_flexible_cell_PCE_end_of_experiment'] = '' 
   
    #%% Stability. Link. Raw data for stability trace
    try:
        data['Stability_link_raw_data_for_stability_trace'] = cdf.convertToString(userData['Stability. Link. Raw data for stability trace'])
    except: 
        print(f'Cound not read in: Stability. Link. Raw data for stability trace {fileName}')
        data['Stability_link_raw_data_for_stability_trace'] = ''           
   
    #%% Outdoor. Tested [TRUE/FALSE]
    try:
        data['Outdoor_tested'] = cdf.trueOrFalse(userData['Outdoor. Tested [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Outdoor. Tested [TRUE/FALSE] from: {fileName}')
        data['Outdoor_tested'] = ''

    #%% Outdoor. Protocol [ISOS x/IEC x/ …]
    try:
        data['Outdoor_protocol'] = cdf.convertToString(userData['Outdoor. Protocol [ISOS x/IEC x/ …]'])
    except: 
        print(f'Cound not read in: Outdoor. Protocol [ISOS x/IEC x/ …] from: {fileName}')
        data['Outdoor_protocol'] = '' 

    #%% Outdoor. Average over N number of cells
    try:
        data['Outdoor_average_over_n_number_of_cells'] = cdf.numericInteger(userData['Outdoor. Average over N number of cells'], default = 1)
    except: 
        print(f'Cound not read in: Outdoor. Average over N number of cells from: {fileName}')
        data['Outdoor_average_over_n_number_of_cells'] = ''
            
    #%% Outdoor. Location. Country [Country]
    try:
        data['Outdoor_location_country'] = cdf.convertToString(userData['Outdoor. Location. Country [Country]'])
    except: 
        print(f'Cound not read in: Outdoor. Location. Country [Country] {fileName}')
        data['Outdoor_location_country'] = ''           
      
    #%% Outdoor. Location. City [City]
    try:
        data['Outdoor_location_city'] = cdf.convertToString(userData['Outdoor. Location. City [City]'])
    except: 
        print(f'Cound not read in: Outdoor. Location. City [City] {fileName}')
        data['Outdoor_location_city'] = ''        

    #%% Outdoor. Location. Coordinates [Latitude; Longitude] [decimal degrees]
    try:
        data['Outdoor_location_coordinates'] = cdf.numberHighLowOrConstant(userData['Outdoor. Location. Coordinates [Latitude; Longitude] [decimal degrees]'])
    except: 
        print(f'Cound not read in: Outdoor. Location. Coordinates [Latitude; Longitude] [decimal degrees] {fileName}')
        data['Outdoor_location_coordinates'] = ''   

    #%% Outdoor. Location. Climate zone [Tropical/Subtropical/Temperate/Cold]
    try:
        data['Outdoor_location_climate_zone'] = cdf.convertToString(userData['Outdoor. Location. Climate zone [Tropical/Subtropical/Temperate/Cold]'])
    except: 
        print(f'Cound not read in: Outdoor. Location. Climate zone [Tropical/Subtropical/Temperate/Cold] from: {fileName}')
        data['Outdoor_location_climate_zone'] = ''        

    #%% Outdoor. Installation. Tilt [degrees]
    try:
        data['Outdoor_installation_tilt'] = cdf.numericValues(userData['Outdoor. Installation. Tilt [degrees]'])
    except: 
        print(f'Cound not read in: Outdoor. Installation. Tilt [degrees] from: {fileName}')
        data['Outdoor_installation_tilt'] = '' 

    #%% Outdoor. Installation. Cardinal direction [degrees]
    try:
        data['Outdoor_installation_cardinal_direction'] = cdf.numericValues(userData['Outdoor. Installation. Cardinal direction [degrees]'])
    except: 
        print(f'Cound not read in: Outdoor. Installation. Cardinal direction [degrees] from: {fileName}')
        data['Outdoor_installation_cardinal_direction'] = '' 

    #%% Outdoor. Installation. Number of solar tracking axis [0/1/2]
    try:
        data['Outdoor_installation_number_of_solar_tracking_axis'] = cdf.numericInteger(userData['Outdoor. Installation. Number of solar tracking axis [0/1/2]'], default = 0)
    except: 
        print(f'Cound not read in: Outdoor. Installation. Number of solar tracking axis [0/1/2] from: {fileName}')
        data['Outdoor_installation_number_of_solar_tracking_axis'] = ''
     
    #%% Outdoor. Time. Season [Winter/Summer/ …]
    try:
        data['Outdoor_time_season'] = cdf.convertToString(userData['Outdoor. Time. Season [Winter/Summer/ …]'])
    except: 
        print(f'Cound not read in: Outdoor. Time. Season [Winter/Summer/ …] from: {fileName}')
        data['Outdoor_time_season'] = ''        

    #%% Outdoor. Time. Start [year:mm:dd:hh:mm]
    try:
        data['Outdoor_time_start'] = cdf.dateTime(userData['Outdoor. Time. Start [year:mm:dd:hh:mm]'])
    except: 
        print(f'Cound not read in: Outdoor. Time. Start [year:mm:dd:hh:mm] from: {fileName}')
        data['Outdoor_time_start'] = ''        
 
    #%% Outdoor. Time. End [year:mm:dd:hh:mm]
    try:
        data['Outdoor_time_end'] = cdf.dateTime(userData['Outdoor. Time. End [year:mm:dd:hh:mm]'])
    except: 
        print(f'Cound not read in: Outdoor. Time. End [year:mm:dd:hh:mm] from: {fileName}')
        data['Outdoor_time_end'] = '' 
      
    #%% Outdoor. Time. Total exposure [days]
    try:
        data['Outdoor_time_total_exposure'] = cdf.numericValues(userData['Outdoor. Time. Total exposure [days]'])
    except: 
        print(f'Cound not read in: Outdoor. Time. Total exposure [days] from: {fileName}')
        data['Outdoor_time_total_exposure'] = '' 
  
    #%% Outdoor. Potential bias. Load condition [Open circuit/MPPT/Constant potential/ …]
    try:
        data['Outdoor_potential_bias_load_condition'] = cdf.convertToString(userData['Outdoor. Potential bias. Load condition [Open circuit/MPPT/Constant potential/ …]'])
    except: 
        print(f'Cound not read in: Outdoor. Potential bias. Load condition [Open circuit/MPPT/Constant potential/ …] from: {fileName}')
        data['Outdoor_potential_bias_load_condition'] = ''        
    
    #%% Outdoor. Potential bias. Range [U.min; U.max] or [U.constant] [V]
    try:
        data['Outdoor_potential_bias_range'] = cdf.numberHighLowOrConstant(userData['Outdoor. Potential bias. Range [U.min; U.max] or [U.constant] [V]'])
    except: 
        print(f'Cound not read in: Outdoor. Potential bias. Range [U.min; U.max] or [U.constant] [V] from: {fileName}')
        data['Outdoor_potential_bias_range'] = ''
   
    #%% Outdoor. Potential bias. Passive resistance [ohm]
    try:
        data['Outdoor_potential_bias_passive_resistance'] = cdf.numericValues(userData['Outdoor. Potential bias. Passive resistance [ohm]'])
    except: 
        print(f'Cound not read in: Outdoor. Potential bias. Passive resistance [ohm] from: {fileName}')
        data['Outdoor_potential_bias_passive_resistance'] = ''
   
    #%% Outdoor. Temperature. Load condition [Constant/Uncontrolled/Cycled/ ...]
    try:
        data['Outdoor_temperature_load_condition'] = cdf.convertToString(userData['Outdoor. Temperature. Load condition [Constant/Uncontrolled/Cycled/ ...]'])
    except: 
        print(f'Cound not read in: Outdoor. Temperature. Load condition [Constant/Uncontrolled/Cycled/ ...] {fileName}')
        data['Outdoor_temperature_load_condition'] = ''           

    #%% Outdoor. Temperature. Range [T.min; T.max] or [T.constant] [deg. C]
    try:
        data['Outdoor_temperature_range'] = cdf.numberHighLowOrConstant(userData['Outdoor. Temperature. Range [T.min; T.max] or [T.constant] [deg. C]'])
    except: 
        print(f'Cound not read in: Outdoor. Temperature. Range [T.min; T.max] or [T.constant] [deg. C] from: {fileName}')
        data['Outdoor_temperature_range'] = ''
          
    #%% Outdoor. Temperature. Tmodule [degrees C]
    try:
        data['Outdoor_temperature_tmodule'] = cdf.numericValues(userData['Outdoor. Temperature. Tmodule [degrees C]'])
    except: 
        print(f'Cound not read in: Outdoor. Temperature. Tmodule [degrees C] from: {fileName}')
        data['Outdoor_temperature_tmodule'] = '' 
  
    #%% Outdoor. Periodic JV measurements [TRUE/FALSE]
    try:
        data['Outdoor_periodic_JV_measurements'] = cdf.trueOrFalse(userData['Outdoor. Periodic JV measurements [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Outdoor. Periodic JV measurements [TRUE/FALSE] from: {fileName}')
        data['Outdoor_periodic_JV_measurements'] = ''
      
    #%% Outdoor. Periodic JV measurements. Time between measurements [h]
    try:
        data['Outdoor_periodic_JV_measurements_time_between_measurements'] = cdf.numericValues(userData['Outdoor. Periodic JV measurements. Time between measurements [h]'])
    except: 
        print(f'Cound not read in: Outdoor. Periodic JV measurements. Time between measurements [h] from: {fileName}')
        data['Outdoor_periodic_JV_measurements_time_between_measurements'] = '' 
  
    #%% Outdoor. PCE. Initial value [%]
    try:
        data['Outdoor_PCE_initial_value'] = cdf.numericValues(userData['Outdoor. PCE. Initial value [%]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. Initial value [%] from: {fileName}')
        data['Outdoor_PCE_initial_value'] = ''
  
    #%% Outdoor. PCE. Burn in observed [TRUE/FALSE]
    try:
        data['Outdoor_PCE_burn_in_observed'] = cdf.trueOrFalse(userData['Outdoor. PCE. Burn in observed [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. Burn in observed [TRUE/FALSE] from: {fileName}')
        data['Outdoor_PCE_burn_in_observed'] = ''

    #%% Outdoor. PCE. End of experiment [% of initial PCE]
    try:
        data['Outdoor_PCE_end_of_experiment'] = cdf.numericValues(userData['Outdoor. PCE. End of experiment [% of initial PCE]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. End of experiment [% of initial PCE] from: {fileName}')
        data['Outdoor_PCE_end_of_experiment'] = ''

    #%% Outdoor. PCE. T95 [h]
    try:
        data['Outdoor_PCE_T95'] = cdf.numericValues(userData['Outdoor. PCE. T95 [h]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. T95 [h] from: {fileName}')
        data['Outdoor_PCE_T95'] = ''

    #%% Outdoor. PCE. Ts95 [h]
    try:
        data['Outdoor_PCE_Ts95'] = cdf.numericValues(userData['Outdoor. PCE. Ts95 [h]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. Ts95 [h] from: {fileName}')
        data['Outdoor_PCE_Ts95'] = ''

    #%% Outdoor. PCE. T80 [h]
    try:
        data['Outdoor_PCE_T80'] = cdf.numericValues(userData['Outdoor. PCE. T80 [h]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. T80 [h] from: {fileName}')
        data['Outdoor_PCE_T80'] = ''

    #%% Outdoor. PCE. Ts80 [h]
    try:
        data['Outdoor_PCE_Ts80'] = cdf.numericValues(userData['Outdoor. PCE. Ts80 [h]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. Ts80 [h] from: {fileName}')
        data['Outdoor_PCE_Ts80'] = ''

    #%% Outdoor. PCE. Te80 [h]
    try:
        data['Outdoor_PCE_Te80'] = cdf.numericValues(userData['Outdoor. PCE. Te80 [h]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. Te80 [h] from: {fileName}')
        data['Outdoor_PCE_Te80'] = ''

    #%% Outdoor. PCE. Tse80 [h]
    try:
        data['Outdoor_PCE_Tse80'] = cdf.numericValues(userData['Outdoor. PCE. Tse80 [h]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. Tse80 [h] from: {fileName}')
        data['Outdoor_PCE_Tse80'] = ''

    #%% Outdoor. PCE. After 1000 h [% of initial PCE]
    try:
        data['Outdoor_PCE_after_1000_h'] = cdf.numericValues(userData['Outdoor. PCE. After 1000 h [% of initial PCE]'])
    except: 
        print(f'Cound not read in: Outdoor. PCE. After 1000 h [% of initial PCE] from: {fileName}')
        data['Outdoor_PCE_after_1000_h'] = ''
 
    #%% Outdoor. Power generated [kWh/year/m^2]
    try:
        data['Outdoor_power_generated'] = cdf.numericValues(userData['Outdoor. Power generated [kWh/year/m^2]'])
    except: 
        print(f'Cound not read in: Outdoor. Power generated [kWh/year/m^2] from: {fileName}')
        data['Outdoor_power_generated'] = ''
 
    #%% Outdoor. Link. Raw data for outdoor trace
    try:
        data['Outdoor_link_raw_data_for_outdoor_trace'] = cdf.convertToString(userData['Outdoor. Link. Raw data for outdoor trace'])
    except: 
        print(f'Cound not read in: Outdoor. Link. Raw data for outdoor trace from: {fileName}')
        data['Outdoor_link_raw_data_for_outdoor_trace'] = ''           

    #%% Outdoor. Detaild weather data available [TRUE/FALSE]
    try:
        data['Outdoor_detaild_weather_data_available'] = cdf.trueOrFalse(userData['Outdoor. Detaild weather data available [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Outdoor. Detaild weather data available [TRUE/FALSE] from: {fileName}')
        data['Outdoor_detaild_weather_data_available'] = ''
   
    #%% Outdoor. Link. Detailed weather data
    try:
        data['Outdoor_link_detailed_weather_data'] = cdf.convertToString(userData['Outdoor. Link. Detailed weather data'])
    except: 
        print(f'Cound not read in: Outdoor. Link. Detailed weather data from: {fileName}')
        data['Outdoor_link_detailed_weather_data'] = ''  
      
    #%% Outdoor. Spectral data available [TRUE/FALSE]
    try:
        data['Outdoor_spectral_data_available'] = cdf.trueOrFalse(userData['Outdoor. Spectral data available [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Outdoor. Spectral data available [TRUE/FALSE] from: {fileName}')
        data['Outdoor_spectral_data_available'] = ''

    #%% Outdoor. Link. Spectral data
    try:
        data['Outdoor_link_spectral_data'] = cdf.convertToString(userData['Outdoor. Link. Spectral data'])
    except: 
        print(f'Cound not read in: Outdoor. Link. Spectral data from: {fileName}')
        data['Outdoor_link_spectral_data'] = ''  

    #%% Outdoor. Irradiance measured [TRUE/FALSE]
    try:
        data['Outdoor_irradiance_measured'] = cdf.trueOrFalse(userData['Outdoor. Irradiance measured [TRUE/FALSE]'])
    except: 
        print(f'Cound not read in: Outdoor. Irradiance measured [TRUE/FALSE] from: {fileName}')
        data['Outdoor_irradiance_measured'] = ''

    #%% Outdoor. Link. Irradiance data 
    try:
        data['Outdoor_link_irradiance_data '] = cdf.convertToString(userData['Outdoor. Link. Irradiance data'])
    except: 
        print(f'Cound not read in: Outdoor. Link. Irradiance data from: {fileName}')
        data['Outdoor_link_irradiance_data'] = '' 

    #%% Finish
    print(f'Finished data cleaning procedure for {fileName}')
    return data

 

#%% Old stuff
def oldFunctions(userData, fileName):

    #%% Ref. Part of the initial dataset
    data['Ref_part_of_initial_dataset'] = False

        #%% Perovskite. Composition. Short form (A-ions B-ions C-ions. Each in alphabetic order)
    try:
        data['Perovskite_composition_short_form'] = cdf.perovskiteShortForm(userData['Perovskite. Composition. Short form (A-ions B-ions C-ions. Each in alphabetic order)'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. Short form (A-ions B-ions C-ions. Each in alphabetic order) from: {fileName}')
        data['Perovskite_composition_short_form'] = ''

    #%% Perovskite. Composition. Long form (PLEASE FOLLOW INSTRUCTIONS!)
    try:
        data['Perovskite_composition_long_form'] = cdf.perovskiteLongForm(userData['Perovskite. Composition. Long form (PLEASE FOLLOW INSTRUCTIONS!)'])
    except: 
        print(f'Cound not read in: Perovskite. Composition. Long form (PLEASE FOLLOW INSTRUCTIONS!): {fileName}')
        data['Perovskite_composition_long_form'] = ''

    #%% Additional layers. Substrate side. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...] 
    try:
        data['Additional_layers_substrate_side_function'] = cdf.convertToString(userData['Additional layers. Substrate side. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]'])
    except: 
        print(f'Cound not read in: Additional layers. Substrate side. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...] from: {fileName}')
        data['Additional_layers_substrate_side_function'] = ''

    #%% Additional layers. Substrate side. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Additional_layers_substrate_side_stack_sequence'] = cdf.stackSequence(userData['Additional layers. Substrate side. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Additional layers. Substrate side. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Additional_layers_substrate_side_stack_sequence'] = ''

    #%% Additional layers. Substrate side. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['Additional_layers_substrate_side_thickness_list'] = cdf.thickness(userData['Additional layers. Substrate side. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: Additional layers. Substrate side. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['Additional_layers_substrate_side_thickness_list'] = ''

    #%% Additional layers. Substrate side. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['Additional_layers_substrate_side_deposition_procedure'] = cdf.depositionProcedure(userData['Additional layers. Substrate side. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Additional layers. Substrate side. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['Additional_layers_substrate_side_deposition_procedure'] = ''

    #%% Additional layers. Backcontact side. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...] 
    try:
        data['Additional_layers_backcontact_side_function'] = cdf.convertToString(userData['Additional layers. Backcontact side. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...]'])
    except: 
        print(f'Cound not read in: Additional layers. Backcontact side. Function [A.R.C./Upconversion/Down conversion/Back reflection/ ...] from: {fileName}')
        data['Additional_layers_backcontact_side_function'] = ''

    #%% Additional layers. Backcontact side. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]
    try:
        data['Additional_layers_backcontact_side_stack_sequence'] = cdf.stackSequence(userData['Additional layers. Backcontact side. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...]'])
    except: 
        print(f'Cound not read in: Additional layers. Backcontact side. Stack sequence [Mat.1; Mat.2; ... | Mat.3; ... | Mat.4 | ...] from: {fileName}')
        data['Additional_layers_backcontact_side_stack_sequence'] = ''

    #%% Additional layers. Backcontact side. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]
    try:
        data['Additional_layers_backcontact_side_thickness_list'] = cdf.thickness(userData['Additional layers. Backcontact side. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm]'], givenUnit = 'nm', desiredUnit = 'nm')
    except: 
        print(f'Cound not read in: Additional layers. Backcontact side. Thickness. List [Th.1 | Th.2 | … | Th.n ] [nm] from: {fileName}')
        data['Additional_layers_backcontact_side_thickness_list'] = ''

    #%% Additional layers. Backcontact side. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]
    try:
        data['Additional_layers_backcontact_side_deposition_procedure'] = cdf.depositionProcedure(userData['Additional layers. Backcontact side. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ]'])
    except: 
        print(f'Cound not read in: Additional layers. Backcontact side. Deposition. Procedure [Proc. 1 >> Proc. 2 >> ... | Proc. 3 >> … | Proc. 4 | ... ] from: {fileName}')
        data['Additional_layers_backcontact_side_deposition_procedure'] = ''
