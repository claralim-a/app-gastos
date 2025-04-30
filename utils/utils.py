import pandas as pd 

# Dataframes 
df_mesada = pd.read_excel("assets/mesada.xlsx")
df_custos = pd.read_excel("assets/cost_sheet.xlsx")

# df_custos_pais
df_custos_pais = df_custos[df_custos["Quem Pagou?"] == "Pais"]

# df_custos_clara
df_custos_clara = df_custos[df_custos["Quem Pagou?"] == "Clara"]

# Varíavel que armazena a última data disponível
ultima_data = df_custos["Data"].iloc[-1]

# Total aluguel 
total_aluguel = 3500

# Ordem dos meses
ordem_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]
