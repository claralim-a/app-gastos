import streamlit as st
import plotly_express as px
from utils.utils import df_viagens, total_viagens, dict_cores


def viagens():
    tabs = st.tabs(['Overview', 'Por Viagem'])

    # Overview ==================================================================================
    with tabs[0]:

        st.header(f"Total: {total_viagens:.2f} €", divider="gray")
        df_viagens_sumary = df_viagens[["Data", "Destino-Viagem", "Categoria-Viagem","Descrição", "Preço EUR"]]
        st.dataframe(df_viagens_sumary, hide_index=True, use_container_width=True)

        df_grouped = df_viagens.groupby("Destino-Viagem", as_index=False)["Preço EUR"].sum()

        # Calcular a porcentagem de cada destino
        df_grouped["Porcentagem"] = df_grouped["Preço EUR"] / df_grouped["Preço EUR"].sum() * 100

        # Criando o gráfico treemap
        fig = px.treemap(df_grouped, 
                        path=['Destino-Viagem'],  
                        values='Porcentagem',  
                        color='Destino-Viagem',  
                        color_discrete_sequence=dict_cores)

        # Adicionar labels no formato "Destino (X%) - €Y"
        fig.update_traces(
            texttemplate='%{label} (%{value:.1f}%) - €%{customdata:.2f}',  
            customdata=df_grouped['Preço EUR'],
            textfont=dict(size=18))

        # Ajustar layout
        fig.update_layout(showlegend=False, margin=dict(r=0, t=0, b=0), height=300)

        # Exibir
        st.plotly_chart(fig, use_container_width=True)


    # Por viagem ==================================================================================
    with tabs[1]:
        if 'viagem' not in st.session_state:
            st.session_state.viagem = "Zaragoza"

        opcoes_filtro = set(list(df_viagens["Destino-Viagem"]))
        st.session_state.viagem = st.radio("", options=opcoes_filtro, horizontal=True)

        for opcao in opcoes_filtro:
            if st.session_state.viagem == f'{opcao}':
                df_viagens_sumary = df_viagens_sumary[df_viagens_sumary["Destino-Viagem"] == f'{opcao}']
                df_viagens_sumary = df_viagens_sumary.sort_values("Data", ascending = True)


        custo_viagem = df_viagens_sumary["Preço EUR"].sum()
        viagem_mkd = f"{st.session_state.viagem}: {custo_viagem:.2f} €"
        st.header(viagem_mkd, divider="gray")
        st.dataframe(df_viagens_sumary, hide_index=True, use_container_width=True)

        # Agrupa
        df_grouped = df_viagens_sumary.groupby("Categoria-Viagem", as_index=False)["Preço EUR"].sum()

        # Calcular a porcentagem de cada destino
        df_grouped["Porcentagem"] = df_grouped["Preço EUR"] / df_grouped["Preço EUR"].sum() * 100

        # Criando o gráfico treemap
        fig = px.treemap(df_grouped, 
                        path=['Categoria-Viagem'],  
                        values='Porcentagem',  
                        color='Categoria-Viagem',  
                        color_discrete_sequence=dict_cores)

        # Adicionar labels 
        fig.update_traces(
            texttemplate='%{label} (%{value:.1f}%) - €%{customdata:.2f}',  
            customdata=df_grouped['Preço EUR'],
            textfont=dict(size=18))

        # Ajustar layout
        fig.update_layout(showlegend=False, margin=dict(r=0, t=0, b=0), height=400)

        st.plotly_chart(fig, use_container_width=True)
