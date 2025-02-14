import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from models.data_access import DataAccess

##### Dados #####

inde_columns = ['INDE 2024', 'INDE 23', 'INDE 22', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'IPV', 'IAN']
def load_data():
    leitor = DataAccess()
    df = leitor.get_orig()

    # Converter colunas de INDE para numérico
    for col in inde_columns:
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

df = load_data()
df = df.drop(columns=['Cg','Cf','Ct','Rec Av1','Rec Av2','Rec Psicologia','Indicado','Atingiu PV','Destaque IEG','Destaque IDA','Destaque IPV'])

##### Página Streamlit ###########################################################################################

# Página: Análises Gerais
st.title("📊 Análises Gerais")
st.write("Nesta página você encontra um resumo das informações mais relevantes sobre a performance dos alunos da Passos Mágicos em 2024.")
st.markdown("---")

# Quantidade de alunos por gênero #############################################################################
gender_counts = df['Gênero'].value_counts()
col1, col2, col3 = st.columns(3)
icon_total = "&#x1F464;"  # Unicode para o ícone de boneco (total)
icon_feminino = "&#x1F467;"  # Unicode para o ícone de menina
icon_masculino = "&#x1F466;"  # Unicode para o ícone de menino
col1.markdown(f"<h3>{icon_total} Estudantes</h3>", unsafe_allow_html=True)
col1.metric(label="", value=gender_counts.sum())
col2.markdown(f"<h3>{icon_feminino} Feminino</h3>", unsafe_allow_html=True)
col2.metric(label="", value=gender_counts.get('Feminino', 0))
col3.markdown(f"<h3>{icon_masculino} Masculino</h3>", unsafe_allow_html=True)
col3.metric(label="", value=gender_counts.get('Masculino', 0))

with st.expander("Análise Geral das médias dos indicadores e comparação com anos anteriores"):
    st.write("A evolução do INDE (Índice de Desenvolvimento Educacional) dos alunos ativos da PM entre os anos de 2022 e 2024 não teve variação significante, se mantendo na média de 7.41 entre os anos.")
    # Cartões - Médias dos índices ao longo dos anos ##############################################################
    mean_indes = {
        '2022': df['INDE 22'].mean(),
        '2023': df['INDE 23'].mean(),
        '2024': df['INDE 2024'].mean()
    }

    years = list(mean_indes.keys())
    values = [f"{v:.2f}" for v in mean_indes.values()]  # Format as string for display
    variations = ["-"]  # First year has no variation

    for i in range(1, len(values)):
        change = ((float(values[i]) - float(values[i - 1])) / float(values[i - 1])) * 100
        variations.append(f"{change:.2f}%")  # Append variation

    df_table = pd.DataFrame({
        "Ano": years,
        "Média INDE": values,
        "Variação (%)": variations
    })

    st.markdown("<h4 style='font-size:16px;'>Médias dos INDE ao longo dos anos</h4>", unsafe_allow_html=True)
    st.dataframe(df_table,hide_index=True)  # Use st.dataframe(df_table) for an interactive table

    # Gráfico de linhas - Média de indicadores ####################################################################
    st.write("Sendo o INDE composto por diversos outros indicadores (IAA, IEG, IPS, IPP, IDA, IPV e IAN), ele é impactado principalmente pela performance positiva dos alunos no IAA (Indicador de Autoavaliação) e pela performance negativa dos alunos no IDA (Indicador de Desempenho Acadêmico). Essa discrepância pode indicar a necessidade da instituição analisar falhas no ensino, desafios específicos do aluno ou inconsistências no processo de autoavaliação.")
    st.markdown("<h4 style='font-size:16px;'>Médias dos Indicadores que compõem o INDE</h4>", unsafe_allow_html=True)

    mean_metrics = df[['INDE 2024', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'IPV', 'IAN']].mean()
    mean_metrics_df = pd.DataFrame(mean_metrics).reset_index()
    mean_metrics_df.columns = ['Indicador', 'Média']

    fig, ax = plt.subplots(figsize=(12, 3))
    sns.lineplot(data=mean_metrics_df, x="Indicador", y="Média", marker="o", ax=ax, color="b", lw=2)
    ax.set_title("Média dos Indicadores", fontsize=10, fontweight='bold')
    ax.set_xlabel("Indicadores", fontsize=8)
    ax.set_ylabel("Média", fontsize=8)
    plt.xticks(rotation=45, fontsize=8)
    st.pyplot(fig)


