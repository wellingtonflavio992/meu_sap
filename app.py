import streamlit as st
from streamlit_option_menu import option_menu
from pages import cadastro, banco_de_modelos, lancamento_teste, correcao_interativa, laudo_final, relatorios
from logic.database import inicializar_banco_de_dados

st.set_page_config(
    page_title="SAP - Edição Profissional",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa o banco de dados na primeira execução
inicializar_banco_de_dados()

with st.sidebar:
    st.image("https://i.imgur.com/qE4g4Fr.png", width=250)
    app = option_menu(
        menu_title='Menu Principal',
        options=['Cadastro', 'Banco de Modelos', 'Lançamento de Teste', 'Correção Interativa', 'Laudo Final', 'Relatórios'],
        icons=['person-plus-fill', 'archive-fill', 'cloud-upload-fill', 'easel2-fill', 'file-earmark-text-fill', 'graph-up-arrow'],
        menu_icon='shield-shaded', default_index=0,
        styles={
            "container": {"background-color": '#e0f2f1'},
            "icon": {"color": "#004d40", "font-size": "22px"},
            "nav-link": {"font-size": "18px", "color": "#004d40", "--hover-color": "#80cbc4"},
            "nav-link-selected": {"background-color": "#00796b", "color": "white"},
        }
    )

if app == 'Cadastro':
    cadastro.app()
elif app == 'Banco de Modelos':
    banco_de_modelos.app()
elif app == 'Lançamento de Teste':
    lancamento_teste.app()
elif app == 'Correção Interativa':
    correcao_interativa.app()
elif app == 'Laudo Final':
    laudo_final.app()
elif app == 'Relatórios':
    relatorios.app()