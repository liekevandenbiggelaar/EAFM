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
    sample = dct_samplesizes[dataset]

    dct_EHR = {}

    # age is skewed towards the age that most AF occurs (from 50)
    age = [random.randint(50, 80) for i in range(sample)]
    dct_EHR['Age'] = age

    # gender is little skewed towards males
    gender = random.choices(['Male', 'Female'], [70, 30], k=sample)
    dct_EHR['Gender'] = gender

    # skewed towards normal weight
    BMI = random.choices(['UW', 'HW', 'OW', 'OB', 'EB', 'MB'], [10, 35, 30, 8, 5, 2], k=sample)
    dct_EHR['BMI'] = BMI


    # Generate health scores
    #EuroI = 
    #EuroII =
    ASA = random.choices([1, 2, 3, 4, 5, 6], k=sample)
    dct_EHR['ASA'] = ASA

    # Habits
    drugs =   random.choices(['0. None', '1. Used', '2. Uses'], k=sample)
    alcohol = random.choices(['0. None', '1. Used', '2. Uses'], k=sample)
    smoking = random.choices(['0. None', '1. Used', '2. Uses'], k=sample)
    dct_EHR['Drugs'], dct_EHR['Alcohol'], dct_EHR['Smoking'] = drugs, alcohol, smoking

    # Fluid losses
    blood = [random.randint(0, 1000) for i in range(sample)]
    urine = [random.randint(0, 1000) for i in range(sample)]
    fluid = [random.randint(0, 1000) for i in range(sample)]
    dct_EHR['Blood loss'], dct_EHR['Urine loss'], dct_EHR['General Fluid Loss'] = blood, urine, fluid


    df_EHR = pd.DataFrame.from_dict(dct_EHR)
    
    return df_EHR

