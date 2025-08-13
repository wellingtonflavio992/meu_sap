import streamlit as st
from logic.database import buscar_todos_candidatos, adicionar_teste

TESTES_APROVADOS = sorted(["BPA2", "Palográfico", "R-1", "MVPT", "TRL", "R-1b", "BDA-AA", "BDA-AC", "BDA-AD", "TERM-2", "Outro"])

def app():
    st.header("📤 Lançamento de Testes do Candidato")
    st.markdown("Selecione o candidato e carregue uma ou várias folhas de respostas.")

    candidatos = buscar_todos_candidatos()
    if not candidatos:
        st.warning("Nenhum candidato cadastrado. Vá para 'Cadastro' primeiro.")
        st.stop()

    with st.container(border=True):
        nomes_candidatos = {c['nome']: c['id'] for c in candidatos}
        
        nome_selecionado = st.selectbox(
            "**1. Selecione o Candidato**",
            options=list(nomes_candidatos.keys()),
            index=None,
            placeholder="Escolha um candidato..."
        )
        
        if nome_selecionado:
            candidato_id = nomes_candidatos[nome_selecionado]
            teste_selecionado = st.selectbox("**2. Selecione o Tipo de Teste**", options=TESTES_APROVADOS)
            
            uploaded_files = st.file_uploader(
                "**3. Carregue uma ou mais Folhas de Respostas**",
                type=['png', 'jpg', 'jpeg'],
                accept_multiple_files=True
            )

            if st.button("✓ Adicionar Testes para Correção"):
                if uploaded_files:
                    count = 0
                    for uploaded_file in uploaded_files:
                        adicionar_teste(candidato_id, teste_selecionado, uploaded_file.getvalue())
                        count += 1
                    st.success(f"{count} teste(s) do tipo '{teste_selecionado}' adicionado(s).")
                else:
                    st.error("É necessário carregar pelo menos uma folha de respostas.")
