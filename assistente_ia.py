import streamlit as st
import google.generativeai as genai

def obter_analise_ia(prompt):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao comunicar com a IA: {e}. Verifique se a API Key do Gemini está configurada corretamente nos 'Secrets' do seu ambiente."

def app():
    st.header("🤖 Assistente IA (Gemini)")
    st.markdown("Consulte a IA para uma segunda opinião sobre os casos analisados.")

    candidatos_analisados = {
        data['nome']: cid for cid, data in st.session_state.candidatos.items() if 'laudo_final' in data
    }

    if not candidatos_analisados:
        st.info("Nenhum candidato com laudo final gerado. Gere um laudo primeiro.")
        return

    nome_selecionado = st.selectbox("Selecione o Candidato para Consultar a IA", options=list(candidatos_analisados.keys()))

    if nome_selecionado:
        cid = candidatos_analisados[nome_selecionado]
        cdata = st.session_state.candidatos[cid]
        
        pergunta = st.text_area("Faça sua pergunta sobre este caso:", placeholder="Ex: Quais pontos focar na devolutiva?")

        if st.button("Perguntar ao Assistente"):
            if pergunta:
                with st.spinner("A IA está a analisar o caso..."):
                    prompt = f"Você é um psicólogo perito em trânsito. Analise o seguinte laudo e responda à pergunta do seu colega.\n\nLAUDO:\n{cdata['laudo_final']}\n\nPERGUNTA: {pergunta}"
                    resposta = obter_analise_ia(prompt)
                    st.markdown("---")
                    st.subheader("Resposta do Assistente IA")
                    st.markdown(resposta)
            else:
                st.error("Por favor, escreva uma pergunta.")