import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="Segurança Pública - Dashboard", layout="wide")

df = pd.read_excel("base_dados_seguranca_publica.xlsx", sheet_name="Ocorrencias")
df["ID"] = pd.to_numeric(df["ID"], errors="coerce")
df = df.dropna(subset=["ID"]).reset_index(drop=True)
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

st.title("🚨 Sistema Inteligente de Segurança Pública")
st.markdown("Painel para identificação de padrões de criminalidade e apoio à decisão.")

bairros = st.multiselect("Filtrar por bairro:", options=df["Bairro/Região"].unique(),
                          default=df["Bairro/Região"].unique())
df_filtrado = df[df["Bairro/Região"].isin(bairros)]

col1, col2, col3 = st.columns(3)
col1.metric("Total de ocorrências", df_filtrado.shape[0])
col2.metric("Tempo médio de resposta", f'{df_filtrado["Tempo de Resposta (min)"].mean():.1f} min')
col3.metric("Bairro mais crítico", df_filtrado["Bairro/Região"].value_counts().idxmax())

st.divider()

col4, col5 = st.columns(2)

with col4:
    st.subheader("Ocorrências por Bairro")
    fig, ax = plt.subplots()
    df_filtrado["Bairro/Região"].value_counts().plot(kind="bar", ax=ax, color="steelblue")
    st.pyplot(fig)

with col5:
    st.subheader("Ocorrências por Gravidade")
    fig, ax = plt.subplots()
    df_filtrado["Gravidade"].value_counts().plot(kind="bar", ax=ax, color="indianred")
    st.pyplot(fig)

st.divider()

st.subheader("Correlação entre variáveis")
colunas_numericas = ["Viaturas Envolvidas", "Tempo de Resposta (min)",
                      "População da Região", "Iluminação Pública (%)"]
fig, ax = plt.subplots()
sns.heatmap(df_filtrado[colunas_numericas].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

st.divider()

st.subheader("Base de dados filtrada")
st.dataframe(df_filtrado)
