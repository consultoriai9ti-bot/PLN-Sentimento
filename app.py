from deep_translator import GoogleTranslator
import streamlit as st
from textblob import TextBlob

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Analisador de Sentimentos Offline", page_icon="📊", layout="centered"
)

# Título e Explicação
st.title("📊 Analisador de Sentimentos Offline")
st.markdown(
    "Esta é uma versão **Offline** que utiliza bibliotecas tradicionais de Python "
    "(`TextBlob` e `deep-translator`) para processar o texto localmente, "
    "sem depender de APIs externas como OpenAI ou Google Gemini."
)

st.divider()

# Área de texto para entrada do usuário
texto_usuario = st.text_area(
    "Digite sua frase ou texto para análise:",
    placeholder="Ex: Eu adorei este aplicativo, ele é simplesmente fantástico!",
    height=150,
)

# Botão de análise
if st.button("Analisar Sentimento", type="primary"):
    if not texto_usuario.strip():
        st.warning(
            "Por favor, digite algum texto antes de clicar em Analisar."
        )
    else:
        with st.spinner("Processando tradução e análise de sentimentos..."):
            try:
                # 1. Tradução invisível para o inglês (já que o TextBlob é otimizado para EN)
                # O GoogleTranslator detecta automaticamente o idioma de origem
                traducao = GoogleTranslator(
                    source="auto", target="en"
                ).translate(texto_usuario)

                # 2. Análise de polaridade com TextBlob
                blob = TextBlob(traducao)
                polaridade = blob.sentiment.polarity
                subjetividade = blob.sentiment.subjectivity

                # 3. Classificação baseada na polaridade (-1.0 a 1.0)
                if polaridade > 0.05:
                    sentimento = "Positivo"
                    cor_alerta = "success"
                elif polaridade < -0.05:
                    sentimento = "Negativo"
                    cor_alerta = "error"
                else:
                    sentimento = "Neutro"
                    cor_alerta = "warning"

                # Exibição dos resultados visuais
                st.subheader("Resultado da Análise:")

                if cor_alerta == "success":
                    st.success(
                        f"**Sentimento:** {sentimento} (Polaridade: {polaridade:.2f})"
                    )
                elif cor_alerta == "error":
                    st.error(
                        f"**Sentimento:** {sentimento} (Polaridade: {polaridade:.2f})"
                    )
                else:
                    st.warning(
                        f"**Sentimento:** {sentimento} (Polaridade: {polaridade:.2f})"
                    )

                # Informações adicionais (métricas)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Polaridade (-1 a 1)", value=f"{polaridade:.2f}"
                    )
                with col2:
                    st.metric(
                        label="Subjetividade (0 a 1)",
                        value=f"{subjetividade:.2f}",
                    )

                with st.expander("Ver detalhes técnicos (Texto traduzido)"):
                    st.write(f"**Texto Original:** {texto_usuario}")
                    st.write(f"**Texto Traduzido (EN):** {traducao}")

            except Exception as e:
                st.error(
                    f"Ocorreu um erro durante o processamento: {str(e)}"
                )

# Rodapé informativo
st.markdown("---")
st.caption(
    "Desenvolvido com Python, Streamlit, TextBlob e deep-translator. Pronto para "
    "hospedagem no GitHub com Licença MIT."
)
