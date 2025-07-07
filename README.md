# 📊 Custos do Intercâmbio

Acesse o web app: [https://intercambio-es.streamlit.app/](https://intercambio-es.streamlit.app/)

## 🧾 Sobre o projeto

Este aplicativo foi desenvolvido para ajudar na organização financeira durante meu intercâmbio, tanto no controle dos gastos do dia a dia e viagens, quanto no acompanhamento das transferências mensais feitas pelos meus pais (como forma de suporte financeiro). 

Com visualizações interativas, gráficos e filtros, consigo acompanhar facilmente para onde o dinheiro está indo e manter a transparência e o planejamento junto à família.

Obs: dados fictícios.

---

## ⚙️ Funcionalidades

### 📅 **Custos**
- Exibição de gastos completos com filtros por responsável e mês
- Visualização dos custos por categoria (treemap)
- Gráficos mensais e por dia
- Análise detalhada mês a mês

### 💰 **Entradas x Saídas**
- Comparativo entre transferências recebidas e despesas feitas
- Resumo líquido mês a mês
- Tabelas detalhadas de entradas e saídas

### ✈️ **Viagens**
- Resumo geral dos gastos com viagens
- Análise por destino e por categoria de gasto
- Comparação visual em formato de treemap

---

## 🗂️ Estrutura de Pastas

```bash
.
├── app/                        # Arquivo principal que inicia o Streamlit
├── main.py                    # Navegação entre abas
├── tabs/
│   ├── custos.py              # Lógica da aba de custos gerais
│   ├── entradas_saidas.py     # Lógica da aba de entradas x saídas
│   └── viagens.py            # Lógica da aba de viagens
├── utils/
│   ├── functions.py           # Funções auxiliares (ex: markdowns personalizados)
│   └── utils.py              # Dataframes, variáveis e dicionários de uso geral
├── assets/
│   ├── cost_sheet.xlsx        # Planilha com dados de gastos
│   ├── mesada.xlsx            # Planilha com registros de transferências recebidas
│   └── appicon.png           # Ícone do aplicativo
