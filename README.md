# 🚀 Assistant Portfolio IA — Julien Forestier
 
> **🌐 Lien de l'application en ligne :** [Cliquez ici pour tester l'assistant](TON_LIEN_STREAMLIT_ICI)
> 
Ce projet est un assistant intelligent basé sur une architecture **RAG** (*Retrieval Augmented Generation*). Il permet d'interroger mon parcours et mes compétences de manière naturelle, en garantissant que les réponses sont fondées sur des documents réels.

## 🧠 Architecture Technique
L'application fonctionne selon un cycle en trois étapes :
1. **Ingestion** : Les documents Markdown sont découpés en segments (chunks) et transformés en vecteurs mathématiques.
2. **Stockage** : Ces vecteurs sont stockés dans une base de données **Upstash Vector** (Recherche Hybride).
3. **Récupération & Génération** : Lorsqu'une question est posée, l'agent récupère les segments les plus pertinents et utilise le modèle **Llama 3.3 (via Groq)** pour générer une réponse synthétique.

---

## ⚙️ Guide d'Installation

### 1. Préparation de l'environnement
Il est recommandé d'utiliser Python 3.12 ou 3.13.
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
