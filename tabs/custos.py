import pandas as pd
import streamlit as st
import plotly_express as px
from utils.functions import gera_markdown
from utils.utils import df_custos, meses_ordenados, ultima_data, dict_cores


def custos():
    # Exibe última data de atualização da planilha 
    st.write(f"Última atualização da planilha de custos: {ultima_data}")    

    # Filtro 1: Quem pagou? =====================================================
    if 'agrupar' not in st.session_state:
        st.session_state.agrupar = 'Pais'

    opcoes_agrupar_por = ['Total', 'Pais', 'Clara']
    st.session_state.agrupar = st.radio('', options= opcoes_agrupar_por, index= opcoes_agrupar_por.index(st.session_state.agrupar), horizontal=True)

    # Pais
    if st.session_state.agrupar == 'Pais':
        df_trabalho = df_custos[df_custos['Quem Pagou?'] == 'Pais']
        gasto_aluguel = 600 * 6
    # Clara
    elif st.session_state.agrupar == 'Clara':
        df_trabalho = df_custos[df_custos['Quem Pagou?'] == 'Clara']
        gasto_aluguel = 0
    # Total
    elif st.session_state.agrupar == 'Total':
        df_trabalho = df_custos
        gasto_aluguel = 600 * 6

    tabs = st.tabs(['Overview', 'Mensal'])

    # Overview =============================================================================

    with tabs[0]:
        st.header('Tabela Completa', divider = 'gray')
        gasto_planilha = round(sum(df_trabalho['Preço EUR']), 2)
        gasto_total = gasto_planilha + gasto_aluguel
        st.subheader(f"Gasto total: {gasto_total}€")
        st.write("Obs.: desconsiderando custos prévios (passagem, seguro, visto, etc.)")
        df_trabalho_summary = df_trabalho[['Data', 'Categoria', 'Descrição', 'Preço EUR', 'Método de Pagamento']]        
        st.dataframe(df_trabalho_summary, hide_index=True, use_container_width=True)

        # Por Mês --------------------------------------------------------------
        st.header('Por Mês', divider = 'gray')

        # Agrupar os custos por mês
        df_monthly = df_trabalho.groupby('Mês', as_index=False)['Preço EUR'].sum()

        # Garantir que todos os meses apareçam no DataFrame
        df_monthly = pd.DataFrame({'Mês': meses_ordenados}).merge(df_monthly, on='Mês', how='left').fillna(0)

        # Criar gráfico com Plotly
        fig = px.bar(df_monthly, x='Mês', y='Preço EUR', labels={'Preço EUR': 'Custo (€)'})

        # Exibir gráfico 
        st.plotly_chart(fig)        
        
        # Criar colunas
        cols = st.columns(len(meses_ordenados))  # Usar todos os meses para manter layout fixo

        # Iterar sobre os meses e custos, garantindo que todos sejam exibidos
        for col, (month, cost) in zip(cols, zip(df_monthly['Mês'], df_monthly['Preço EUR'])):
            mkd = gera_markdown(month, cost)
            with col:
                st.markdown(mkd, unsafe_allow_html=True)                   

        # Categorias --------------------------------------------------------------------
        st.write('')
        st.write('')
        st.header('Por Categoria', divider = 'gray')

        # Agrupar, somar e ordenar os dados
        categ_costs_df = (
            df_trabalho.groupby("Categoria", as_index=False)["Preço EUR"]
            .sum()
            .sort_values(by="Preço EUR", ascending=False)  # Ordenar do maior para o menor
        )

        # Calculando a porcentagem de cada categoria
        categ_costs_df["Porcentagem"] = categ_costs_df["Preço EUR"] / categ_costs_df["Preço EUR"].sum() * 100

        # Criando o gráfico treemap
        fig = px.treemap(categ_costs_df, 
                        path=['Categoria'],  
                        values='Porcentagem',  
                        color='Categoria',  
                        color_discrete_sequence=dict_cores,  
                        title=''
                        )

        # Adiciona os valores em euros como texto dentro dos retângulos
        fig.update_traces(
            texttemplate='%{label} (%{value:.1f}%)<br>',  
            customdata=categ_costs_df['Preço EUR'],
            textfont=dict(size=18),
        )
        fig.update_layout(showlegend=False, margin=dict(r=50, t=0, b=0), height = 300)

        # Exibe no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # Iterando de 5 em 5
        for i in range(0, len(categ_costs_df), 5):
            cols = st.columns(5)  # Criar uma nova linha de colunas
            
            # Pegando um subconjunto do DataFrame
            subset = categ_costs_df.iloc[i:i+5]
            
            for col, (_, row) in zip(cols, subset.iterrows()):
                mkd = gera_markdown(row["Categoria"], row["Preço EUR"])
                with col:
                    st.markdown(mkd, unsafe_allow_html=True)

    # Mensal =============================================================================

    with tabs[1]:   
        if 'mes' not in st.session_state:
            st.session_state.mes = "Janeiro"

        opcoes_filtrar_por = meses_ordenados
        st.session_state.mes = st.radio('Mês', options= opcoes_filtrar_por, index= opcoes_filtrar_por.index(st.session_state.mes), horizontal=True)

        # Filtra dataframe pelo mês
        for mes in meses_ordenados:
            if st.session_state.mes == f'{mes}':
                df_trabalho = df_trabalho[df_trabalho['Mês'] == f'{mes}']
                df_trabalho  = df_trabalho.sort_values('Data', ascending = True)

        # Geral --------------------------------------------------
        custo_mensal = df_trabalho["Preço EUR"].sum()

        st.write('')
        st.write('')
        st.header(f'Custo do mês de {st.session_state.mes}: {custo_mensal:.2f} €', divider = 'gray')
        df_trabalho_summary = df_trabalho[['Data', 'Categoria', 'Descrição', 'Preço EUR', 'Método de Pagamento']]        
        st.dataframe(df_trabalho_summary, hide_index=True, use_container_width=True)

        # Por Categoria --------------------------------------------------
        st.write('')
        st.write('')
        st.header('Por Categoria', divider = 'gray')

        # Agrupar, somar e ordenar os dados
        categ_costs_df = (
            df_trabalho.groupby("Categoria", as_index=False)["Preço EUR"]
            .sum()
            .sort_values(by="Preço EUR", ascending=False)  # Ordenar do maior para o menor
        )

        # Calculando a porcentagem de cada categoria
        categ_costs_df["Porcentagem"] = categ_costs_df["Preço EUR"] / categ_costs_df["Preço EUR"].sum() * 100

        # Criando o gráfico treemap
        fig = px.treemap(categ_costs_df, 
                        path=['Categoria'],  
                        values='Porcentagem',  
                        color='Categoria',  
                        color_discrete_sequence=dict_cores,  
                        title=''
                        )

        # Adiciona os valores em euros como texto dentro dos retângulos
        fig.update_traces(
            texttemplate='%{label} (%{value:.1f}%)<br>',  
            customdata=categ_costs_df['Preço EUR'],
            textfont=dict(size=18),
        )
        fig.update_layout(showlegend=False, margin=dict(r=50, t=0, b=0), height = 300)

        # Exibe no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # Iterando de 5 em 5
        for i in range(0, len(categ_costs_df), 5):
            cols = st.columns(5)  # Criar uma nova linha de colunas
            
            # Pegando um subconjunto do DataFrame
            subset = categ_costs_df.iloc[i:i+5]
            
            for col, (_, row) in zip(cols, subset.iterrows()):
                mkd = gera_markdown(row["Categoria"], row["Preço EUR"])
                with col:
                    st.markdown(mkd, unsafe_allow_html=True)

        with st.expander("Tabela Agrupada", expanded=False):
            if 'categoria' not in st.session_state:
                st.session_state.categoria = "Mercado"

            categorias = set(list(df_trabalho_summary['Categoria']))

            st.session_state.categoria = st.radio('', options= categorias, horizontal=True)

            # Filtra dataframe pelo Categoria
            for categoria in categorias:
                if st.session_state.categoria == f'{categoria}':
                    df_trabalho_summary = df_trabalho_summary[df_trabalho_summary['Categoria'] == f'{categoria}']
            
            st.dataframe(df_trabalho_summary, hide_index=True, use_container_width=True)
        
        # Por Dia --------------------------------------------------
        st.write('')
        st.write('')
        st.header('Por Dia', divider = 'gray')

        # Agrupar os custos por mês
        df_monthly = df_trabalho.groupby('Data', as_index=False)['Preço EUR'].sum()

        # Criar gráfico com Plotly
        fig = px.bar(df_monthly, x='Data', y='Preço EUR', labels={'Preço EUR': 'Custo (€)'})

        # Exibir gráfico 
        st.plotly_chart(fig)        





   
