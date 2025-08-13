import streamlit as st
from streamlit_image_comparison import image_comparison
from io import BytesIO
from PIL import Image
from logic.motor_analise_clinica import obter_campos_especificos, gerar_analise_automatica
from logic.database import buscar_testes_nao_corrigidos, buscar_modelo_por_tipo, salvar_correcao
import time

def app():
    st.header("🔬 Correção Interativa")
    st.markdown("Selecione um teste pendente, insira os dados brutos e o sistema gerará a análise normativa.")

    testes_para_corrigir = buscar_testes_nao_corrigidos()
    if not testes_para_corrigir:
        st.info("Todos os testes lançados já foram corrigidos ou não há testes para corrigir.")
        return

    testes_para_corrigir_map = {f"{t['nome_candidato']} - {t['tipo_teste']} ({t['id'][:8]})": t['id'] for t in testes_para_corrigir}

    with st.container(border=True):
        teste_selecionado_label = st.selectbox("1. Selecione o Teste a Corrigir", options=list(testes_para_corrigir_map.keys()))

        if teste_selecionado_label:
            teste_id = testes_para_corrigir_map[teste_selecionado_label]
            teste_data = next((t for t in testes_para_corrigir if t['id'] == teste_id), None)
            
            modelo_gabarito = buscar_modelo_por_tipo(teste_data['tipo_teste'])
            if not modelo_gabarito:
                st.error(f"Modelo/Gabarito para '{teste_data['tipo_teste']}' não encontrado. Carregue-o no 'Banco de Modelos'.")
                return

            st.subheader(f"Analisando: **{teste_data['tipo_teste']}** para **{teste_data['nome_candidato']}**")

            with st.expander("Visualizar Imagens de Referência (Candidato vs Gabarito)", expanded=True):
                try:
                    img_candidato = Image.open(BytesIO(teste_data['folha_candidato']))
                    img_modelo = Image.open(BytesIO(modelo_gabarito['imagem']))
                    image_comparison(img1=img_candidato, img2=img_modelo, label1="Candidato", label2="Gabarito")
                except Exception as e:
                    st.error(f"Erro ao processar as imagens: {e}.")

            st.subheader("2. Insira os Dados Brutos da Correção")
            with st.form(key=f"correcao_{teste_id}"):
                campos = obter_campos_especificos(teste_data['tipo_teste'])
                dados_brutos = {}
                cols = st.columns(2)
                for i, (campo, tipo, opcoes) in enumerate(campos):
                    with cols[i % 2]:
                        if tipo == "number": dados_brutos[campo] = st.number_input(f"**{campo}**", min_value=0, step=1)
                        elif tipo == "select": dados_brutos[campo] = st.selectbox(f"**{campo}**", options=opcoes)
                
                observacoes = st.text_area("**Observações Adicionais do Avaliador**", height=120)

                if st.form_submit_button("✓ Gerar Análise Normativa e Salvar"):
                    with st.spinner("Analisando..."):
                        st.markdown("<div class='scan-animation'></div>", unsafe_allow_html=True)
                        time.sleep(2)
                    
                    analise = gerar_analise_automatica(teste_data['tipo_teste'], dados_brutos)
                    salvar_correcao(teste_id, dados_brutos, observacoes, analise)
                    st.success("Análise salva com sucesso!")
                    st.rerun()
