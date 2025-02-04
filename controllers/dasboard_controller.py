import pandas as pd
import numpy as np
from utils.pipelines import FeatureEngineering, FeatureSelectionToCluster, MinMaxScaleFeatureToCluster, DimensionalityReductionFeatureToCluster
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from models.data_access import DataAccess

class Data_treatment_controller:
    def __init__(self):
        return
        
    def __process_pipeline_to_use(self, df):
        pipeline = Pipeline([
            ('feature_engineer', FeatureEngineering())
        ])
        df_pipeline = pipeline.fit_transform(df)
        return df_pipeline
    
    def get_raw_data(self):
        reader = DataAccess()
        df = reader.get_pm_db()
        
        return self.__process_pipeline_to_use(df)
    
    def get_compare_indidividual_indicator_with_mean(self, student_row_id):
        data = self.get_raw_data()
        indicators_columns = [ 'inde', 'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian' ]
        student_info = data[data['id'] == student_row_id][indicators_columns].T
        student_info.reset_index(inplace=True)
        student_info.columns = ['indicators', 'values']
        student_info['type'] = 'Estudante'
        phase_mean = round(data[data['phase'] == data[data['id'] == student_row_id].phase.values[0]][indicators_columns].mean(), 2).reset_index()
        phase_mean.columns = ['indicators', 'values']
        phase_mean['type'] = 'Média da fase'
        return pd.concat([phase_mean, student_info])
    
    def get_historycal_inde(self, student_row_id):
        data = self.get_raw_data()
        student_ra = data[data['id'] == student_row_id].ra.values[0]
        inde_historic = data[data['ra'] == student_ra][['ano_ref', 'inde']]
        return inde_historic.round(2)
    
    def get_grades_history(self, student_row_id):
        data = self.get_raw_data()
        student_ra = data[data['id'] == student_row_id].ra.values[0]
        grade_historic = data[data['ra'] == student_ra][['ano_ref', 'phase', 'mat', 'por', 'ing']]
        grade_historic[['mat', 'por', 'ing']] = grade_historic[['mat', 'por', 'ing']].round(2).fillna('-')
        grade_historic['ano_ref'] = grade_historic['ano_ref'].astype(str)
        grade_historic['phase'] = grade_historic['phase'].astype(str)
        grade_historic.sort_values(by='ano_ref', ascending=False, inplace=True)
        grade_historic.rename(columns={
            'mat': 'Matemática',
            'por':'Português',
            'ing': 'Inglês',
            'ano_ref': 'Ano',
            'phase': 'Fase'
        }, inplace=True)
        grade_historic.reset_index(inplace=True, drop=True)
        return grade_historic
    
    def get_student_growing(self, student_row_id):
        #Cálculo estatístico para entender se houve melhora (BASE DE NOTAS? INDE - PEDRAS?) desde a entrada na PM (desvio padrão?)
        #USAR AS PEDRAS NOS VALORES DE INDICADORES
        return
    
    def get_student_percentile(self, student_row_id):
        #Cálculo estatístico para entender como se classifica o estudante em comparação aos demais, usar o INDE
        #USAR AS PEDRAS NOS VALORES DE INDICADORES
        #É ISSO E PARTIR PRA IA
        return
    

    
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
    
    def get_filtered_data_to_cluster_by_student(self, df, selected_student, student_phase):
        max_year = df['ano_ref'].max()
        df_same_phase = df.query("(phase == @student_phase and ano_ref < @max_year and ano_ref > 2022) or (nome == @selected_student and ano_ref == @max_year)")
        df_next_phase = df[df['ra'].isin(df_same_phase['ra']) & (df['phase'] == (student_phase + 1))]
        return df_same_phase, df_next_phase
    
    def clustering(self, df):

        def process_pipeline_to_cluster(df):
            pipeline = Pipeline([
                ('feature_selection', FeatureSelectionToCluster()),
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