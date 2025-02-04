import streamlit as st
import pandas as pd
import plotly.express as px

def create_title(text):
    st.markdown(f'<h1 style="color: #fbba00;">{text}</h1>', unsafe_allow_html=True)
    
def create_section_title(text):
    st.markdown(f'<h1 style="color: #ed3237;">{text}</h1>', unsafe_allow_html=True)

def create_dataframe_view_stylized(df, selected_index):
    def highlight_row(row):
        if row.name == selected_index:  # Usa o índice correto da linha
            return ['background-color: #b8dbfc'] * len(row)  # Destaca a linha selecionada
        else:
            return [''] * len(row)
    
    # Aplica o estilo e exibe o DataFrame estilizado
    st.dataframe(df.style.apply(highlight_row, axis=1))

def create_student_history(nome, idade, sexo, tipo_escola, fase, ano_entrada, escola, turma, fase_ideal, situacao, ra):
    st.title("📋 Ficha de Consulta do Aluno")

    # Sessão 1: Informações Pessoais
    with st.container():
        st.subheader("🔍 Informações Gerais")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("RA", ra)
        col2.metric("Nome", nome)
        col3.metric("Idade", idade)
        col4.metric("Sexo", sexo)

    st.markdown("---")  # Linha divisória

    # Sessão 2: Informações Acadêmicas
    with st.container():
        st.subheader("🏫 Informações Passos Mágicos")
        col1, col2 = st.columns(2)
        col1.metric("Ano de Entrada", ano_entrada)
        col2.metric("Situação", situacao)

        col3, col4, col5, col6 = st.columns(4)
        col3.metric("Tipo de Escola", tipo_escola)
        col4.metric("Fase", fase)
        col5.metric("Fase Ideal", fase_ideal)
        col6.metric("Turma", turma)

        st.metric("Escola", escola)

def create_scatter_plot(x, y, c=None, labelX='', labelY='', title=''):
    data = pd.DataFrame({'x': x, 'y': y, 'color': c})
    fig = px.scatter(
    data, 
    x='x', 
    y='y', 
    color='color',
    color_continuous_scale='rainbow',
    labels={'x': labelX, 'y': labelY}, 
    title=title
    )
    st.plotly_chart(fig, use_container_width=True)
