import pandas as pd
import streamlit as st
import plotly_express as px
# import st_aggrid
# from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from functions_costs import gera_markdown, color_scheme, color_scheme_plus
from charts import fn_update_layout


def costs():
    # Le a table
    df_costs = pd.read_excel("assets/cost_sheet.xlsx")

    # Lista com os meses
    meses_ordenados = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]

    # Converte a data
    df_costs['Data'] = pd.to_datetime(df_costs['Data']).dt.strftime('%d/%m/%Y')


    # Filtro 1: Quem pagou? =====================================================
    if 'agrupar' not in st.session_state:
        st.session_state.agrupar = 'Pais'

    opcoes_agrupar_por = ['Total', 'Pais', 'Clara']
    st.session_state.agrupar = st.radio('', options= opcoes_agrupar_por, index= opcoes_agrupar_por.index(st.session_state.agrupar), horizontal=True)

    # Pais
    if st.session_state.agrupar == 'Pais':
        df_trabalho = df_costs[df_costs['Quem Pagou?'] == 'Pais']
    # Clara
    elif st.session_state.agrupar == 'Clara':
        df_trabalho = df_costs[df_costs['Quem Pagou?'] == 'Clara']
    # Total
    elif st.session_state.agrupar == 'Total':
        df_trabalho = df_costs

    total_cost = df_trabalho['Preço EUR'].sum()
    # Titulo
    st.title(f"Custo Do Intercâmbio: {total_cost:.2f} €")
    st.write(f"Média mensal: {total_cost/2:.2f} €")

    tabs = st.tabs(['Overview', 'Mensal', 'Viagens'])

    # Overview =============================================================================

    with tabs[0]:
        df_trabalho_summary = df_trabalho[['Data', 'Categoria', 'Descrição', 'Preço EUR', 'Método de Pagamento']]        
        st.dataframe(df_trabalho_summary, hide_index=True, use_container_width=True)

        st.header('Por mês', divider = 'gray')

        # Por Mês --------------------------------------------------------------

        # Agrupar os custos por mês
        df_monthly = df_trabalho.groupby('Mês', as_index=False)['Preço EUR'].sum()

        # Garantir que todos os meses apareçam no DataFrame
        df_monthly = pd.DataFrame({'Mês': meses_ordenados}).merge(df_monthly, on='Mês', how='left').fillna(0)

        # Criar gráfico com Plotly
        fig = px.bar(df_monthly, x='Mês', y='Preço EUR', title='Custos por Mês', labels={'Preço EUR': 'Custo (€)'})

        # Exibir gráfico no Streamlit
        st.plotly_chart(fig)        
        
        # Criar colunas no Streamlit
        cols = st.columns(len(meses_ordenados))  # Usar todos os meses para manter layout fixo

        # Iterar sobre os meses e custos, garantindo que todos sejam exibidos
        for col, (month, cost) in zip(cols, zip(df_monthly['Mês'], df_monthly['Preço EUR'])):
            mkd = gera_markdown(month, cost)
            with col:
                st.markdown(mkd, unsafe_allow_html=True)                   

        # Categorias --------------------------------------------------------------------
        st.header('Por Categoria', divider = 'gray')

        # Agrupar, somar e ordenar os dados
        categ_costs_df = (
            df_trabalho.groupby("Categoria", as_index=False)["Preço EUR"]
            .sum()
            .sort_values(by="Preço EUR", ascending=False)  # Ordenar do maior para o menor
        )

        # Iterando de 5 em 5
        for i in range(0, len(categ_costs_df), 5):
            cols = st.columns(5)  # Criar uma nova linha de colunas
            
            # Pegando um subconjunto do DataFrame
            subset = categ_costs_df.iloc[i:i+5]
            
            for col, (_, row) in zip(cols, subset.iterrows()):
                mkd = gera_markdown(row["Categoria"], row["Preço EUR"])
                with col:
                    st.markdown(mkd, unsafe_allow_html=True)

        # Identificar as duas menores categorias
        menores_categorias = categ_costs_df.tail(2)

        # Criar uma nova linha para "Outros" com a soma das duas menores categorias
        linha_outros = pd.DataFrame({
            "Categoria": ["Outros"],
            "Preço EUR": [menores_categorias["Preço EUR"].sum()],
            "Porcentagem": [menores_categorias["Preço EUR"].sum() / categ_costs_df["Preço EUR"].sum() * 100],
            "Total": ["Gastos Totais"]
        })

        # Remover as duas menores categorias do DataFrame
        categ_costs_df = categ_costs_df.drop(menores_categorias.index)

        # Adicionar a linha "Outros" ao final do DataFrame
        categ_costs_df = pd.concat([categ_costs_df, linha_outros], ignore_index=True)            
        
        # Calculando a porcentagem de cada categoria
        categ_costs_df["Porcentagem"] = categ_costs_df["Preço EUR"] / categ_costs_df["Preço EUR"].sum() * 100

        # Criando um valor fictício "Total" para que todas as categorias sejam empilhadas em uma única barra
        categ_costs_df["Total"] = "Gastos Totais"

        # # Criando o gráfico de barra empilhada
        # fig = px.bar(
        #     categ_costs_df, 
        #     x="Porcentagem", 
        #     y="Total", 
        #     color="Categoria",
        #     color_discrete_sequence=color_scheme, 
        #     # text=categ_costs_df["Categoria"],
        #     text=categ_costs_df.apply(lambda row: f"{row['Categoria']} ({row['Porcentagem']:.2f}%)", axis=1),  # Exibindo a categoria e a porcentagem
        #     title="",
        #     orientation="h"  # Faz as barras horizontais
        # )

        # fig.update_layout(
        #     xaxis=dict(title="%", showticklabels=True, showgrid=False, zeroline=False),
        #     yaxis=dict(title="", showticklabels=False, showgrid=False, zeroline=False),
        #     showlegend=False,
        #     height=150,
        #     width=1000,
        #     margin=dict(l=0, r=100, t=0, b=0)  # Reduces extra margins
        # )     

        # st.plotly_chart(fig, use_container_width=False)

        cols = st.columns(2)

        with cols[0]:

            fig = px.pie(categ_costs_df, 
                            values = 'Porcentagem', 
                            names = 'Categoria', 
                            title = '', 
                            color= 'Categoria',
                            color_discrete_sequence = color_scheme, 
                            hole= 0.5)
            
            fig = fn_update_layout(fig, 500, 400, '', 17, "", "", 14, 14, '')
            
            fig.update_traces(
            textposition='outside',
            texttemplate='%{label} (%{percent:.1%})',
            customdata=categ_costs_df['Preço EUR']
            )
            fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

        # # Filtro 2: Mês =====================================================   
        # if 'mes' not in st.session_state:
        #     st.session_state.mes = 'Total'

        # opcoes_filtrar_por = ['Total'] + meses_ordenados
        # st.session_state.mes = st.radio('Mês', options= opcoes_filtrar_por, index= opcoes_filtrar_por.index(st.session_state.mes), horizontal=True)

        # # Filtra dataframe pelo mês
        # for mes in meses_ordenados:
        #     if st.session_state.mes == f'{mes}':
        #         df_trabalho = df_trabalho[df_trabalho['Mês'] == f'{mes}']


   
