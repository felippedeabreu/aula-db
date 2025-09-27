import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub  # Para baixar o dataset do Kaggle

# Título do aplicativo
st.title("📊 Análise de Dados com Pandas + Streamlit")

# Baixar o dataset com kagglehub
@st.cache_data
def baixar_dados_kaggle():
    path = kagglehub.dataset_download("mosapabdelghany/medical-insurance-cost-dataset")
    return path

# Caminho do arquivo CSV
dataset_path = baixar_dados_kaggle()
arquivo = f"{dataset_path}/insurance.csv"

# Carregar e preparar os dados
@st.cache_data
def carregar_dados(nome_arquivo):
    df = pd.read_csv(nome_arquivo)

    # Categorizar número de filhos: 0, 1, 2, 3+
    df["filhos_categoria"] = df["children"].apply(lambda x: str(x) if x < 3 else "3+")

    return df

df = carregar_dados(arquivo)

# Mostrar os dados originais
st.subheader("🔍 Visualização da Tabela de Dados")
st.dataframe(df)

# Filtros interativos
st.sidebar.header("🔧 Filtros")

sexo = st.sidebar.multiselect("Sexo", options=df["sex"].unique(), default=df["sex"].unique())

fumante = st.sidebar.selectbox("É fumante?", options=df["smoker"].unique())

filhos = st.sidebar.multiselect("Número de Filhos", options=["0", "1", "2", "3+"], default=["0", "1", "2", "3+"])

regioes = st.sidebar.multiselect("Região", options=df["region"].unique(), default=df["region"].unique())

# Filtro de faixa etária
idade_min = int(df["age"].min())
idade_max = int(df["age"].max())

idade_selecionada = st.sidebar.slider(
    "Faixa Etária",
    min_value=idade_min,
    max_value=idade_max,
    value=(idade_min, idade_max),
    step=1
)

# Aplicar os filtros
df_filtrado = df[
    (df["sex"].isin(sexo)) &
    (df["smoker"] == fumante) &
    (df["filhos_categoria"].isin(filhos)) &
    (df["region"].isin(regioes)) &
    (df["age"] >= idade_selecionada[0]) &
    (df["age"] <= idade_selecionada[1])
]

# Mostrar os dados filtrados
st.subheader("📌 Dados Filtrados")
st.dataframe(df_filtrado)

# Estatísticas descritivas
st.subheader("📈 Estatísticas Descritivas")
st.write(df_filtrado.describe())

# Gráfico 1: Dispersão
st.subheader("💸 Relação entre Total da Conta e Idade")
st.scatter_chart(df_filtrado, x="age", y="charges", color="bmi", size="children")

# Gráfico 2: Gráfico de Barras
st.subheader("📦 Distribuição Custo x Idade")
st.bar_chart(df_filtrado, x="age", y="charges", color="smoker")

# Gráfico 3: Boxplot
st.subheader("📦 Boxplot Custo x Idade")
fig2, ax2 = plt.subplots()
sns.boxplot(data=df_filtrado, x="age", y="charges", ax=ax2)
st.pyplot(fig2)
