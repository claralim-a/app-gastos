import streamlit as st 
import streamlit_antd_components as sac

from costs import costs

def md_menu():
    chosen_menu = sac.menu([

        sac.MenuItem('Costs', icon='bi bi-wallet2'),
        sac.MenuItem('Exchange Rates', icon='bi bi-wallet2'),

    ], open_index=[0, 8], open_all=False, return_index=True, size='md', variant='light', color='gray', format_func='title')
    
    return chosen_menu

def md_main():

    with st.sidebar:
        
        sac.divider(align='center')
        
        chosen_menu = md_menu()
        # st.write(chosen_menu)
        st.markdown(f"<p style='color: gray;'>Page ID: {chosen_menu}</p>", unsafe_allow_html=True)

    match chosen_menu:

        case 0: # Costs
            costs()
