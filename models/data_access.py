import pandas as pd

class DataAccess:
    def __init__(self):
        pass

    def get_pm_db(self):
        return pd.read_csv('data/base_pm_consolidada.csv')
    
    def get_orig(self):
        return pd.read_csv('data/base_2024_original.csv')