import streamlit as st
import pandas as pd
import plotly.express as px

def create_title(text):
    st.markdown(f'<h1 style="color: #fbba00;">{text}</h1>', unsafe_allow_html=True)
    
def create_section_title(text):
    st.markdown(f'<h1 style="color: #ed3237;">{text}</h1>', unsafe_allow_html=True)

def create_dataframe_view_stylized(df, selected_index=None):
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
        create_section_title("🔍 Informações Gerais")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("RA", ra)
        col2.metric("Nome", nome)
        col3.metric("Idade", idade)
        col4.metric("Sexo", sexo)

    st.markdown("---")  # Linha divisória

    # Sessão 2: Informações Acadêmicas
    with st.container():
        create_section_title("🏫 Informações Passos Mágicos")
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

def create_radar_polar_plot(data, r='values', theta='indicators', color='type', title='', color_map=None):
    fig = px.line_polar(
        data,
        r=r,
        theta=theta,
        color=color,
        line_close=True,
        title=title,
        color_discrete_map=color_map
    )
    fig.update_traces(
        line_shape='linear',
        line_width=3
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(240,248,255,1)",
            radialaxis=dict(
                showgrid=False,
                showticklabels=False
            ),
            angularaxis=dict(
                showgrid=False,  # Remove linhas de grade ao redor
                tickfont=dict(size=16, family='Arial, sans-serif', color='darkblue')  # Aumenta texto das categorias
            )
        ),
        plot_bgcolor="rgba(0,0,0,0)"  # Fundo do gráfico transparente
    )
    return fig

def create_line_chart_plot(data, x, y, labels, title='', range=[0, 10]):
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        markers=True,
        labels=labels,
        line_shape="linear",
        text=y
    )

    # Personalização do layout
    fig.update_traces(line_width=4, line_color="#9370DB", marker=dict(size=10), textposition="top center")
    fig.update_layout(
        plot_bgcolor="rgba(240,248,255,1)",
        title=dict(font=dict(size=24, color="black")),
        xaxis=dict(title_font=dict(size=18), tickvals=data[x].unique(), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=18), tickfont=dict(size=14), range=[0, 10])
    )
    return fig
