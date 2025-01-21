import numpy as np
import pandas as pd

def other_relations(result: int, results_dataset, patients_dataset, quality_dataset, af_dataset):
    """ 
    Code to check the relevance of all characteristics. 
    e.g. is x AND y AND z necessary or is x AND y also insightful? 
    """
    
    relations_dataset = pd.DataFrame()
    attributes, descriptives = define_attributes()
    
    row = results_dataset.iloc[result]
    desc = eval(row['Description'])['description']
    theta = row['Theta']
    
    items = desc.items()

    temp = []
    # Get all items and its indexes
    for item in items:
        key = item[0]
        value = item[1]
        
        data_subgroup, ids = select_subgroup(description=[key, value], df=patients_dataset, descriptives=descriptives)
        temp.append((str(key)+" "+str(value), ids))

    coms = [] + temp
    # Go over all combinations
    for i in range(len(temp)):
        for j in range(i, len(temp)):
            if i == j:
                continue
            
            d1 = temp[i][0]
            d2 = temp[j][0]
            
            i1 = set(temp[i][1])
            i2 = set(temp[j][1])
            i12 = i1 & i2
            
            d12 = d1 + " AND " + d2

            coms.append((d12, i12))
    
    # Get the one for the entire description
    d_all = ''
    i_all = set()
    for m in range(len(temp)):
        dm = temp[m][0]
        im = set(temp[m][1])
        if m == 0:
            d_all = dm
            i_all = im
        else:
            d_all += " AND " + dm
            i_all = i_all & im
    
    coms.append((d_all, i_all))
        
    
    relations_dataset['Description'] = [c[0] for c in coms]
    relations_dataset['Indexes'] = [c[1] for c in coms]
    
    # get average AF and phenotype difference
    af_lst = []
    qm_diff = []
    qm_perc = []
    
    for k in range(len(relations_dataset)):
        pats = list(relations_dataset.iloc[k]['Indexes'])
        pids = list(patients_dataset.iloc[pats]['PID'])
        
        compls = af_dataset[af_dataset['PID'].isin(pids)]
        nr_af = len(compls)
        af_perc = round(nr_af / len(pats) * 100, 2)
        
        af_lst.append(af_perc)
        
        qms = quality_dataset[quality_dataset['PID'].isin(pids)]
        theta_avg_group = round( np.mean(qms[theta]), 2)
        theta_avg_all = round( np.mean(quality_dataset[theta]), 2)
        theta_diff = round(theta_avg_group - theta_avg_all, 2)
        theta_diff_perc = round(theta_avg_group / theta_avg_all, 2)
        
        qm_diff.append(theta_diff)
        qm_perc.append(theta_diff_perc)
    
    relations_dataset['AF'] = af_lst
    relations_dataset['Pheno Diff'] = qm_diff
    relations_dataset['Pheno Diff %'] = qm_perc
    
    # get phenotype difference
    

     
    return relations_dataset

def select_subgroup(description=None, df=None, descriptives=None):

    num_atts = descriptives['num_atts']
    bin_atts = descriptives['bin_atts']
    nom_atts = descriptives['nom_atts']
    ord_atts = descriptives['ord_atts']

    # select all indices as a starting point
    idx = df.index.values

    att = description[0]
    sel = description[1]

    if att in bin_atts:
            
        idx = select_bin_att(idx=idx, att=att, sel=sel, df=df)
        
    elif att in num_atts:

        idx = select_num_att(idx=idx, att=att, sel=sel, df=df)

    elif att in nom_atts:

        idx = select_nom_att(idx=idx, att=att, sel=sel, df=df)

    elif att in ord_atts:

        idx = select_ord_att(idx=idx, att=att, sel=sel, df=df)

    all_idx = df.index.values
    subgroup = df.loc[idx]

    return subgroup, list(idx)

