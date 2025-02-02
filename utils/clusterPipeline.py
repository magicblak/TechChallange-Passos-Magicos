import pandas as pd
import numpy as np
from datetime import datetime
import re
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin

indicators_columns = [
    
]

class FeatureEngineeringToCluster(BaseEstimator, TransformerMixin):
    def __init__(self, indicators_features = ['inde', 'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian'], features_to_ajust = ['ra', 'ano_nasc', 'genero', 'instituicao_ensino', 'fase', 'defasagem', 'ano_ref']):
       self.indicators_features = indicators_features
       self.features_to_ajust = features_to_ajust
    
    def fit(self, df):
        return self
    
    def __ajust_gender_female(self, gender):
        if(gender == 'Menina' or gender == 'Feminino'): return 1
        return 0
    
    def __ajust_gender_male(self, gender):
        if(gender == 'Menino' or gender == 'Masculino'): return 1
        return 0
    
    def __ajust_phase(self, phase):
        if(phase == 'ALFA'): return 0
        elif(phase == '9'): return 8
        return "".join(re.findall(r"\d+", str(phase)))
    
    def __ajust_public_school(self, shool):
        if(shool == 'Escola Pública' or shool == 'Pública'): return 1
        return 0
    
    def __ajust_public_private(self, shool):
        if(shool != 'Escola Pública' and shool != 'Pública'): return 1
        return 0
    
    def __get_age_from_year(self, year):
        year = int(str(year)[-4:])
        age = datetime.now().year - year
        return age
    
    def transform(self, df):
        df = df[self.features_to_ajust + self.indicators_features]
        df.head()
        df['id'] = df.apply(lambda row: f"{row['ano_ref']}{row['ra']}", axis=1)
        print(df.columns)
        df['female'] = pd.to_numeric(df['genero'].apply(self.__ajust_gender_female))
        df['male'] = pd.to_numeric(df['genero'].apply(self.__ajust_gender_male))
        df['phase'] = pd.to_numeric(df['fase'].apply(self.__ajust_phase))
        df['public_school'] = pd.to_numeric(df['instituicao_ensino'].apply(self.__ajust_public_school))
        df['private_school'] = pd.to_numeric(df['instituicao_ensino'].apply(self.__ajust_public_private))
        df['age'] = pd.to_numeric(df['ano_nasc'].apply(self.__get_age_from_year))
        df.drop(columns=['genero', 'fase', 'instituicao_ensino'], inplace=True)
        df[self.indicators_features] = (
            df[self.indicators_features]
            .astype(str)
            .replace(",", '.', regex=True)
            .apply(pd.to_numeric, errors='coerce')
        )
        return df

class FeatureSelectionToCluster(BaseEstimator, TransformerMixin):
    def __init__(self, feature_to_remove=['female', 'male', 'public_school', 'private_school', 'ano_nasc', 'ano_ref'], phase_to_filter=-1):
        self.feature_to_remove = feature_to_remove
        self.phase_to_filter = phase_to_filter
    
    def fit(self, df):
        return self
    
    def transform(self, df):
        df = df[df['ano_ref'] > 2022]#removendo 2022 pela falta do ipp
        if(self.phase_to_filter > -1): df = df[df['phase'] == self.phase_to_filter]
        df.drop(columns=self.feature_to_remove, inplace=True)
        return df

class MinMaxScaleFeatureToCluster(BaseEstimator, TransformerMixin):
    def __init__(self, feature_to_scale=['iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian']):
        self.feature_to_scale = feature_to_scale
    
    def fit(self, df):
        return self
    
    def transform(self, df):
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled_data = scaler.fit_transform(df[self.feature_to_scale])
        df_scaled = pd.DataFrame(scaled_data, columns=self.feature_to_scale)
        df.reset_index(inplace=True, drop=True)
        df_scaled.reset_index(inplace=True, drop=True)
        df_scaled['id'] = df['id']
        return df_scaled

class DimensionalityReductionFeatureToCluster(BaseEstimator, TransformerMixin):
    def __init__(self, feature_to_dimension=['iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian']):
        self.feature_to_dimension = feature_to_dimension
    
    def fit(self, df):
        return self
    
    def transform(self, df):
        pca = PCA(n_components=2)
        df = df[['id'] + self.feature_to_dimension]
        df.dropna(inplace=True)
        dimensioned_data = pca.fit_transform(df[self.feature_to_dimension])
        return df, dimensioned_data