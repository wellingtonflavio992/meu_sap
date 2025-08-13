
# =================================================================
# FICHEIRO 4: pages/banco_de_modelos.py (CÓDIGO ATUALIZADO)
# ONDE GUARDAR: Dentro da pasta 'pages/'
# =================================================================
import streamlit as st
from logic.file_converter import process_uploaded_file
from logic.database import adicionar_modelo, buscar_todos_modelos, excluir_modelo

TESTES_APROVADOS = sorted(["BPA2", "Palográfico", "R-1", "MVPT", "TRL", "R-1b", "BDA-AA", "BDA-AC", "BDA-AD", "TERM-2", "Outro"])

def app():
    st.header("🗂️ Banco de Modelos e Gabaritos")
    st.markdown("Carregue aqui os modelos de correção (Imagens ou PDF).")
    with st.container(border=True):
        st.subheader("Adicionar Novo Modelo")
        with st.form("upload_modelo_form", clear_on_submit=True):
            teste_selecionado = st.selectbox("Tipo de teste do modelo", options=TESTES_APROVADOS)
            modelo_file = st.file_uploader("Carregue o ficheiro do modelo", type=['png', 'jpg', 'jpeg', 'pdf'])
            
            if st.form_submit_button("✓ Salvar Modelo no Banco"):
                if modelo_file:
                    image_bytes = process_uploaded_file(modelo_file)
                    if image_bytes:
                        adicionar_modelo(teste_selecionado, image_bytes)
                        st.success(f"Modelo para '{teste_selecionado}' salvo!")
                        st.rerun()
                else:
                    st.error("Por favor, carregue um ficheiro.")
    
    st.subheader("Modelos Salvos")
    modelos = buscar_todos_modelos()
    if not modelos:
        st.info("Nenhum modelo carregado.")
    else:
        cols = st.columns(4)
        for i, modelo in enumerate(modelos):
            with cols[i % 4]:
                with st.container(border=True):
                    st.caption(f"**{modelo['tipo_teste']}**")
                    st.image(modelo['imagem'], use_container_width=True)
                    if st.button("Excluir", key=f"delete_{modelo['tipo_teste']}", use_container_width=True):
                        excluir_modelo(modelo['tipo_teste'])
                        st.success(f"Modelo '{modelo['tipo_teste']}' excluído!")
                        st.rerun()

