import pandas as pd
import streamlit as st
import plotly_express as px
import st_aggrid
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
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
        fig = px.bar(df_monthly, x='Mês', y='Preço EUR', labels={'Preço EUR': 'Custo (€)'})

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
                        color_discrete_sequence=color_scheme,  
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

        # Geral --------------------------------------------------
        custo_mensal = df_trabalho["Preço EUR"].sum()

        st.write('')
        st.write('')
        st.header(f'Custo Mensal                    .: {custo_mensal:.2f} €', divider = 'gray')
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
                        color_discrete_sequence=color_scheme,  
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

        # Tabela AgGrid
        df_categoria = df_trabalho[["Categoria", "Data", "Descrição", "Preço EUR"]]
        gb = GridOptionsBuilder.from_dataframe(df_categoria)
        gb.configure_column(field = "Categoria", header_name = 'Categoria', groupable = True, value = True, enableRowGroup= True, rowGroup=True, hide = True)
        gb.configure_column(field = "Data",  groupable=False, rowGroup=False, header_name="Data", hide= False)
        gb.configure_column(field = "Descrição",  groupable=False, rowGroup=False, header_name="Descrição", hide= False)
        gb.configure_column(field = "Preço EUR", aggFunc="sum", type="numericColumn", valueFormatter="value.toLocaleString('en', {minimumFractionDigits: 2, maximumFractionDigits: 2})", groupable = False, hide = False, header_name = "Preço EUR")
        gb.configure_grid_options(domLayout="normal", suppressAggFuncInHeader = True,groupDisplayType = 'multipleColumns') 
        gridOptions = gb.build()
        st.write('')

        with st.expander("Tabela Agrupada", expanded=False):
            AgGrid(df_categoria, 
                    gridOptions=gridOptions, 
                    height = 300, 
                    allow_unsafe_jscode= True,
                    fit_columns_on_grid_load=True, 
                    update_mode=st_aggrid.GridUpdateMode.NO_UPDATE, 
                    columns_auto_size_mode = ColumnsAutoSizeMode.FIT_CONTENTS,
                    theme="streamlit")
        

        # Por Dia --------------------------------------------------
        st.write('')
        st.write('')
        st.header('Por Dia', divider = 'gray')

        # Agrupar os custos por mês
        df_monthly = df_trabalho.groupby('Data', as_index=False)['Preço EUR'].sum()

        # Criar gráfico com Plotly
        fig = px.bar(df_monthly, x='Data', y='Preço EUR', labels={'Preço EUR': 'Custo (€)'})

        # Exibir gráfico no Streamlit
        st.plotly_chart(fig)        




   
