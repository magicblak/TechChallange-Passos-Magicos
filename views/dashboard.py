import streamlit as st
from utils.functions import create_title, create_section_title
from controllers.dasboard_controller import Cluster_controller, Data_treatment_controller
import matplotlib.pyplot as plt

create_title("Ficha do(a) estudante")
cluster_creator = Cluster_controller()
data_treater = Data_treatment_controller()

df_raw_data = data_treater.get_treated_data()
df_cluster, df_dimensioned_clustered = cluster_creator.clustering()

fig, ax = plt.subplots()
scatter = ax.scatter(df_dimensioned_clustered[:, 0], df_dimensioned_clustered[:, 1], c=df_cluster['cluster'], cmap='rainbow')
ax.set_xlabel('Componente Principal 1')
ax.set_ylabel('Componente Principal 2')
ax.set_title('K-Means após PCA para 2D')
st.pyplot(fig)

print(df_cluster.head())
print(df_raw_data.head())

df_clustered_raw_data = df_raw_data.merge(df_cluster[['id', 'cluster']], left_on='id', right_on='id', how='inner')
agg_data = round(df_clustered_raw_data.groupby(by=['cluster'])[['inde', 'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian']].agg(['mean', 'std']), 2)
agg_data['count'] = df_clustered_raw_data.groupby(by='cluster').size()
print(agg_data)