import pandas as pd

def create_metadata_table(features: dict, pid: str, wid: str):
    
    metadata = pd.DataFrame.from_dict(features)
    
    return metadata

def add_metadata_table(tables: list):
    return pd.concat(tables)


    
    
    
    