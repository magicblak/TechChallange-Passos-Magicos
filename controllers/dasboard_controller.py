import pandas as pd
import numpy as np
from utils.clusterPipeline import FeatureEngineeringToCluster, FeatureSelectionToCluster, MinMaxScaleFeatureToCluster, DimensionalityReductionFeatureToCluster
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from models.data_access import DataAccess

class Data_treatment_controller:
    def __init__(self):
        return
    
    def get_treated_data(self):
        reader = DataAccess()
        df = reader.get_pm_db()
        
        def process_pipeline_to_use(df):
            pipeline = Pipeline([
                ('feature_engineer', FeatureEngineeringToCluster())
            ])
            df_pipeline = pipeline.fit_transform(df)
            return df_pipeline
        
        return process_pipeline_to_use(df)


class Cluster_controller:
    def __init__(self):
        pass
    
    __cluster_features = [
        'inde', 
        'iaa',
        'ieg',
        'ips',
        'ipp', #sem dados para 2022
        'ida',
        'ipv',
        'ian'
    ]

    def to_excel(self, df): #algum expoort de excel???
        #output = io.BytesIO()
        #with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        #    df.to_excel(writer, index=False, sheet_name='Sheet1')
        #processed_data = output.getvalue()
        #return processed_data
        return
    
    def clustering(self):
        reader = DataAccess()
        df = reader.get_pm_db()

        def process_pipeline_to_cluster(df):
            pipeline = Pipeline([
                ('feature_engineer', FeatureEngineeringToCluster()),
                ('feature_selection', FeatureSelectionToCluster(phase_to_filter=1)),
                ('min_max_scale', MinMaxScaleFeatureToCluster()),
                ('dimensional_reduction', DimensionalityReductionFeatureToCluster()),
            ])
            df_pipeline, dimensioned_data = pipeline.fit_transform(df)
            return df_pipeline, dimensioned_data
    
        def verify_K(df):
            K = range(2, 5)
            elbow = []
            silhouette = []
            
            for k in K:
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(df)
                elbow.append(kmeans.inertia_)
                sil_score = silhouette_score(df, kmeans.labels_)
                silhouette.append(sil_score)
            #identificando elbow e silhouette de forma automatizada
            wss_diff = np.diff(elbow)
            wss_diff2 = np.diff(wss_diff)
            elbow = np.argmax(-wss_diff2) + 2
            print(max(silhouette))
            silhouette = silhouette.index(max(silhouette)) + 2
            return elbow, silhouette
        
        df, dimensioned_data = process_pipeline_to_cluster(df)
        elbow, silhouette = verify_K(dimensioned_data)        
        optimal_k = silhouette
        kmeans_final = KMeans(n_clusters=optimal_k, random_state=42)
        labels = kmeans_final.fit_predict(dimensioned_data)
        df_dimensioned_clustered = dimensioned_data
        df['cluster'] = labels
        return df, df_dimensioned_clustered