def select_bin_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
    else:
        sel_idx = df[df[att] == sel[0]].index.values

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_num_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
    else:
        low_idx =  df[df[att] >= sel[0]].index.values # value can be equal to the lower bound
        up_idx = df[df[att] <= sel[1]].index.values # value can be equal to the upper bound            
        sel_idx = np.intersect1d(low_idx, up_idx)
    
    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_nom_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()
    tup = sel

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)
  
    # when the first value is a 1, then take all datapoints with the value in position two
    if tup[0] == 1.0:
        df_drop = df[df[att].notnull()]
        sel_idx = df_drop[df_drop[att] == tup[1]].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)
        
    # when the first value is a 0, then take all datapoints that do not have the value in position two
    elif tup[0] == 0.0:
        df_drop = df[df[att].notnull()]
        sel_idx = df_drop[df_drop[att] != tup[1]].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)

    idx_out = idx_in.copy()

    return idx_out    

def select_ord_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()        

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
    else:
        # a loop over all categories in the description
        # cases that equal either of the categories should be selected
        sel_idx = df[df[att].isin(sel)].index.values

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def define_attributes(skip_attributes=None, outcome_attribute=None):
    
    # Define the descriptives attributes
    num_atts = ['Leeftijd', 
                
 'ALAT', 'APTT','APTT(heparinase)','APTT(heparinase)Ckprest','APTTCkprest',
 'ASAT','Aniongap','Baseexcess',
 'Basofielen','Bicarbonaat','BilirubineTotaal','CK',
 'CK-MB','CRP','Calciumionen','Carboxyhemoglobine',
 'Chloride','Cholesterol','Eosinofielen','FIO2','Fibrinogeen','Glucose','Glucose(arterieel)','Hematocriet',
 'Hemoglobine','Kalium','Kreatinine','Lactaat',
 'Leucocyten','Lymfocyten','Methemoglobine',
 'Monocyten','Natrium','Neutrofielen','PCO2','PH',
 'PO2','PT-INR','Protrombinetijd','SO2','Standaardbicarbonaat','Triglyceriden','Trombocyten','Ureum',
 'aniongapveneus','eGFR(CKD-EPI)','Euroscore-I','Euroscore-II',

                
'ALBUMINE_hosp','ALFENTANIL_hosp','AMIODARON_hosp',
 'CALCIUMGLUCONAAT_hosp','CARDIOPLEGIE_hosp',
 'CEFAZOLINE_hosp','CEFOTAXIM_hosp','CELLSAVER BLOED_hosp',
 'CLONIDINE_hosp','COROTROPE_hosp','CUSTODIOL_hosp',
 'DEXAMETHASON_hosp','DOBUTAMINE CF INFVLST CONC 12,5MG/ML AMP_hosp','EFEDRINE_hosp','ERYTR_hosp',
 'ERYTROMYCINE_hosp','ETOMIDAAT_hosp','FENTANYL_hosp','FENYLEFRINE_hosp',
 'FIBRINOGEEN_hosp','FRESH FROZEN PLASMA_hosp','FUROSEMIDE_hosp','FUROSEMIDE CF_hosp','GELATINE, GEMODIFICEERD_hosp',
 'GLUCOSE_hosp','GRANISETRON_hosp','HEPARINE_hosp','HYDROCORTISON_hosp',
 'JOMEPROL_hosp','KALIUMCHLORIDE_hosp','KALIUMCHLORIDE/MAGNESIUMCHLORIDE_hosp',
 'MAGNESIUMSULFAAT_hosp','MIDAZOLAM_hosp',
 'MIDAZOLAM HAMELN INJ/INFVLST 5MG/ML AMPU_hosp','MORFINE_hosp','NATRIUMCHLORIDE_hosp',
 'NITROGLYCERINE_hosp','NORADRENALINE_hosp','NORADRENALINE CF INFVLST CONC 1MG/ML AMP_hosp',
 'NOVORAPID_hosp','NUTRISON ENERGY MULTI FIBRE CB_hosp','NUTRISON PROTEIN PLUS MULTI FIBRE CB_hosp',
 'PANTOPRAZOL_hosp','PIPERACILLINE/TAZOBACTAM_hosp','PROPOFOL_hosp',
 'PROTAMINE HCL_hosp','RINGER/LACTAAT_hosp','ROCURONIUM_hosp',
 'SUFENTANIL_hosp','THIAMINE_hosp',
 'TRANEXAMINEZUUR_hosp','TROMB_hosp','VANCOMYCINE_hosp',
                
 'Bloed','Defecatie', 'Dialyse','Drains','Maag',
 'Urine','Vocht'
]
    # 'ALAT'
    #'ADRENALINE_hosp','CLEMASTINE_hosp','LIDOCAINE_hosp', 'NICARDIPINE_hosp' ,'PARACETAMOL_hosp' ,'SUGAMMADEX_hosp','PROTROMBINECOMP_hosp', 'ACETYLSALICYLZUUR_hosp', 'AMLODIPINE_hosp', 'ATORVASTATINE_hosp', 'BASIS VOOR SDD SUSPENSIE ASG_hosp','CICLOPIROX_hosp','CLEMASTINE_hosp','COFACT INJPDR FLAC CA 250IE +SV 10ML+TOE_hosp','DALTEPARINE_hosp','DURATEARS OOGDRUPPELS FLACON 15ML_hosp','FENOTEROL/IPRATROPIUM_hosp','HYDROCHLOORTHIAZIDE_hosp','ILOPROST_hosp','LACTITOL_hosp', 'MAGNESIUMOXIDE_hosp', 'METOPROLOL_hosp', 'MUPIROCINE_hosp', 'NATRIUMFOSFATEN_hosp', 'NORTRIPTYLINE_hosp','OOGZALF_hosp','OXAZEPAM_hosp','OXYBUTYNINE_hosp','PROTAMINE SULFAAT_hosp','PROTROMBINECOMP_hosp','SALBUTAMOL/IPRATROPIUM_hosp','SDD_hosp'
    #'Spoelvocht',
    
    bin_atts = ['Geslacht', 'CAR0000010',
 'CHI0000280','CHI0000960','CTC0000027','CTC0000031','CTC0000036','CTC0000037','CTC0000038','CTC0000046','CTC0000056','CTC0000062','CTC0000067','CTC0000068',
 'CTC0000078','CTC0000082','CTC0000095','CTC0000103',
 'CTC0000130','CTC0000162',
 'CTC0000170','CTC0000174','CTC0000175','CTC0000176','CTC0000206',
 'CTC0000208','ECC0000001','NCH0000016','OKART00044',

 'ACENOCOUMAROL','ACETYLSALICYLZUUR','AMLODIPINE',
 'APIXABAN','ATORVASTATINE','BISOPROLOL','BUDESONIDE',
 'BUMETANIDE','COLECALCIFEROL','DESLORATADINE','DIGOXINE','KUNSTTRANEN EN ANDERE INDIFFERENTE PREPARATEN',
 'EMPAGLIFLOZINE','EPLERENON','FAMOTIDINE','FUROSEMIDE','ISOSORBIDEDINITRAAT','LEVOTHYROXINE','LISINOPRIL',
 'LORAZEPAM','LOSARTAN MET DIURETICA','MACROGOL, COMBINATIEPREPARATEN','METOPROLOL',
 'NITROGLYCERINE','NORTRIPTYLINE','OLOPATADINE','PANTOPRAZOL',
 'PERINDOPRIL','RIVAROXABAN','ROSUVASTATINE',
 'TEMAZEPAM','TRIAMCINOLON','ZOPICLON',
] #, 'ABPs_high', 'ABPs_low', 'ABPm_high', 'ABPm_low', 'AF'] #type binary 
    # 'CTC0000035','CTC0000055', 'CTC0000064','CTC0000066','CTC0000077','CTC0000101','CTC0000104', 'CTC0000110','CTC0000163','CTC0000169','CTC0000210', 'CAR0000111', 'CHI0000059', 'CHI0000102', 'CHI0000104', 'CTC0000007', 'CTC0000047', 'CTC0000048', 'CTC0000205', 'GYN0000005', 'CTC0000052'
    # ,'ALLOPURINOL','AMIODARON',  'KETOCONAZOL','LANREOTIDE','METOCLOPRAMIDE','OXYCODON','VENLAFAXINE', 'BETAHISTINE', 'SILDENAFIL', 'SITAGLIPTINE', 'VENLAFAXINE'

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