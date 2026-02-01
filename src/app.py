import os
import time
import streamlit as st
from dotenv import load_dotenv
from agent import portfolio_agent
from agents import Runner

# Chargement de l'environnement
load_dotenv()

st.set_page_config(page_title="Julien Forestier - Assistant Portfolio", layout="centered")

# --- FONCTIONS ---
def run_agent_query(query: str) -> str:
    result = Runner.run_sync(starting_agent=portfolio_agent, input=query)
    return result.final_output

def stream_text(text: str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# --- INTERFACE ---
def main():
    with st.sidebar:
        st.header("Contact")
        st.write("- [LinkedIn](https://www.linkedin.com/in/julien-forestier-2b3203313/)") 
        st.write("- [GitHub](https://github.com/JulienForestier16)") 
        st.write("- [Email](mailto:julien.forestier16@gmail.com)") 
        
        st.divider()
        # Bouton CV Permanent
        cv_path = "assets/CV Julien Forestier.pdf"
        if os.path.exists(cv_path):
            with open(cv_path, "rb") as f:
                st.download_button("📄 Télécharger mon CV", f, file_name="CV_Julien_Forestier.pdf")

    st.title("Assistant Portfolio - Julien Forestier")

    # Initialisation historique
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis l'assistant de Julien. Cliquez sur une suggestion ou posez-moi une question."}]

    # Affichage historique
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- BOUTONS DE SUGGESTIONS ---
    # On ne les affiche que si la conversation vient de commencer
    if len(st.session_state.messages) <= 1:
        st.write("### 💡 Suggestions")
        col1, col2, col3 = st.columns(3)
        
        # On définit une variable pour capturer le clic
        suggestion_query = None
        
        if col1.button("🎓 Formation & BUT SD"):
            suggestion_query = "Détaille ton parcours académique et ce que tu apprends en BUT Science des Données."
        
        if col2.button("💻 Projets & Stack Tech"):
            suggestion_query = "Quels sont tes projets techniques les plus marquants (R, Scala, Python) ?"
            
        if col3.button("🎯 Objectifs & Stage"):
            suggestion_query = "Quels sont tes objectifs professionnels et ton bilan après tes premières expériences ?"

        # Si un bouton est cliqué, on traite la requête
        if suggestion_query:
            process_query(suggestion_query)

    # Zone de saisie manuelle
    if query := st.chat_input("Votre question..."):
        process_query(query)

def process_query(query: str):
    """Fonction centralisée pour traiter une question (bouton ou texte)"""
    st.session_state.messages.append({"role": "user", "content": query})
    
    # On force l'affichage immédiat du message utilisateur avant la réponse
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("Recherche dans les documents..."):
            response = run_agent_query(query)
        
        full_text = ""
        for chunk in stream_text(response):
            full_text += chunk
            placeholder.markdown(full_text + "▌")
        placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

if __name__ == "__main__":
    main()