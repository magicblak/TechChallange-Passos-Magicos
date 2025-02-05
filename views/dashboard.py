import streamlit as st
from utils.functions import (
    create_title, 
    create_section_title, 
    create_dataframe_view_stylized, 
    create_student_history, 
    create_scatter_plot, 
    create_radar_polar_plot, 
    create_line_chart_plot, 
    create_relative_bar_chart_for_growth, 
    create_bar_chart_for_grades
)
from controllers.dasboard_controller import Cluster_controller, Data_treatment_controller
import numpy as np

create_title("Ficha do(a) estudante")
cluster_creator = Cluster_controller()
data_treater = Data_treatment_controller()

df_raw_data = data_treater.get_raw_data()
active_student_list = df_raw_data[['id', 'nome', 'phase', 'defasagem', 'male', 'female', 'public_school', 'private_school', 'inde']][(df_raw_data['situacao'] == 'Cursando')]
active_student_list.drop_duplicates(inplace=True)
active_student_list.sort_values(by='nome', inplace=True)
phase_list = ['selecione...', 0, 1, 2, 3, 4, 5, 6, 7, 8]
diff_list = ['selecione...'] + sorted(active_student_list['defasagem'].unique())
gender_list = ['selecione...', 'Masculino', 'Feminino']
school_list = ['selecione...', 'Pública', 'Privada']
create_section_title("Filtros de busca")
col_phase, col_diff, col_gender, col_School = st.columns(4)
with col_phase:
    selected_phase = st.selectbox(
        "Fase:",
        options=phase_list,
        help='Fase atual do(a) estudante. Utilizando esse filtro você verá apenas estudantes da fase selecionada no filtro de estudnate.'
    )
with col_diff:
    selected_diff = st.selectbox(
        "Defasagem:",
        options=diff_list,
        help='Defasagem do(a) estudante. Utilizando esse filtro você verá apenas estudantes da defasagem selecionada no filtro de estudnate.'
    )
with col_gender:
    selected_gender = st.selectbox(
        "Sexo:",
        options=gender_list,
        help='Sexo do(a) estudante. Utilizando esse filtro você verá apenas estudantes do sexo selecionada no filtro de estudnate.'
    )
with col_School:
    selected_school = st.selectbox(
        "Tipo de escola:",
        options=school_list,
        help='Tipo de escola do(a) estudante. Utilizando esse filtro você verá apenas estudantes da escola selecionada no filtro de estudnate.'
    )

if(selected_phase != 'selecione...'):
    active_student_list = active_student_list[active_student_list['phase'] == selected_phase]
if(selected_diff != 'selecione...'):
    active_student_list = active_student_list[active_student_list['defasagem'] == selected_diff]
if(selected_gender == 'Masculino'):
    active_student_list = active_student_list[active_student_list['male'] == 1]
if(selected_gender == 'Feminino'):
    active_student_list = active_student_list[active_student_list['female'] == 1]
if(selected_school == 'Privada'):
    active_student_list = active_student_list[active_student_list['private_school'] == 1]
if(selected_school == 'Pública'):
    active_student_list = active_student_list[active_student_list['public_school'] == 1]

student_name_list = ['selecione...'] + active_student_list['nome'].tolist()
selected_student = st.selectbox(
    "Estudante:",
    options=student_name_list,
    help='Lista com nomes dos(as) estudantes para viualizar de forma individual.'
)

if(selected_student != 'selecione...'):
    max_year = df_raw_data['ano_ref'].max()
    selected_student_info = df_raw_data.query("nome == @selected_student and ano_ref == @max_year")
    concept_strone_value = None
    decile_data = None
    if(selected_student_info['inde'].notna().all()):
        concept_strone_value = data_treater.get_concept_stone_inde(student_row_id=selected_student_info.id.values[0])
        decile_data = data_treater.get_student_deciles(student_row_id=selected_student_info.id.values[0])
    create_student_history(        
        nome=selected_student_info.nome.values[0],
        stone=concept_strone_value,
        inde=round(selected_student_info['inde'].values[0], 2),
        decile=decile_data,
        idade=selected_student_info.age.values[0],
        sexo=('Masculino' if selected_student_info.male.values[0] else 'Feminino'),
        tipo_escola=('Pública' if selected_student_info.public_school.values[0] else 'Privada'),
        fase=selected_student_info.phase.values[0],
        ano_entrada=selected_student_info.ano_ingresso.values[0],
        escola=selected_student_info.escola.values[0],
        turma=selected_student_info.turma.values[0],
        fase_ideal=selected_student_info.ideal_phase.values[0],
        situacao=selected_student_info.situacao.values[0],
        ra=selected_student_info.ra.values[0]
    )
    with st.expander("Análise educacional - Clique para expandir"):
        st.write('Passe o mouse no gráfico e clique para expandir se necessário.')
        col_radar_plot, col_inde_history = st.columns([1,1.2])
        with col_radar_plot:
            radar_plot_values = data_treater.get_compare_indidividual_indicator_with_mean(student_row_id=selected_student_info.id.values[0])
            radar_plot_colors = {
                'Estudante': '#9370DB',
                'Média da fase': '#708090'     
            }
            st.plotly_chart(
                create_radar_polar_plot(
                    data=radar_plot_values,
                    title=' ',
                    color_map=radar_plot_colors
                ),
                use_container_width=True
            )
        with col_inde_history:
            inde_history_data = data_treater.get_historycal_indicators(student_row_id=selected_student_info.id.values[0])[['ano_ref', 'inde']]
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

        col_growth, col_grade = st.columns(2)
        with col_growth:
            grow_data = data_treater.get_student_growing(student_row_id=selected_student_info.id.values[0])
            st.plotly_chart(create_relative_bar_chart_for_growth(
                data=grow_data, 
                x='Indicador', 
                y='Inclinação', 
                title='Evolução do(a) estudante nos indicadores'
            ))
        with col_grade:
            grade_data = data_treater.get_grades_history(student_row_id=selected_student_info.id.values[0])
            st.plotly_chart(create_bar_chart_for_grades(
                data=grade_data, 
                x='disicpline', 
                y='grade',
                color='Ano',
                title='Evolução do(a) estudante nos indicadores'
            ))
    
    if(False):
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
else:
    st.warning('Selecione um estudante para ver o detalhe.')
