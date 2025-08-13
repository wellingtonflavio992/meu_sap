

# =================================================================
# FICHEIRO 11: logic/motor_analise_clinica.py (CÓDIGO ATUALIZADO)
# ONDE GUARDAR: Dentro da pasta 'logic/'
# =================================================================
import json
import re

def clean_html(raw_html):
    """Função para limpar tags HTML de uma string de forma robusta."""
    cleanr = re.compile('<.*?>|&nbsp;')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.replace('Análise Normativa para: ', '') # Remove o título repetido

def obter_campos_especificos(tipo_teste):
    if "BDA" in tipo_teste or "BPA" in tipo_teste or "TE" in tipo_teste:
        return [("Percentil", "number", None)]
    elif "Palográfico" in tipo_teste:
        return [
            ("Produtividade", "select", ["Baixa", "Média", "Alta"]),
            ("Qualidade do Traçado", "select", ["Bom", "Irregular", "Trêmulo"]),
            ("Indicadores de Agressividade", "select", ["Ausentes", "Presentes"])
        ]
    else:
        return [("Resultado (Percentil)", "number", None)]

def gerar_analise_automatica(tipo_teste, dados_brutos):
    analise = f"<h4>Análise Normativa para: {tipo_teste}</h4>"
    if "Palográfico" in tipo_teste:
        analise += "<ul>"
        if dados_brutos.get("Indicadores de Agressividade") == "Presentes":
            analise += "<li style='color:red;'><b>Fator Crítico:</b> A presença de indicadores de agressividade é um fator de alto risco.</li>"
        else:
            analise += "<li>Ausência de indicadores de agressividade primários.</li>"
        analise += "</ul>"
    else:
        percentil = dados_brutos.get("Percentil", dados_brutos.get("Resultado (Percentil)", 0))
        if percentil < 20:
            analise += f"<p style='color:red;'><b>Nível Crítico:</b> Percentil ({percentil}) muito abaixo do esperado (Res. CONTRAN 927/22).</p>"
        elif percentil < 40:
            analise += f"<p style='color:orange;'><b>Nível de Alerta:</b> Percentil ({percentil}) na faixa limítrofe.</p>"
        else:
            analise += f"<p style='color:green;'><b>Nível Adequado:</b> Percentil ({percentil}) compatível com as exigências da condução.</p>"
    return analise

def gerar_sintese_perfil(testes_corrigidos):
    stress = "Controlado"
    agressividade = "Controlada"
    atencao = "Adequada"
    desleixo = "Não observado"
    animosidade = "Não observada"
    pontos_risco = 0
    
    for teste in testes_corrigidos:
        dados = json.loads(teste.get('dados_brutos', '{}'))
        if teste.get('tipo_teste') == 'Palográfico':
            if dados.get('Indicadores de Agressividade') == 'Presentes':
                agressividade = "Elevada (Fator de Risco)"
                animosidade = "Presente"
                pontos_risco += 5
            if dados.get('Qualidade do Traçado') == 'Trêmulo':
                stress = "Elevado (Indicador de Alerta)"
            if dados.get('Produtividade') == 'Baixa':
                desleixo = "Observado (Indicador de Alerta)"
        else: # Testes de Atenção/Raciocínio
            percentil = dados.get('Percentil', 100)
            if percentil < 20:
                atencao = "Déficit de Atenção (Fator de Risco)"
                pontos_risco += 5
            elif percentil < 40 and atencao == "Adequada":
                atencao = "Nível de Atenção Limítrofe (Indicador de Alerta)"

    sintese = f"""
- **Nível de Stress:** {stress}. A capacidade de lidar com a pressão do trânsito é um fator crucial. Resultados indicam um perfil {stress.lower()}.
- **Nível de Agressividade:** {agressividade}. A impulsividade e a agressividade são contraindicadas para a condução. O perfil do candidato indica uma agressividade {agressividade.lower()}.
- **Capacidade de Atenção:** {atencao}. Manter o foco é essencial para a segurança. A avaliação da atenção do candidato resultou num nível {atencao.lower()}.
- **Indicadores de Desleixo/Animosidade:** Desleixo: {desleixo} / Animosidade: {animosidade}.
- **Observações Adicionais:** Análise baseada nos dados quantitativos e qualitativos inseridos pelo avaliador.
"""
    
    resultado_final = "Apto"
    if pontos_risco >= 5:
        resultado_final = "Inapto"
    elif pontos_risco >= 2:
        resultado_final = "Inapto Temporário"
        
    return sintese, resultado_final
