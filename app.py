from flask import Flask, render_template, request, redirect, url_for
import spacy
from database import init_db, salvar_comentario, obter_historico

app = Flask(__name__)

# Carrega o modelo de Processamento de Linguagem Natural (PLN) do spaCy em Português
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    import os
    os.system("python -m spacy download pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")

# Listas de apoio léxico para análise de polaridade baseada em termos (heurística ajustada para PLN)
PALAVRAS_POSITIVAS = {
    "bom", "ótimo", "excelente", "maravilhoso", "perfeito", "amei", "gostei", 
    "rápido", "eficiente", "recomendo", "satisfeito", "parabéns", "fantástico", 
    "qualidade", "adoramos", "feliz", "útil", "top"
}

PALAVRAS_NEGATIVAS = {
    "ruim", "péssimo", "horrível", "lento", "caro", "decepcionado", "problema", 
    "falha", "atrasado", "Péssimo", "odiei", "reclamar", "péssima", "horrível", 
    "ruim", "fraco", "pior", "nunca", "defeito"
}

def analisar_sentimento_spacy(texto):
    """
    Analisa o texto utilizando spaCy para lematização e filtragem de stopwords,
    calculando a polaridade com base em léxico especializado.
    """
    doc = nlp(texto.lower())
    
    score = 0
    tokens_analisados = 0

    for token in doc:
        # Ignora pontuações, espaços e stop words para focar nas palavras de conteúdo
        if not token.is_stop and not token.is_punct:
            lema = token.lemma_
            if lema in PALAVRAS_POSITIVAS:
                score += 1
                tokens_analisados += 1
            elif lema in PALAVRAS_NEGATIVAS:
                score -= 1
                tokens_analisados += 1

    # Classificação baseada no escore de polaridade
    if score > 0:
        sentimento = "Positivo"
    elif score < 0:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"
        
    return sentimento, float(score)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        texto_usuario = request.form.get("comentario", "").strip()
        
        if texto_usuario:
            sentimento, polaridade = analisar_sentimento_spacy(texto_usuario)
            salvar_comentario(texto_usuario, sentimento, polaridade)
            resultado = {
                "texto": texto_usuario,
                "sentimento": sentimento,
                "polaridade": polaridade
            }
            
    historico = obter_historico()
    return render_template("index.html", resultado=resultado, historico=historico)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)