def multiselectShortAlternatives():
    '''Returns a dictionary with the most common alternatives for  the key multiselects'''
    alternatives = {
        'Backcontact_stack_sequence' : ['All',
            'none',
            'Ag', 
            'Ag-nw', 
            'AgAl', 
            'Al', 
            'Au', 
            'Ca | Al', 
            'Carbon', 
            'Carbon-nt', 
            'Cu', 
            'ITO', 
            'MoO3 | Ag', 
            'MoO3 | Al', 
            'MoO3 | Au', 
            'MoOx | Ag', 
            'MoOx | Al', 
            'PEDOT:PSS', 
            'Pt | FTO',],
        
    'Cell_architecture' : ['All', 
        'nip', 
        'pin', 
        'Back contacted', 
        'Front contacted', 
        'Schottky',],
                         
    'ETL_stack_sequence' : ['All',
        'none',
        'C60', 
        'C60 | BCP', 
        'PCBM-60', 
        'PCBM-60 | BCP', 
        'PCBM-60 | Bphen', 
        'PCBM-60 | C60 | BCP', 
        'PCBM-60 | LiF', 
        'PCBM-60 | ZnO-np', 
        'SnO2-c', 
        'SnO2-np', 
        'TiO2-c', 
        'TiO2-c | PCBM-60', 
        'TiO2-c | TiO2-mp', 
        'TiO2-c | TiO2-mp | Al2O3-mp', 
        'TiO2-c | TiO2-mp | ZrO2-mp', 
        'TiO2-c | TiO2-nw', 
        'TiO2-np', 
        'ZnO-c', 
        'ZnO-np',],
    
    'HTL_stack_sequence' : ['All',
        'none',
        'CuSCN', 
        'NiO-c', 
        'NiO-np', 
        'P3HT', 
        'PEDOT:PSS', 
        'PTAA', 
        'Spiro-MeOTAD',],
  
    'Perovskite_additives_compounds' : ['All',
        'Undoped', 
        '5-AVAI', 
        'Acetate', 
        'Acetate; Cl', 
        'Cl', 
        'H2O', 
        'HCl', 
        'HI', 
        'HPA', 
        'K', 
        'KI', 
        'NH4Cl', 
        'NH4SCN', 
        'PEAI', 
        'Pb(SCN)2', 
        'Pb(SCN)2; SnF2', 
        'Rb', 
        'RbI', 
        'SnF2',                                     
        'Urea',],
 
    'Perovskite_composition_short_form' : [ 'All',
        'CsFAMAPbBrI', 
        'CsFAPbBrI',
        'CsPbBr',
        'CsPbBrI',
        'CsPbI',
        'FAMAPbBrI', 
        'FAMAPbI', 
        'FAPbI', 
        'MAPbBrI', 
        'MAPbI',],                     
    
    'Perovskite_deposition_procedure' : ['All',
        'Co-evaporation', 
        'Doctor blading', 
        'Drop-infiltration', 
        'Drop-infiltration >> CBD', 
        'Evaporation >> CBD', 
        'Evaporation >> Evaporation', 
        'Evaporation >> Gas reaction', 
        'Evaporation >> Spin-coating', 
        'Inkjet printing', 
        'Slot-die coating', 
        'Spin-coating', 
        'Spin-coating >> CBD', 
        'Spin-coating >> Gas reaction', 
        'Spin-coating >> Recrystallization', 
        'Spin-coating >> Spin-coating', 
        'Spin-coating >> Spin-coating >> Spin-coating', 
        'Spin-coating >> Spray-coating', 
        'Spray-coating', 
        'Ultrasonic spray',],

    'Substrate_stack_sequence' : ['All',
        'PEN | ITO', 
        'PET', 
        'PET | Ag-grid', 
        'PET | ITO', 
        'PET | IZO', 
        'SLG', 
        'SLG | AZO', 
        'SLG | FTO', 
        'SLG | ITO',],
    }

    return alternatives