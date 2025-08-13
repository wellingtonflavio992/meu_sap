import streamlit as st
import pandas as pd
import plotly.express as px
from logic.database import buscar_todos_candidatos_com_resultado

def app():
    st.header("📊 Relatórios Dinâmicos")
    st.markdown("Analise a sua base de candidatos com filtros e gráficos interativos.")
    
    candidatos = buscar_todos_candidatos_com_resultado()
    if not candidatos:
        st.warning("Nenhum candidato com laudo final para gerar relatórios.")
        st.stop()

    df = pd.DataFrame(candidatos)

    with st.container(border=True):
        filtro = st.text_input("Pesquisar por Nome, CPF ou RENACH")
        colunas_para_busca = [col for col in ['nome', 'cpf', 'renach'] if col in df.columns]
        
        if filtro and colunas_para_busca:
            query = " | ".join([f"`{col}`.str.contains('{filtro}', case=False, na=False)" for col in colunas_para_busca])
            df_filtrado = df.query(query)
        else:
            df_filtrado = df
        st.dataframe(df_filtrado[['nome', 'cpf', 'renach', 'resultado_final']])

    st.markdown("---")
    st.subheader("Visualização de Dados")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names='resultado_final', title='Distribuição de Resultados Finais', color='resultado_final',
                     color_discrete_map={'Apto':'green', 'Inapto':'red', 'Apto com Ressalvas':'orange'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.bar(df.groupby('escolaridade').size().reset_index(name='contagem'), 
                      x='escolaridade', y='contagem', title='Contagem de Candidatos por Escolaridade')
        st.plotly_chart(fig2, use_container_width=True)
