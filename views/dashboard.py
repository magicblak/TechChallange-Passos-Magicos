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
from controllers.analysis_agents import StudentDashboardAgents
import asyncio


async def analyze_student_data(agents, indicators_explanation, cluster_explanation):
    result = await asyncio.to_thread(
        agents.request_analysis, indicators_explanation, cluster_explanation
    )
    return result

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
        percentile_data = data_treater.get_student_percentile(student_row_id=selected_student_info.id.values[0])
    create_student_history(        
        nome=selected_student_info.nome.values[0],
        stone=concept_strone_value,
        inde=round(selected_student_info['inde'].values[0], 2),
        percentile_data=percentile_data,
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

    general_context = f"""

        Toda essa avaliação está resultando do trabalho de um ONG que oferece aulas de alfabetização, língua portuguesa e matemática para crianças e adolescentes, de 7 a 17 anos, 
        que sejam baixa renda e moradores do município de Embu-Guaçu. 
        Os alunos são divididos por nível de conhecimento, determinado por meio de uma prova de sondagem que é realizada ao ingressarem na Passos Mágicos, 
        e são inseridos em turmas que variam da alfabetização até o nível 8.

        As fases são os momentos de cada estudante, perceba que também se tratam da série desses estudantes
        Fase 0: Destinadas a alunos que estejam em fase de alfabetização ou que apresentem dificuldade na leitura e na escrita
        Fase 1 e 2: Focadas em conteúdo do ensino fundamental 1, sendo explorados com mais detalhes de um nível para o outro
        Fase 3 e 4: Focadas em conteúdo do ensino fundamental 2, sendo explorado com mais detalhes de um nível para o outro
        Fase 5 e 6: Focadas em conteúdos para jovens e adolescentes do ensino médio para um maior nível de conhecimento
        Fase 7 e 8: Destinadas aos jovens alunos terceiranistas e vestibulandos com foco na aceleração do conhecimento

        Indicadores que calculam o aprendizado do aluno em diversas esferas, podem ser interessantes para entender aspctos de destaque e melhoria.
        IAN (Indicador de Adequação de Nível) Fórmula: D = Fase Efetiva - Fase Ideal, sendo D>= 0 Em fase(IAN=10), 0>D>-2 Moderada(IAN=5) e D<-2 severa(IAN=2,5)
        IDA (Indicador de Desempenho Acadêmico) Fórmula: IDA = (Nota Matemática + Nota Português + Nota Inglês) / 3
        IEG (Indicador de Engajamento) Fórmula: IEG = Soma das pontuações das tarefas realizadas e registradas / Número de tarefas
        IAA (Indicador de Autoavaliação) Fórmula: IAA = Soma das pontuações das respostas do estudante / Número total de perguntas
        IPS (Indicador Psicossocial) Fórmula: IPS = Soma das pontuações dos avaliadores / Número de avaliadores PS: Avaliações feitas por psicólogos (comportamental, emocional, social)
        IPP (Indicador Psicopedagógico) Fórmula: IPP = Soma das avaliações sobre aspectos pedagógicos ​/ Número de avaliações
        IPV (Indicador do Ponto de Virada) Fórmula: IPV = Análises longitudinais de progresso acadêmico, engajamento e desenvolvimento emocional
        INDE (Índice de Desenvolvimento Educacional) Fórmula (FASE 0 A 7): IAN*0,1+IDA*0,2+IEG*0,2+IAA*0,1+IPS*0,1+IPP*0,1+IPV*0,2 Fórmula (FASE 8): IAN*0,1+IDA*0,4+IEG*0,2+IAA*0,1+IPS*0,2
        O INDE é o indicador principal e composto pelos demais

        Informações e análises do(a) estudante:
        Informações adicionais: {selected_student_info[['inde', 'age', 'male', 'female', 'public_school', 'private_school', 'phase', 'ideal_phase']].to_string(index=False)}

    """

    indicators_explanation = f""""

        Comparação de indicadores do(a) estudante e média de outros(as) estudantes da mesma fase: {radar_plot_values.to_string(index=False)}
        Evolução do INDE do(a) estudante: {inde_history_data.to_string(index=False)}
        Evolução do(a) indicadores: {grow_data.to_string(index=False)}
        Notas de disciplina do(a) estudantes: {grade_data.to_string(index=False)}
        Posição no percentil do INDE em comparação com alunos da mesma fase: {percentile_data}

    """
    cluster_explanation = f""""
        clusterização considerando alunos que já cursaram a fase do estudante selecionado, o cluster está olhando para a próxima fase do aluno, afim de prever possíveis comportamentos futuros.
        Atente-se, pois a análise de cluster é desconsiderada para alunos da fase 8
        As etapas realizada foram:
        1. tratamento de dados
        2. redimencionammento com PCA bidimencional
        3. clusterização com dados de alunos de mesma turma, cluster do estudante: {student_cluster} resultado da clusterização: {df_cluster.to_string(index=False)}
        4. filtragem dos alunos que possuem resultados da próxima fase para compara com o estudante: {agg_data.to_string(index=False)}
    """
    agents = StudentDashboardAgents()
    result = asyncio.run(analyze_student_data(
        agents,
        indicators_explanation=general_context + indicators_explanation,
        cluster_explanation=general_context + cluster_explanation
    ))
    st.write(result)
    print(result)
else:
    st.warning('Selecione um estudante para ver o detalhe.')