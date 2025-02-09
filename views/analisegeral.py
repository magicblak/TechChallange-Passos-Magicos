import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

##### Dados #####

def load_data():
    file_path = r'C:\Users\FabiaBocayuva\Documents\Python Scripts\Streamlit_App\PEDE 2024 - DATATHON - PEDE2024.csv'
    df = pd.read_csv(file_path)
    
    # Converter colunas de INDE para numérico
    inde_columns = ['INDE 2024', 'INDE 23', 'INDE 22', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'IPV', 'IAN']
    for col in inde_columns:
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

df = load_data()
df = df.drop(columns=['Cg','Cf','Ct','Rec Av1','Rec Av2','Rec Psicologia','Indicado','Atingiu PV','Destaque IEG','Destaque IDA','Destaque IPV'])

##### Página Streamlit ####
# Configuração de estilo
st.set_page_config(layout="wide", page_title="Dashboard de Alunos")

plt.style.use('bmh')
sns.set_palette("pastel")

# Criar a barra de menu
menu = ["Análises Gerais", "Análise do Aluno", "Análise do Avaliador"]
escolha = st.sidebar.radio("Selecione uma página:", menu)

# Página: Análises Gerais
if escolha == "Análises Gerais":
    st.title("📊 Análises Gerais")
    st.markdown("---")

    # 1. Quantidade de alunos
    total_alunos = df['Nome Anonimizado'].nunique()
    st.metric(label="Total de Alunos", value=total_alunos)
    # Cartões - Médias dos INDE ao longo dos anos
    mean_indes = {
        '2022': df['INDE 22'].mean(),
        '2023': df['INDE 23'].mean(),
        '2024': df['INDE 2024'].mean()
    }

    st.markdown("### Médias dos INDE ao longo dos anos")
    col6, col7, col8 = st.columns(3)
    colunas = [col6, col7, col8]
    years = list(mean_indes.keys())
    values = list(mean_indes.values())

    for i in range(len(values)):
        if i > 0:
            change = ((values[i] - values[i-1]) / values[i-1]) * 100
            var_text = f"<p>Variação: {change:.2f}%</p>"
        else:
            var_text = ""
        colunas[i].markdown(f"<div class='metric-container'><h2>{years[i]}</h2><h1>{values[i]:.2f}</h1>{var_text}</div>", unsafe_allow_html=True)


    # 2. Gráfico de pizza - Distribuição de Gênero
    gender_counts = df['Gênero'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    colors = sns.color_palette("pastel")
    wedges, texts, autotexts = ax1.pie(
        gender_counts, labels=gender_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'}
    )
    plt.setp(autotexts, size=10, weight="bold")
    ax1.set_title("Distribuição por Gênero", fontsize=14, fontweight='bold')

    # 3. Gráfico de barras vertical - Idade com linha de INDE 2024
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df['Idade'].value_counts().index, 
                y=df['Idade'].value_counts().values, 
                ax=ax2, color=colors[1], alpha=0.7)
    ax2.set_ylabel("Quantidade de Alunos", fontsize=11)
    ax2.set_xlabel("Idade", fontsize=11)
    ax2.set_title("Distribuição de Alunos por Idade e médias INDE 24", fontsize=13, fontweight='bold')
    plt.xticks(rotation=45)

    ax3 = ax2.twinx()
    sns.lineplot(x=df.groupby('Idade')['INDE 2024'].mean().index, 
                 y=df.groupby('Idade')['INDE 2024'].mean().values, 
                 ax=ax3, color=colors[0], marker='o', linewidth=2.5)
    ax3.set_ylabel("Média INDE 2024", fontsize=11)

    # 4. Gráfico de barras vertical - Fase Ideal com linha de INDE 2024
    fig3, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df['Fase Ideal'].value_counts().index, 
                y=df['Fase Ideal'].value_counts().values, 
                ax=ax4, color=colors[2], alpha=0.7)
    ax4.set_ylabel("Quantidade de Alunos", fontsize=11)
    ax4.set_xlabel("Fase Ideal", fontsize=11)
    ax4.set_title("Quantidade de Alunos por Fase Ideal e médias INDE 24", fontsize=13, fontweight='bold')
    plt.xticks(rotation=45)

    ax5 = ax4.twinx()
    sns.lineplot(x=df.groupby('Fase Ideal')['INDE 2024'].mean().index, 
                 y=df.groupby('Fase Ideal')['INDE 2024'].mean().values, 
                 ax=ax5, color=colors[3], marker='s', linewidth=2.5)
    ax5.set_ylabel("Média INDE 2024", fontsize=11)

    # 5. Gráfico de barras - Média de indicadores por Gênero
    mean_metrics = df.groupby('Gênero')[['INDE 2024', 'IAA', 'IEG', 'IPS', 'IPP', 'IDA', 'IPV', 'IAN']].mean().reset_index()
    fig5, ax7 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=mean_metrics.melt(id_vars='Gênero', var_name='Indicador', value_name='Média'), 
                x='Indicador', y='Média', hue='Gênero', ax=ax7, palette="Set2")
    ax7.set_title("Média dos Indicadores por Gênero", fontsize=14, fontweight='bold')
    ax7.set_xlabel("Indicadores", fontsize=12)
    ax7.set_ylabel("Média", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    ax7.legend(title="Gênero", loc="upper right")

    # Organizando os gráficos
    col1, col2 = st.columns(2)
    col1.pyplot(fig1)
    col2.pyplot(fig5)

    st.markdown("---")
    st.pyplot(fig2)
    st.pyplot(fig3)

   
# Página: Análise do Aluno
elif escolha == "Análise do Aluno":
    st.title("Análise do Aluno")
    st.write("Detalhamento por aluno ainda não implementado.")

# Página: Análise do Avaliador
elif escolha == "Análise do Avaliador":
    st.title("Análise do Avaliador")

    avaliadores = ['Avaliador1', 'Avaliador2', 'Avaliador3', 'Avaliador4', 'Avaliador5', 'Avaliador6']
    avaliador_escolhido = st.selectbox("Selecione o Avaliador:", avaliadores)
    avaliador_stats_inde = df.groupby(avaliador_escolhido)[['INDE 2024', 'INDE 23', 'INDE 22']].agg(['mean', 'max', 'min']).round(2).reset_index()

    # Flatten the multi-level columns for easier readability
    avaliador_stats_inde.columns = [' '.join(col).strip() for col in avaliador_stats_inde.columns.values]

    # Display the resulting DataFrame
    st.dataframe(avaliador_stats_inde)

    avaliador_nomes = df[avaliador_escolhido].dropna().unique()
    avaliador_nome_escolhido = st.selectbox("Selecione o nome do Avaliador:", avaliador_nomes)
    
    # Filtrar dados do avaliador
    filtered_df = df[df[avaliador_escolhido] == avaliador_nome_escolhido]
    # Média dos INDEs do avaliador escolhido
    # Filter the DataFrame for the specific 'avaliador_nome_escolhido'
    avaliador_mean = avaliador_stats_inde[avaliador_stats_inde[avaliador_escolhido] == avaliador_nome_escolhido]

    # Select only the columns related to the mean
    mean_columns = [col for col in avaliador_stats_inde.columns if 'mean' in col]
    avaliador_mean = avaliador_mean[[avaliador_escolhido] + mean_columns]

    # Display the resulting DataFrame
    st.dataframe(avaliador_mean)

    if not avaliador_mean.empty:
        years = ['2022', '2023', '2024']
        inde_values = [avaliador_mean['INDE 22 mean'].values[0], avaliador_mean['INDE 23 mean'].values[0], avaliador_mean['INDE 2024 mean'].values[0]]
        
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(years, inde_values, marker='o', linestyle='-', color='b', label=f'{avaliador_nome_escolhido}')
        ax.set_xlabel('Ano')
        ax.set_ylabel('Média INDE')
        ax.set_title(f'Média dos INDEs para {avaliador_nome_escolhido}')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
    else:
        st.write("Nenhum dado encontrado para este avaliador.")
