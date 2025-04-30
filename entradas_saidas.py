import pandas as pd
import streamlit as st
from functions import gera_markdown
from utils.utils import total_aluguel, ordem_meses


def entradas_x_saidas():
    # Le a table
    df_mesada = pd.read_excel("assets/mesada.xlsx")
    df_costs = pd.read_excel("assets/cost_sheet.xlsx")

    # Df costs
    df_costs_pais = df_costs[df_costs["Quem Pagou?"] == "Pais"]
    df_costs_pais = df_costs_pais[df_costs_pais["Método de Pagamento"] != "CC"]
    df_costs_pais = df_costs_pais.drop(columns=["Destino-Viagem", "Categoria-Viagem"])
    df_costs_pais['Data'] = pd.to_datetime(df_costs_pais['Data']).dt.strftime('%d/%m/%Y')
    df_costs_pais  = df_costs_pais.sort_values('Data', ascending = True)

    # Variavel saidas_tot
    saidas_tot = df_costs_pais["Preço EUR"].sum()

    # Variável com a última data disponível
    df_mesada  = df_mesada.sort_values('Data', ascending = True)
    df_mesada['Data'] = pd.to_datetime(df_mesada['Data']).dt.strftime('%d/%m/%Y')
    
    # Total mesada
    total_mesada = df_mesada["Preço EUR"].sum()
    entradas_tot = round(total_mesada - total_aluguel, 2)

    # Entradas - saídas
    liquido_tot = entradas_tot - saidas_tot

    # Agrupando e somando por mês
    entradas = df_mesada.groupby("Mês")["Preço EUR"].sum().reset_index()
    entradas.rename(columns={"Preço EUR": "Entrada"}, inplace=True)
    entradas.loc[entradas["Mês"] == "Janeiro", "Entrada"] -= 3500

    saidas = df_costs_pais.groupby("Mês")["Preço EUR"].sum().reset_index()
    saidas.rename(columns={"Preço EUR": "Saída"}, inplace=True)

    # Juntando os dois dataframes por "Mês"
    df_final = pd.merge(entradas, saidas, on="Mês", how="outer")

    # Preenchendo possíveis NaNs com 0
    df_final["Entrada"] = df_final["Entrada"].fillna(0)
    df_final["Saída"] = df_final["Saída"].fillna(0)

    # Calculando o valor líquido
    df_final["Líquido"] = df_final["Entrada"] - df_final["Saída"]

    # Ordenando por Mês 
    df_final["Mês"] = pd.Categorical(df_final["Mês"], categories=ordem_meses, ordered=True)
    df_final = df_final.sort_values("Mês")

    # Front ==================================================
    st.header(f'Entradas x Saídas', divider = 'gray')
    st.write('Obs.: desconsiderando o aluguel')

    # Markdowns
    mkd_entradas = gera_markdown("Entradas", entradas_tot)
    mkd_saidas = gera_markdown("Saidas", saidas_tot)
    mkd_liquido = gera_markdown("Liquido", liquido_tot, use_color=True)

    cols = st.columns(5)
    with cols[0]:
        st.markdown(mkd_entradas, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(mkd_saidas, unsafe_allow_html=True)
    with cols[4]:
        st.markdown(mkd_liquido, unsafe_allow_html=True)

    st.write("")
    st.dataframe(df_final, use_container_width=True, hide_index=True)

    st.write('')
    with st.expander("Detalhamento", expanded=False):
        
        st.write("Planilha de Entradas:")
        st.dataframe(df_mesada, use_container_width=True, hide_index=True)

        st.write("Planilha de Saídas:")
        st.dataframe(df_costs_pais, use_container_width=True, hide_index=True)
