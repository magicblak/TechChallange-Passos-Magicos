import streamlit as st
import pandas as pd
import plotly.express as px

def create_title(text):
    st.markdown(f'<h1 style="color: #004580;">{text}</h1>', unsafe_allow_html=True)
    
def create_section_title(text):
    st.markdown(f'<h5>{text}</h5>', unsafe_allow_html=True)

def create_dataframe_view_stylized(df, selected_index=None):
    def highlight_row(row):
        if row.name == selected_index:
            return ['background-color: #b8dbfc'] * len(row)
        else:
            return [''] * len(row)
    st.dataframe(df.style.apply(highlight_row, axis=1))

def create_student_history(nome, inde, stone, percentile_data, idade, sexo, tipo_escola, fase, ano_entrada, escola, turma, fase_ideal, situacao, ra):
    with st.container():
        create_section_title(f"{str.upper(nome)} ({ra})")
        if(stone != None and percentile_data != None):
            colimg, colstone, colinde, colpercentile_data = st.columns([1,3,3,3])
            with colimg:
                st.image(f"./assets/{stone}.png", use_container_width=True)
            colstone.metric("Pedra-conceito atual", stone)
            colinde.metric("INDE", inde)
            colpercentile_data.metric("Percentil - INDE", percentile_data, help="INDE superior a X% dos estudantes de mesma fase")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Idade", idade)
        col2.metric("Sexo", sexo)
        col3.metric("Situação", situacao)
        col4.metric("Tipo de Escola", tipo_escola)
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Ano de Entrada", ano_entrada)
        col6.metric("Fase", fase)
        col7.metric("Fase Ideal", fase_ideal)
        col8.metric("Turma", turma)

        st.metric("Escola", escola)

def create_scatter_plot(x, y, c=None, labelX='', labelY='', title=''):
    data = pd.DataFrame({'x': x, 'y': y, 'color': c})
    fig = px.scatter(
    data, 
    x='x', 
    y='y', 
    color='color',
    color_discrete_sequence=px.colors.qualitative.Set1,
    labels={'x': labelX, 'y': labelY}, 
    title=title
    )
    st.plotly_chart(fig, use_container_width=True)

def create_radar_polar_plot(data, r='values', theta='indicators', color='type', title='', color_map=None):
    theta_values = data[theta].str.upper()
    fig = px.line_polar(
        data,
        r=r,
        theta=theta_values,
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
        title_font_size=16,
        font=dict(size=14),
        margin=dict(l=40, r=40, t=40, b=40),
        polar=dict(
            radialaxis=dict(
                showgrid=False,
                showticklabels=False
            ),
            angularaxis=dict(
                showgrid=False,
                tickfont=dict(size=14)
            )
        ),
        plot_bgcolor="rgba(0,0,0,0)"
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
    fig.update_traces(line_width=4, line_color="#9370DB", marker=dict(size=10), textposition="top center")
    fig.update_layout(
        title=dict(font=dict(size=16)),
        xaxis=dict(title_font=dict(size=14), tickvals=data[x].unique(), tickfont=dict(size=14)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=14), range=[3, 10])
    )
    return fig

def create_relative_bar_chart_for_growth(data, x, y, title=''):
    data['color'] = data[y].apply(lambda value: 'Evolução positiva' if value > 0 else 'Evolução negativa')
    x_values = data[x].str.upper()
    fig = px.bar(
        data,
        x=x_values,
        y=y,
        title=title,
        color='color',
        color_discrete_map={'Evolução positiva': '#9ACD32', 'Evolução negativa': '#A52A2A'},
        text=y
    )
    fig.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside'
    )    
    fig.update_layout(
        title_font_size=16,
        font=dict(size=14),
        yaxis_title="Inclinação",
        xaxis_title="Indicador",
        yaxis=dict(
            tickmode='linear',
            dtick=.5,
            range=[data[y].min() - 1, data[y].max() + 1]
        )
    )
    return fig

def create_bar_chart_for_grades(data, x, y, color, title=''):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        barmode='group',
        text=y
    )
    fig.update_traces(
        texttemplate='%{text:.2f}',  # Formatar os rótulos com duas casas decimais
        textposition='outside'  # Mostrar os rótulos fora das barras
    )    
    fig.update_layout(
        title_font_size=16,
        font=dict(size=14),
        yaxis_title="Nota",
        xaxis_title="Disciplina",
        yaxis=dict(
            tickmode='linear',
            dtick=1,  # Intervalo entre os ticks
            range=[0, 10]  # Garante que valores negativos e positivos fiquem visíveis
        )
    )
    return fig