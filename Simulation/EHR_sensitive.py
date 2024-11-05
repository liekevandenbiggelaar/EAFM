# Generating Electronic Health Records (EHR) to accompany the signals.
# This EHR is used as the descriptors of the EMM Framework.
import random
import pandas as pd

def generate_EHR(dataset = 'CPSC'):
    """
    Generating fictional Electronic Health Records for patients. The values are created biased towards the real world as informed by domain experts.
    This includes binary, numerical, and nominal features: 
        gender (binary), age (numerical), BMI (ordinal), health scores (ordinal), fluid losses (numerical), habits (ordinal), and medication at home (binary).

    Input:
    * dataset (str): the dataset that will be used. Used to find the sample size.

    """
    random.seed(2)

    dct_samplesizes = {'MITBIH': 25, 'CPSC': 105, 'SHDB-AF': 100}
    size = dct_samplesizes[dataset]

    dct_EHR = {}

    # age is skewed towards the age that most AF occurs (from 50)
    age = [random.randint(50, 80) for i in range(size)]
    dct_EHR['a1'] = age

    # gender is little skewed towards males
    gender = random.choices(['Male', 'Female'], [70, 30], k=size)
    dct_EHR['a2'] = gender

    # skewed towards normal weight
    BMI = random.choices(['UW', 'HW', 'OW', 'OB', 'EB', 'MB'], [10, 35, 30, 8, 5, 2], k=size)
    dct_EHR['a3'] = BMI


    # Generate health scores
    #EuroI = 
    #EuroII =
    ASA = random.choices(['1', '2', '3', '4', '5', '6'], k=size)
    dct_EHR['a4'] = ASA

    # Habits
    habits = ['a5', 'a6', 'a7']
    for hab in habits:
        use = random.choices(['0. None', '1. Used', '2. Uses'], k=size)
        dct_EHR[hab] = use

    # Fluid losses
    fluids = ['a8', 'a9', ' a10', ' a11', 'a12', 'a13', 'a14']
    for fl in fluids:
        loss = random.choices([0, random.randint(0, 2500)], [60, 40], k=size) #assume less loss is more common
        dct_EHR[fl] = loss

    lst_homemeds = ['a15', 'a16', 'a17', 'a18', 'a19', 'a20', 'a21', 'a22',
               'a23', 'a24', 'a25', 'a26', 'a27', 'a28', 'a29', 'a30',
               'a31', 'a32', 'a33', 'a34', 'a35', 'a36', 'a37', 'a38', 'a39', 'a40',
               'a41', 'a42', 'a43', 'a44', 'a45', 'a46', 'a47',
               'a48', 'a49', 'a50', 'a51', 'a52', 'a53', 'a54', 'a55', 'a56', 'a57']
    
    for homemed in lst_homemeds:
        binsmed = random.choices(['Not Taken', 'Taken'], [80, 20], k=size) #assume more do not take a medicine than the ones that do
        dct_EHR[homemed] = binsmed


    df_EHR = pd.DataFrame.from_dict(dct_EHR)
    
    return df_EHR

