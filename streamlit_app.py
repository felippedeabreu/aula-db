import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub  # Importando o kagglehub para baixar o dataset

# Título do aplicativo
st.title("📊 Análise de Dados com Pandas + Streamlit")

# Função para baixar o dataset do Kaggle
@st.cache_data
def baixar_dados_kaggle():
    # Baixa o dataset e retorna o caminho
    path = kagglehub.dataset_download("mosapabdelghany/medical-insurance-cost-dataset")
    return path

# Baixar o dataset e obter o caminho
dataset_path = baixar_dados_kaggle()

# Exibir o caminho para o dataset baixado
st.write(f"📂 Dataset baixado para o caminho: {dataset_path}")

# Carregar o dataset usando pandas
@st.cache_data
def carregar_dados(nome_arquivo):
    return pd.read_csv(nome_arquivo)

# O nome do arquivo dentro do diretório de dados baixados
arquivo = f"{dataset_path}/insurance.csv"
df = carregar_dados(arquivo)

# Mostrar dados
st.subheader("🔍 Visualização da Tabela de Dados")
st.dataframe(df)

# Filtros interativos
st.sidebar.header("🔧 Filtros")
sexo = st.sidebar.multiselect("Sexo", options=df['sex'].unique(),
                              default=df['sex'].unique())
fumante = st.sidebar.selectbox("É fumante?", options=df['smoker'].unique())

# Aplicar filtros
df_filtrado = df[(df['sex'].isin(sexo)) & (df['smoker'] == fumante)]
st.subheader("📌 Dados Filtrados")
st.dataframe(df_filtrado)

# Estatísticas
st.subheader("📈 Estatísticas Descritivas")
st.write(df_filtrado.describe())

# Gráfico 1: Dispersão
st.subheader("💸 Relação entre Total da Conta e Idade")
st.scatter_chart(df_filtrado, x="age", y="charges", color="bmi", size="children")

# Gráfico 2: Bar
st.subheader("📦 Distribuição Custo x Idade")
st.bar_chart(df_filtrado, x="age", y="charges", color="smoker")

# Gráfico 3: Boxplot
st.subheader("📦 Boxplot Custo x Idade")
fig2, ax2 = plt.subplots()
sns.boxplot(data=df_filtrado, x="age", y="charges", ax=ax2)
st.pyplot(fig2)