# Quantidade de alunos por pedras #############################################################################
with st.expander("Distribuição dos alunos na classificação de Pedra-conceito e Análise dos Indicadores por Pedra-conceito"):
    st.write("A metodologia de Pedra-conceito é utilizada pela Passos Mágicos para classificar seus alunos de acordo com uma faixa de desempenho INDE:")
    st.write("Pedra Topázio: INDE entre 9,4 e 8,2.")  
    st.write("Pedra Ametista: INDE entre 8,2 e 7,2.")  
    st.write("Pedra Ágata: INDE entre 7,2 e 6,1.")  
    st.write("Pedra Quartzo: INDE entre 6,1 e 3,0.")  
    st.write("A maior parte dos alunos se classificam em Topázio e Ametista, indicando um ótimo desempenho geral dos alunos da instituição. Alunos Quartzo, apesar de estarem em menor número, ainda estão em quantidade significativa e precisam de uma atenção especial para conseguirem evoluir para os outros níveis nos próximos anos.")
    st.markdown("<h4 style='font-size:16px;'>Distribuição dos alunos na classificação de Pedra-conceito</h4>", unsafe_allow_html=True)

    stones_counts = df['Pedra 2024'].value_counts()
    col1, col2, col3, col4 = st.columns(4)
    stones = ["Topázio", "Ametista", "Ágata", "Quartzo"]
    col = st.columns(4)
    for i, stone in enumerate(stones):
        with col[i]:
            st.image(f"./assets/{stone}.png", width=80)
            st.markdown(f"<h3>{stone}</h3>", unsafe_allow_html=True)
            st.metric(label="", value=stones_counts.get(stone, 0))

    st.markdown("<h4 style='font-size:16px;'>Médias dos indicadores por Pedra-conceito</h4>", unsafe_allow_html=True)

    # Agrupar por pedra e calcular a média de cada indicador
    df_filtered = df[df['Pedra 2024'].isin(stones)]
    mean_metrics_by_stone = df_filtered.groupby('Pedra 2024')[['INDE 2024', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'IPV', 'IAN']].mean()
    mean_metrics_melted = mean_metrics_by_stone.reset_index().melt(id_vars='Pedra 2024', var_name='Indicador', value_name='Média')

    # Gráfico de linhas - Média de indicadores por pedra
    fig, ax = plt.subplots(figsize=(12, 3))
    sns.lineplot(data=mean_metrics_melted, x="Indicador", y="Média", hue="Pedra 2024", marker="o", ax=ax, lw=2)
    ax.set_title("Média dos Indicadores por Pedra", fontsize=10, fontweight='bold')
    ax.set_xlabel("Indicadores", fontsize=8)
    ax.set_ylabel("Média", fontsize=8)
    plt.xticks(rotation=45, fontsize=8)
    ax.legend(loc="lower right")
    st.pyplot(fig)

    st.write("É evidente que o índice de engajamento (IEG) e o índice de desempenho acadêmico (IDA) são as maiores discrepâncias entre os Alunos Topázio e Alunos Quartzo. Já os indicadores psicosocial (IPS) e psicopedagógico (IPP) não parecem ter grande relevância no distaciamento de desempenho entre esses dois perfis de alunos.")

# Gráfico de barras vertical - Idade com linha de INDE 2024 ################################################

with st.expander("Relacione os Indicadores com Fase Ideal, Idade e Pedra-conceito"):

    # Opções para os filtros
    opcoes_x = ["Idade", "Pedra 2024", "Fase Ideal"]
    opcoes_y_sec = inde_columns

    # Filtros no Streamlit
    eixo_x = st.selectbox("Escolha a variável categárica:", opcoes_x)
    eixo_y_sec = st.selectbox("Escolha o indicador:", opcoes_y_sec)

    # Criando o gráfico
    fig, ax1 = plt.subplots(figsize=(12, 4))

    # Gráfico de barras (quantidade de alunos)
    sns.barplot(x=df[eixo_x].value_counts().index, 
                y=df[eixo_x].value_counts().values, 
                ax=ax1, alpha=0.7)
    ax1.set_ylabel("Quantidade de Alunos", fontsize=8)
    ax1.set_xlabel(eixo_x, fontsize=8)
    ax1.set_title(f"Distribuição de Alunos por {eixo_x} e médias {eixo_y_sec}", fontsize=10, fontweight='bold')
    plt.xticks(rotation=45)

    # Criando eixo secundário
    ax2 = ax1.twinx()

    # Gráfico de linha (média do indicador escolhido)
    sns.lineplot(x=df.groupby(eixo_x)[eixo_y_sec].mean().index, 
                y=df.groupby(eixo_x)[eixo_y_sec].mean().values, 
                ax=ax2, marker='o', linewidth=2.5)
    ax2.set_ylabel(f"Média {eixo_y_sec}", fontsize=8)

    # Exibir gráfico no Streamlit
    st.pyplot(fig)

    st.markdown("<h4 style='font-size:16px;'>Análise por Idade</h4>", unsafe_allow_html=True)
    st.write("O INDE começa a diminuir no início da fase adulta, entre 17 e 23 anos, possivelmente devido a fatores pessoais. Essa queda pode estar relacionada à redução do IEG (Índice de Engajamento), que diminui após os 17 anos. Além disso, o IAA (Índice de Autoavaliação) também sofre uma queda significativa nesse período de transição da adolescência para a vida adulta. No entanto, aos 17 anos, observa-se o maior IPV (Índice de Ponto de Virada), o que pode indicar que a PM já cumpriu seu papel no desenvolvimento do aluno, tornando-o mais independente da instituição.")
    st.markdown("<h4 style='font-size:16px;'>Análise por Fase Ideal</h4>", unsafe_allow_html=True)
    st.write("Quando analisamos os alunos da fase 3 (7ª e 8ª série), que apresentam os menores índices de INDE, é possível identificar que os maiores responsáveis por essa queda são o IAA (Índice de Autoavaliação), o IPP (Indicador Psicopedagógico) e o IDA (Índice de Desempenho Acadêmico). Nesse período, os alunos estão em uma fase de transição emocional e psicológica, o que pode levar a uma diminuição na confiança e na percepção sobre suas próprias habilidades. Além disso, o aumento da complexidade dos conteúdos e a maior pressão por desempenho, juntamente com os fatores emocionais e psicológicos, contribuem para a queda nesses índices.")
