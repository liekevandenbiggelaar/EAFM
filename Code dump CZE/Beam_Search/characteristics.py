import numpy as np

def BMI(length: list, weight: list):
    ll = np.array(length)
    ww = np.array(weight)
    
    return list( ww/np.square(ll/100) )
    
def BMI_bins(bmi: list):
    """
    Underweight   (UW) : [ :18.5)
    Health Weight (HW) : [18.5: 25)
    Overweight    (OW) : [25: 30)
    Obese         (OB) : [30: 35)
    Extreme Obese (EB) : [35: 40)
    Morbid Obese  (MB) : [40: ]
    """
    
    bins = [0, 18.5, 25, 30, 35, 40, np.inf]
    names = ['0. UW', '1. HW', '2. OW', '3. OB', '4. EB', '5. MB']

    d = dict(enumerate(names, 1))

    return np.vectorize(d.get)(np.digitize(bmi, bins))
