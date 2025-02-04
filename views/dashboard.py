import streamlit as st
from utils.functions import create_title, create_section_title, create_dataframe_view_stylized, create_student_history, create_scatter_plot, create_radar_polar_plot, create_line_chart_plot
from controllers.dasboard_controller import Cluster_controller, Data_treatment_controller
import matplotlib.pyplot as plt
import numpy as np

create_title("Ficha do(a) estudante")
cluster_creator = Cluster_controller()
data_treater = Data_treatment_controller()

df_raw_data = data_treater.get_raw_data()
active_student_list = df_raw_data[['id', 'nome']][(df_raw_data['situacao'] == 'Cursando') & (df_raw_data['phase'] < 8)]
active_student_list.drop_duplicates(inplace=True)
active_student_list.sort_values(by='nome', inplace=True)

selected_student = st.selectbox(
    "Selecione o(a) estudante:",
    options=active_student_list['nome'],
    key=active_student_list['id'],
    placeholder ='selecione...',
    help='xxx'
)
if(selected_student != ''):
    max_year = df_raw_data['ano_ref'].max()
    selected_student_info = df_raw_data.query("nome == @selected_student and ano_ref == @max_year")
    create_student_history(        
        nome=selected_student_info.nome.values[0],
        idade=selected_student_info.age.values[0],
        sexo=('Masculino' if selected_student_info.male.values[0] else 'Feminino'),
        tipo_escola=('Pública' if selected_student_info.public_school.values[0] else 'Privada'),
        fase=selected_student_info.phase.values[0],
        ano_entrada=selected_student_info.ano_ingresso.values[0],
        escola=selected_student_info.escola.values[0],
        turma=selected_student_info.turma.values[0],
        fase_ideal=selected_student_info.fase_ideal.values[0],
        situacao=selected_student_info.situacao.values[0],
        ra=selected_student_info.ra.values[0]
    )
    radar_plot_values = data_treater.get_compare_indidividual_indicator_with_mean(student_row_id=selected_student_info.id.values[0])
    radar_plot_colors = {
        'Estudante': '#9370DB',
        'Média da fase': '#708090'     
    }
    st.plotly_chart(
        create_radar_polar_plot(
            data=radar_plot_values,
            title='Indicadores atuais do(a) estudante',
            color_map=radar_plot_colors
        ),
        use_container_width=True
    )
    inde_history_data = data_treater.get_historycal_inde(student_row_id=selected_student_info.id.values[0])
    st.plotly_chart(
        create_line_chart_plot(
            data=inde_history_data,
            title='Evolução do INDE',
            x='ano_ref',
            y='inde',
            labels={
                'ano_ref': 'ANO',
                'inde': 'INDE'
            }
        ),
        use_container_width=True
    )
    create_dataframe_view_stylized(data_treater.get_grades_history(student_row_id=selected_student_info.id.values[0]))
    

    if(selected_student_info['phase'].values[0] < 8):
        df_same_phase, df_next_phase = cluster_creator.get_filtered_data_to_cluster_by_student(df_raw_data, selected_student, selected_student_info['phase'].values[0])
        if(len(df_same_phase) < 50):
            st.warning('Sem amostra o suficiente para seguir com predição')
        else:
            df_cluster, df_dimensioned_clustered = cluster_creator.clustering(df_same_phase)
            create_scatter_plot(
                x=df_dimensioned_clustered[:, 0], 
                y=df_dimensioned_clustered[:, 1], 
                c=df_cluster['cluster'], 
                labelX='Componente Principal 1', 
                labelY='Componente Principal 2', 
                title='K-Means após PCA para 2D'
            )

            df_same_phase_clustered = df_same_phase.merge(df_cluster[['id', 'cluster']], left_on='id', right_on='id', how='inner')
            df_next_phase_clustered = df_next_phase.merge(df_same_phase_clustered[['ra', 'cluster']], left_on='ra', right_on='ra', how='inner')
            student_cluster = df_same_phase_clustered[df_same_phase_clustered['nome'] == selected_student]['cluster'].values[0]
            
            agg_data = round(df_next_phase_clustered.groupby(by=['cluster'])[['inde', 'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian']].agg(['mean', 'std']), 2)
            agg_data['count'] = df_next_phase_clustered.groupby(by='cluster').size()
            create_dataframe_view_stylized(agg_data, student_cluster)

    else:
        st.warning('O(a) estudante já se encontra na última fase')
