import pandas as pd 

# Dataframe ===========================================================

# DataFrame de Custos --------------------------------------------------
df_custos = pd.read_excel("assets/cost_sheet.xlsx") # Leitura

# Data
df_custos = df_custos.sort_values('Data', ascending = True) # Ordena por data
df_custos['Data'] = pd.to_datetime(df_custos['Data']).dt.strftime('%d/%m/%Y')
ultima_data = df_custos['Data'].iloc[-1]

# DataFrame Viagem
df_viagens = df_custos[df_custos["Categoria"] == "Viagem"]
total_viagens = sum(df_viagens["Preço EUR"])

# DataFrame de Mesada ------------------------------------------------
df_mesada = pd.read_excel("assets/mesada.xlsx")
df_mesada = df_mesada.sort_values('Data',ascending = True) # Ordena por data
df_mesada['Data'] = pd.to_datetime(df_mesada['Data']).dt.strftime('%d/%m/%Y')

# Variaveis ============================================================

# Total aluguel 
total_aluguel = 3500


# Dicionarios ==========================================================
# Ordem dos meses
meses_ordenados = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]

# Cores
dict_cores = ['#0378A6','#07F2F2','#21405F','#E5E9EF',
                        '#ED7F05','#FFAD1F','#A15500','#E6572C','#FF6047'] 

dict_cores_plus = ['#0378A6','#07F2F2','#21405F','#E5E9EF',
                        '#ED7F05','#FFAD1F','#A15500','#E6572C','#FF6047', 
                        '#0326A6', '#19E0AC', '#E45F52', '#AD0223', '#3E697A',
                        '#036969', '#646669', '#56A5F5']