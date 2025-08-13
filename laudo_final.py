

# =================================================================
# FICHEIRO 7: pages/laudo_final.py (CÓDIGO ATUALIZADO)
# ONDE GUARDAR: Dentro da pasta 'pages/'
# =================================================================
import streamlit as st
import datetime
from logic.motor_analise_clinica import gerar_sintese_perfil, clean_html
from logic.database import buscar_candidatos_com_testes_corrigidos, buscar_testes_corrigidos_por_candidato, salvar_laudo
import urllib.parse

def app():
    st.header("📄 Laudo Final e Síntese da Avaliação")
    st.markdown("Compile as análises de um candidato num laudo técnico completo e profissional.")

    candidatos_prontos = buscar_candidatos_com_testes_corrigidos()
    if not candidatos_prontos:
        st.info("Nenhum candidato possui testes corrigidos para a geração do laudo.")
        return

    nomes_candidatos = {c['nome']: c['id'] for c in candidatos_prontos}
    nome_selecionado = st.selectbox("**1. Selecione o Candidato para Gerar o Laudo**", options=list(nomes_candidatos.keys()))

    if nome_selecionado:
        cid = nomes_candidatos[nome_selecionado]
        cdata = next((c for c in candidatos_prontos if c['id'] == cid), None)

        if st.button(f"✓ Gerar Laudo para {nome_selecionado}"):
            testes_corrigidos = buscar_testes_corrigidos_por_candidato(cid)
            sintese_perfil, resultado_final = gerar_sintese_perfil(testes_corrigidos)
            
            laudo = f"## LAUDO DE AVALIAÇÃO PSICOLÓGICA (PERÍCIA DE TRÂNSITO)\n\n"
            laudo += f"**Data de Emissão:** {datetime.date.today().strftime('%d/%m/%Y')}\n\n---\n"
            laudo += f"### **1. DADOS DE IDENTIFICAÇÃO**\n"
            laudo += f"- **Nome:** {cdata.get('nome')}\n"
            laudo += f"- **CPF:** {cdata.get('cpf')}\n"
            laudo += f"- **RENACH:** {cdata.get('renach')}\n"
            laudo += f"- **Endereço:** {cdata.get('endereco')}\n\n"
            laudo += f"**Psicólogo(a) Responsável:** [Seu Nome Aqui]\n"
            laudo += f"**CRP:** [Seu CRP Aqui]\n\n---\n"
            
            laudo += "### **2. HISTÓRICO E PROCEDIMENTOS**\n"
            laudo += f"**Motivo da Avaliação:** Avaliação psicológica pericial para obtenção/renovação da Carteira Nacional de Habilitação (CNH), conforme Resolução CONTRAN Nº 927/2022.\n"
            laudo += "**Procedimentos Utilizados:** Entrevista individual e aplicação dos seguintes instrumentos psicológicos, devidamente aprovados pelo CFP:\n"
            
            tipos_testes_usados = ", ".join(sorted(list(set(t['tipo_teste'] for t in testes_corrigidos))))
            laudo += f"- {tipos_testes_usados}\n\n---\n"

            laudo += "### **3. ANÁLISE DOS RESULTADOS**\n"
            laudo += "A seguir, apresenta-se a análise integrada dos resultados obtidos nos instrumentos aplicados.\n"
            
            for teste in testes_corrigidos:
                laudo += f"\n\n**Instrumento:** {teste.get('tipo_teste')}\n"
                analise_normativa_html = teste.get('analise_normativa', '')
                analise_normativa_clean = clean_html(analise_normativa_html) # Limpa o HTML
                laudo += analise_normativa_clean
            
            laudo += f"\n\n---\n### **4. SÍNTESE DO PERFIL PSICOLÓGICO**\n"
            laudo += "A análise conjunta dos resultados permite traçar o seguinte perfil psicológico do candidato, focado nos construtos relevantes para a condução segura:\n\n"
            laudo += sintese_perfil
            
            laudo += f"\n\n---\n### **5. CONCLUSÃO**\n"
            laudo += f"Com base na análise técnica e na síntese do perfil psicológico, e em conformidade com as resoluções do Conselho Nacional de Trânsito (CONTRAN) e do Conselho Federal de Psicologia (CFP), o candidato foi considerado:\n\n"
            laudo += f"## **{resultado_final.upper()}**\n\n"
            laudo += "---\n\n"
            laudo += "________________________________________\n"
            laudo += "**[Seu Nome Aqui]**\n"
            laudo += "Psicólogo(a) Perito(a) em Trânsito\n"
            laudo += "CRP: [Seu CRP Aqui]"

            salvar_laudo(cid, laudo, resultado_final)
            cdata['laudo_final'] = laudo
            cdata['resultado_final'] = resultado_final

        if cdata.get('laudo_final'):
            st.subheader("Laudo Gerado")
            resultado_final = cdata['resultado_final']
            if resultado_final == "Apto": st.success(f"**Resultado Final: {resultado_final}**")
            elif "Inapto" in resultado_final: st.error(f"**Resultado Final: {resultado_final}**")
            else: st.warning(f"**Resultado Final: {resultado_final}**")
            
            with st.container(border=True): st.markdown(cdata['laudo_final'])
            
            st.subheader("Partilhar Laudo")
            texto_encoded = urllib.parse.quote(cdata['laudo_final'])
            col1, col2, col3 = st.columns(3)
            with col1: st.link_button("WhatsApp", f"https://api.whatsapp.com/send?text={texto_encoded}")
            with col2: st.link_button("Telegram", f"https://t.me/share/url?url=Laudo&text={texto_encoded}")
            with col3: st.link_button("Email", f"mailto:?subject=Laudo Psicológico - {nome_selecionado}&body={texto_encoded}")
