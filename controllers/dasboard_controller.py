import pandas as pd
import numpy as np
from utils.pipelines import FeatureEngineering, FeatureSelectionToCluster, MinMaxScaleFeatureToCluster, DimensionalityReductionFeatureToCluster
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LinearRegression
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
        return round(pd.concat([phase_mean, student_info]), 2)
    
    def get_historycal_indicators(self, student_row_id):
        indicators_columns = [ 'inde', 'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian' ]
        data = self.get_raw_data()
        student_ra = data[data['id'] == student_row_id].ra.values[0]
        inde_historic = data[data['ra'] == student_ra][['ano_ref'] + indicators_columns]
        return inde_historic.round(2)
    
    def get_grades_history(self, student_row_id):
        def ajust_discipline(discipline):
            if(discipline == 'mat'): return 'Matemática'
            elif(discipline == 'por'): return 'Português'
            elif(discipline == 'ing'): return 'Inglês'
        data = self.get_raw_data()
        student_ra = data[data['id'] == student_row_id].ra.values[0]
        grade_historic = data[data['ra'] == student_ra][['ano_ref', 'phase', 'mat', 'por', 'ing']]
        grade_historic[['mat', 'por', 'ing']] = grade_historic[['mat', 'por', 'ing']].round(2)
        grade_historic['ano_ref'] = grade_historic['ano_ref'].astype(str)
        grade_historic['phase'] = grade_historic['phase'].astype(str)
        grade_historic.sort_values(by='ano_ref', ascending=True, inplace=True)
        grade_historic = grade_historic.melt(id_vars=['ano_ref', 'phase'], value_vars=['mat', 'por', 'ing'], value_name='grade', var_name='disicpline')
        grade_historic.rename(columns={
            'ano_ref': 'Ano',
            'phase': 'Fase'
        }, inplace=True)
        grade_historic['grade'] = pd.to_numeric(grade_historic['grade'])
        grade_historic['disicpline'] = grade_historic['disicpline'].apply(ajust_discipline)
        grade_historic.reset_index(inplace=True, drop=True)
        return round(grade_historic, 2)
    
    def get_student_growing(self, student_row_id):
        indicators_columns = [ 'inde', 'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian' ]
        variation = []
        indicators_historic = self.get_historycal_indicators(student_row_id).fillna(0)
        for indicador in indicators_columns:
            X = np.array(indicators_historic['ano_ref']).reshape(-1, 1)
            y = indicators_historic[indicador].values
            modelo = LinearRegression().fit(X, y)
            variation.append({'Indicador': indicador, 'Inclinação': modelo.coef_[0]})
        return round(pd.DataFrame(variation), 2)
    
def get_student_percentile(self, student_row_id):
    data = self.get_raw_data()
    student_phase = data.loc[data['id'] == student_row_id, 'phase'].values[0]
    data = data[data['phase'] == student_phase]
    data['inde'] = pd.to_numeric(data['inde'], errors='coerce').fillna(0)
    unique_values = len(data['inde'].unique())
    if unique_values >= 100:
        q = 100
    elif unique_values >= 10:
        q = 10
    else:
        return "Sem percentil"  # Not enough data for percentile calculation
    data['decile'] = pd.qcut(data['inde'], q=q, labels=[f'{i}%' for i in range(1, q + 1)], duplicates="drop")
    student_info = data.loc[data['id'] == student_row_id, 'decile']
    return student_info.values[0] if not student_info.empty else "Sem percentil"
    
    def get_concept_stone_inde(self, student_row_id):
        inde_data = self.get_historycal_indicators(student_row_id)['inde'].values[-1]
        if(inde_data < 6.1): return 'Quartzo'
        elif(inde_data >= 6.1 and inde_data < 7.2): return 'Ágata'
        elif(inde_data >= 7.2 and inde_data < 8.2): return 'Ametista'
        elif(inde_data >= 8.2): return 'Topázio'
    

    
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
