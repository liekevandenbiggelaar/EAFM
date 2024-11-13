# Define the attributes and descriptions
# 12-06-2024: Getest op mockset, werkt!


def define_attributes(skip_attributes=None, outcome_attribute=None):
    
    # Define the descriptives attributes
    num_atts = ['a1', 'a8', 'a9', 'a10', 'a11', 'a12', 'a13', 'a14']
    
    bin_atts = ['a2', 'a15', 'a16', 'a17', 'a18', 'a19', 'a20', 'a21', 
                'a22', 'a23', 'a24', 'a25', 'a26', 'a27', 'a28', 'a29', 
                'a30', 'a31', 'a32', 'a33', 'a34', 'a35', 'a36', 'a37', 
                'a38', 'a39', 'a40', 'a41', 'a42', 'a43', 'a44', 'a45', 
                'a46', 'a47', 'a48', 'a49', 'a50', 'a51', 'a52', 'a53', 
                'a54', 'a55', 'a56', 'a57']

    
    nom_atts = [] #type category
    
    ord_atts = ['a3', 'a4', 'a5', 'a6', 'a7'] #type category
    
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