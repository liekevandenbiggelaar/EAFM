import pandas as pd

def create_metadata_table(features: dict, pid: str, wid: str):
    
    metadata = pd.DataFrame.from_dict(features)
    """
    print(pid, wid)
    metadata['PID'] = [pid]
    metadata['WID'] = [wid]
    
    # R Peak
    metadata['R-location'] = [features['R-location']]
    metadata['RR-interval'] = [features['RR-interval']]
    
    # QRS Complex
    metadata['Q-location'] = [features['Q-location']]
    metadata['S-location'] = [features['S-location']]
    metadata['QRS-duration'] = [features['QRS-duration']]
    """
    
    return metadata

def add_metadata_table(tables: list):
    return pd.concat(tables)


    
    
    
    