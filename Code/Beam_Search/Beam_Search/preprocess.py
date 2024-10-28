# Define the attributes and descriptions
# 12-06-2024: Getest op mockset, werkt!


def define_attributes(skip_attributes=None, outcome_attribute=None):
    
    # Define the descriptives attributes
    num_atts = ['Leeftijd', 
                'ALAT', 'ASAT', 'Aniongap', 'Baseexcess', 'Basofielen',
               'Bicarbonaat', 'CK', 'CK-MB', 'CRP', 'Calciumionen',
               'Carboxyhemoglobine', 'Chloride', 'Eosinofielen', 'FIO2', 'Fibrinogeen',
               'Glucose', 'Glucose(arterieel)', 'Hematocriet', 'Hemoglobine', 'Kalium',
               'Kreatinine', 'Lactaat', 'Leucocyten', 'Lymfocyten', 'Methemoglobine',
               'Monocyten', 'Natrium', 'Neutrofielen', 'PCO2', 'PH', 'PO2', 'PT-INR',
               'Protrombinetijd', 'SO2', 'Standaardbicarbonaat', 'Temperatuur',
               'Trombocyten', 'Ureum', 'eGFR(CKD-EPI)', 'Euroscore-I', 'Euroscore-II',
               'ACETYLSALICYLZUUR_hosp', 'ADRENALINE_hosp', 'ALBUMINE_hosp',
               'ALFENTANIL_hosp', 'AMIODARON_hosp', 'AMLODIPINE_hosp',
               'ATORVASTATINE_hosp', 'BASIS VOOR SDD SUSPENSIE ASG_hosp',
               'CALCIUMGLUCONAAT_hosp', 'CARDIOPLEGIE_hosp', 'CEFAZOLINE_hosp',
               'CEFOTAXIM_hosp', 'CELLSAVER BLOED_hosp', 'CICLOPIROX_hosp',
               'CLEMASTINE_hosp', 'CLONIDINE_hosp',
               'COFACT INJPDR FLAC CA 250IE +SV 10ML+TOE_hosp', 'COROTROPE_hosp',
               'CUSTODIOL_hosp', 'DALTEPARINE_hosp', 'DEXAMETHASON_hosp',
               'DOBUTAMINE CF INFVLST CONC 12,5MG/ML AMP_hosp',
               'DURATEARS OOGDRUPPELS FLACON 15ML_hosp', 'EFEDRINE_hosp', 'ERYTR_hosp',
               'ERYTROMYCINE_hosp', 'ETOMIDAAT_hosp', 'FENOTEROL/IPRATROPIUM_hosp',
               'FENTANYL_hosp', 'FENYLEFRINE_hosp', 'FIBRINOGEEN_hosp',
               'FRESH FROZEN PLASMA_hosp', 'FUROSEMIDE_hosp', 'FUROSEMIDE CF_hosp',
               'GELATINE, GEMODIFICEERD_hosp', 'GLUCOSE_hosp', 'GRANISETRON_hosp',
               'HEPARINE_hosp', 'HYDROCHLOORTHIAZIDE_hosp', 'HYDROCORTISON_hosp',
               'ILOPROST_hosp', 'JOMEPROL_hosp', 'KALIUMCHLORIDE_hosp',
               'KALIUMCHLORIDE/MAGNESIUMCHLORIDE_hosp', 'LACTITOL_hosp',
               'LIDOCAINE_hosp', 'MAGNESIUMOXIDE_hosp', 'MAGNESIUMSULFAAT_hosp',
               'METAMIZOL_hosp', 'METOPROLOL_hosp', 'MIDAZOLAM_hosp',
               'MIDAZOLAM HAMELN INJ/INFVLST 5MG/ML AMPU_hosp', 'MORFINE_hosp',
               'MUPIROCINE_hosp', 'NATRIUMCHLORIDE_hosp', 'NATRIUMFOSFATEN_hosp',
               'NICARDIPINE_hosp', 'NITROGLYCERINE_hosp', 'NORADRENALINE_hosp',
               'NORADRENALINE CF INFVLST CONC 1MG/ML AMP_hosp', 'NORTRIPTYLINE_hosp',
               'NOVORAPID_hosp', 'NUTRISON ENERGY MULTI FIBRE CB_hosp',
               'NUTRISON PROTEIN PLUS MULTI FIBRE CB_hosp', 'OOGZALF_hosp',
               'OXAZEPAM_hosp', 'OXYBUTYNINE_hosp', 'PANTOPRAZOL_hosp',
               'PARACETAMOL_hosp', 'PIPERACILLINE/TAZOBACTAM_hosp', 'PROPOFOL_hosp',
               'PROTAMINE HCL_hosp', 'PROTAMINE SULFAAT_hosp', 'PROTROMBINECOMP_hosp',
               'RINGER/LACTAAT_hosp', 'ROCURONIUM_hosp', 'SALBUTAMOL/IPRATROPIUM_hosp',
               'SDD_hosp', 'SUFENTANIL_hosp', 'SUGAMMADEX_hosp', 'THIAMINE_hosp',
               'TRANEXAMINEZUUR_hosp', 'TROMB_hosp', 'VANCOMYCINE_hosp',
               'Bloed', 'Defecatie', 'Dialyse', 'Drains', 'Maag', 'Urine', 'Vocht']
    
    bin_atts = ['Geslacht', 'CHI0000104', 'CHI0000149', 'CTC0000027', 'CTC0000031', 'CTC0000036',
               'CTC0000046', 'CTC0000062', 'CTC0000077', 'CTC0000095', 'CTC0000130',
               'CTC0000162', 'CTC0000170', 'CTC0000175', 'CTC0000176', 'CTC0000208', 'CTC0000210', 
               'ACENOCOUMAROL', 'ACETYLSALICYLZUUR', 'ALLOPURINOL', 'AMIODARON',
               'AMLODIPINE', 'APIXABAN', 'ATORVASTATINE', 'BETAHISTINE', 'BISOPROLOL',
               'BUDESONIDE', 'BUMETANIDE', 'COLECALCIFEROL', 'DARBEPOETINE ALFA',
               'DESLORATADINE', 'DIGOXINE', 'EMPAGLIFLOZINE', 'EPLERENON',
               'FAMOTIDINE', 'FUROSEMIDE', 'ISOSORBIDEDINITRAAT', 'KETOCONAZOL',
               'KUNSTTRANEN EN ANDERE INDIFFERENTE PREPARATEN', 'LANREOTIDE',
               'LEVOTHYROXINE', 'LISINOPRIL', 'LORAZEPAM', 'LOSARTAN MET DIURETICA',
               'MACROGOL, COMBINATIEPREPARATEN', 'METOCLOPRAMIDE', 'METOPROLOL',
               'NITROGLYCERINE', 'NORTRIPTYLINE', 'OLOPATADINE', 'OXYCODON',
               'PANTOPRAZOL', 'PERINDOPRIL', 'RIVAROXABAN', 'ROSUVASTATINE',
               'SILDENAFIL', 'SITAGLIPTINE', 'TEMAZEPAM', 'TRIAMCINOLON',
               'VENLAFAXINE', 'ZOPICLON'] #, 'ABPs_high', 'ABPs_low', 'ABPm_high', 'ABPm_low', 'AF'] #type binary 
    
    nom_atts = [] #type category
    
    ord_atts = ['BMI_bins', 'ASA_Score', 'PriorityCode', 
                'Drugs', 'Alcohol', 'Smoking'] #type category
    
    # Define the remaining attributes
    id_attribute = ['PID']
    outcome_attribute = outcome_attribute #Either a HRV (SDSD, RMSSD, SDRR) or P-wave ()
    
    # Remove the skipped attributes
    skip_attributes_temp = []
    if not skip_attributes is None:
        for var in skip_attributes:
            skip_attributes_temp.append(var)
            if var in ord_atts:
                ord_atts.remove(var)
    skip_attributes = skip_attributes_temp
    
    descriptives = {'num_atts': num_atts, 'bin_atts': bin_atts, 'nom_atts': nom_atts, 'ord_atts': ord_atts}
    attributes = {'skip_attributes': skip_attributes, 'id_attribute': id_attribute, 'outcome_attribute': outcome_attribute}
    
    return attributes, descriptives

def define_dtypes(dataset=None, descriptives=None):
    
    for col in descriptives['ord_atts']:
        dataset[col] = dataset[col].astype('category')
    
    return dataset