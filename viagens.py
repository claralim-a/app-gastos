import pandas as pd
import streamlit as st
import plotly_express as px
from functions import color_scheme



def viagens():
    df = pd.read_excel("assets/cost_sheet.xlsx")
    df_trabalho = df[df["Categoria"] == "Viagem"]
    df_trabalho = df_trabalho.sort_values("Data", ascending = True)
    df_trabalho['Data'] = pd.to_datetime(df_trabalho['Data']).dt.strftime('%d/%m/%Y')    

    tabs = st.tabs(['Overview', 'Por Viagem'])

    # Overview ==================================================================================
    with tabs[0]:

        st.header(f"Total: {sum(df_trabalho["Preço EUR"]):.2f} €", divider="gray")
        df_trabalho_sumary = df_trabalho[["Data", "Destino-Viagem", "Categoria-Viagem","Descrição", "Preço EUR"]]
        st.dataframe(df_trabalho_sumary, hide_index=True, use_container_width=True)

        df_grouped = df_trabalho.groupby("Destino-Viagem", as_index=False)["Preço EUR"].sum()

        # Calcular a porcentagem de cada destino
        df_grouped["Porcentagem"] = df_grouped["Preço EUR"] / df_grouped["Preço EUR"].sum() * 100

        # Criando o gráfico treemap
        fig = px.treemap(df_grouped, 
                        path=['Destino-Viagem'],  
                        values='Porcentagem',  
                        color='Destino-Viagem',  
                        color_discrete_sequence=color_scheme)

        # Adicionar labels no formato "Destino (X%) - €Y"
        fig.update_traces(
            texttemplate='%{label} (%{value:.1f}%) - €%{customdata:.2f}',  
            customdata=df_grouped['Preço EUR'],
            textfont=dict(size=18))

        # Ajustar layout
        fig.update_layout(showlegend=False, margin=dict(r=0, t=0, b=0), height=300)

        # Exibe 
        st.plotly_chart(fig, use_container_width=True)


    # Por viagem ==================================================================================
    with tabs[1]:
        if 'viagem' not in st.session_state:
            st.session_state.viagem = "Zaragoza"

        opcoes_filtro = set(list(df_trabalho["Destino-Viagem"]))
        st.session_state.viagem = st.radio("", options=opcoes_filtro, horizontal=True)



        for opcao in opcoes_filtro:
            if st.session_state.viagem == f'{opcao}':
                df_trabalho_sumary = df_trabalho_sumary[df_trabalho_sumary["Destino-Viagem"] == f'{opcao}']
                df_trabalho_sumary = df_trabalho_sumary.sort_values("Data", ascending = True)


        custo_viagem = df_trabalho_sumary["Preço EUR"].sum()
        viagem_mkd = f"{st.session_state.viagem}: {custo_viagem:.2f} €"
        st.header(viagem_mkd, divider="gray")
        st.dataframe(df_trabalho_sumary, hide_index=True, use_container_width=True)

        # Agrupa
        df_grouped = df_trabalho_sumary.groupby("Categoria-Viagem", as_index=False)["Preço EUR"].sum()

        # Calcular a porcentagem de cada destino
        df_grouped["Porcentagem"] = df_grouped["Preço EUR"] / df_grouped["Preço EUR"].sum() * 100

        # Criando o gráfico treemap
        fig = px.treemap(df_grouped, 
                        path=['Categoria-Viagem'],  
                        values='Porcentagem',  
                        color='Categoria-Viagem',  
                        color_discrete_sequence=color_scheme)

        # Adicionar labels 
        fig.update_traces(
            texttemplate='%{label} (%{value:.1f}%) - €%{customdata:.2f}',  
            customdata=df_grouped['Preço EUR'],
            textfont=dict(size=18))

        # Ajustar layout
        fig.update_layout(showlegend=False, margin=dict(r=0, t=0, b=0), height=400)

        st.plotly_chart(fig, use_container_width=True)
