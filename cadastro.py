import streamlit as st
from logic.database import adicionar_candidato, buscar_todos_candidatos

def app():
    st.header("👤 Cadastro de Candidatos")
    st.markdown("Insira os dados demográficos completos do candidato.")

    with st.container(border=True):
        with st.form("cadastro_form"):
            st.subheader("Informações Pessoais e Documentos")
            
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("**Nome Completo***")
                cpf = st.text_input("**CPF***")
                telefone = st.text_input("**Telefone***")
                cidade = st.text_input("Cidade")
            with col2:
                renach = st.text_input("RENACH")
                email = st.text_input("Email")
                profissao = st.text_input("Profissão")
                estado = st.text_input("Estado")
            
            escolaridade = st.selectbox("**Escolaridade***", ["", "Não informado", "Ensino Fundamental Incompleto", "Ensino Fundamental Completo", "Ensino Médio Completo", "Ensino Superior Completo"])
            endereco = st.text_area("**Endereço Completo***")

            if st.form_submit_button("✓ Salvar Candidato"):
                campos_obrigatorios = [nome, cpf, escolaridade, telefone, endereco]
                if not all(campos_obrigatorios):
                    st.error("Por favor, preencha todos os campos marcados com *.")
                else:
                    adicionar_candidato(nome, cpf, renach, telefone, email, profissao, escolaridade, endereco, cidade, estado)
                    st.success(f"Candidato '{nome}' cadastrado com sucesso!")
                    st.rerun()

    st.subheader("Candidatos Cadastrados")
    candidatos = buscar_todos_candidatos()
    if not candidatos:
        st.info("Nenhum candidato cadastrado.")
    else:
        for candidato in candidatos:
            with st.expander(f"**{candidato['nome']}** - RENACH: {candidato.get('renach', 'N/A')}"):
                st.write(f"**CPF:** {candidato.get('cpf', 'N/A')}")
