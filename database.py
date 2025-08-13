
# =================================================================
# FICHEIRO 9: logic/database.py (CÓDIGO ATUALIZADO)
# ONDE GUARDAR: Crie a pasta 'logic/' e salve o ficheiro dentro dela.
# =================================================================
import sqlite3
import uuid
import json

DB_NAME = "sap_database.db"

def conectar_bd():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco_de_dados():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidatos (
        id TEXT PRIMARY KEY, nome TEXT NOT NULL, cpf TEXT, renach TEXT, telefone TEXT, email TEXT,
        profissao TEXT, escolaridade TEXT, endereco TEXT, cidade TEXT, estado TEXT,
        laudo_final TEXT, resultado_final TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
        tipo_teste TEXT PRIMARY KEY, imagem BLOB NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS testes (
        id TEXT PRIMARY KEY, candidato_id TEXT NOT NULL, tipo_teste TEXT NOT NULL, folha_candidato BLOB,
        dados_brutos TEXT, observacoes_avaliador TEXT, analise_normativa TEXT, corrigido INTEGER DEFAULT 0,
        FOREIGN KEY (candidato_id) REFERENCES candidatos (id)
    )""")
    conn.commit()
    conn.close()

def adicionar_candidato(nome, cpf, renach, telefone, email, profissao, escolaridade, endereco, cidade, estado):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidatos (id, nome, cpf, renach, telefone, email, profissao, escolaridade, endereco, cidade, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (str(uuid.uuid4().hex), nome, cpf, renach, telefone, email, profissao, escolaridade, endereco, cidade, estado))
    conn.commit()
    conn.close()

def buscar_todos_candidatos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cpf, renach FROM candidatos ORDER BY nome")
    return [dict(row) for row in cursor.fetchall()]

def adicionar_modelo(tipo_teste, imagem):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO modelos (tipo_teste, imagem) VALUES (?, ?)", (tipo_teste, imagem))
    conn.commit()
    conn.close()

def buscar_todos_modelos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modelos ORDER BY tipo_teste")
    return [dict(row) for row in cursor.fetchall()]

def excluir_modelo(tipo_teste):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM modelos WHERE tipo_teste = ?", (tipo_teste,))
    conn.commit()
    conn.close()

def adicionar_teste(candidato_id, tipo_teste, folha_candidato):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO testes (id, candidato_id, tipo_teste, folha_candidato) VALUES (?, ?, ?, ?)",
                   (str(uuid.uuid4().hex), candidato_id, tipo_teste, folha_candidato))
    conn.commit()
    conn.close()

def buscar_testes_nao_corrigidos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.tipo_teste, t.folha_candidato, c.nome as nome_candidato
        FROM testes t JOIN candidatos c ON t.candidato_id = c.id
        WHERE t.corrigido = 0
    """)
    return [dict(row) for row in cursor.fetchall()]

def buscar_modelo_por_tipo(tipo_teste):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modelos WHERE tipo_teste = ?", (tipo_teste,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def salvar_correcao(teste_id, dados_brutos, observacoes, analise):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE testes SET dados_brutos = ?, observacoes_avaliador = ?, analise_normativa = ?, corrigido = 1
        WHERE id = ?
    """, (json.dumps(dados_brutos), observacoes, analise, teste_id))
    conn.commit()
    conn.close()

def buscar_candidatos_com_testes_corrigidos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT c.*
        FROM candidatos c JOIN testes t ON c.id = t.candidato_id
        WHERE t.corrigido = 1
    """)
    return [dict(row) for row in cursor.fetchall()]

def buscar_testes_corrigidos_por_candidato(candidato_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM testes WHERE candidato_id = ? AND corrigido = 1", (candidato_id,))
    return [dict(row) for row in cursor.fetchall()]

def salvar_laudo(candidato_id, laudo, resultado):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE candidatos SET laudo_final = ?, resultado_final = ? WHERE id = ?", (laudo, resultado, candidato_id))
    conn.commit()
    conn.close()

def buscar_todos_candidatos_com_resultado():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, renach, resultado_final, escolaridade FROM candidatos WHERE resultado_final IS NOT NULL")
    return [dict(row) for row in cursor.fetchall()]
