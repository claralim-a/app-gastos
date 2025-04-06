import streamlit as st 
import streamlit_antd_components as sac

from custos import costs
from entradas_saidas import entradas_x_saidas
from viagens import viagens

def md_menu():
    chosen_menu = sac.menu([

        sac.MenuItem('Custos', icon='currency-exchange'),
        sac.MenuItem('Entradas x Saídas', icon='arrow-left-right'),
        sac.MenuItem('Viagens', icon='bi bi-airplane'),

    ], open_index=[0, 8], open_all=False, return_index=True, size='md', variant='light', color='gray', format_func='title')
    
    return chosen_menu

def md_main():

    with st.sidebar:
        
        sac.divider(align='center')
        
        chosen_menu = md_menu()
        st.markdown(f"<p style='color: gray;'>Page ID: {chosen_menu}</p>", unsafe_allow_html=True)

    match chosen_menu:

        case 0: # Custos
            costs()

        case 1: # Entradas x Saídas
            entradas_x_saidas()

        case 2: # Viagens
            viagens()
