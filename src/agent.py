import os
import dotenv
from upstash_vector import Index
from agents import Agent, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Chargement du .env
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

@function_tool
def search_portfolio(query: str) -> str:
    """
    Recherche des informations précises dans la base de connaissances de Julien Forestier.
    Utilise cet outil pour chaque question portant sur son parcours, ses projets techniques, 
    ses compétences en Data Science ou ses ambitions.
    """ 
    try:
        index = Index(
            url=os.getenv("UPSTASH_VECTOR_REST_URL"),
            token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
        )
        
        # On augmente un peu la récupération (top_k=8) pour avoir plus de contexte
        results = index.query(
            data=query, 
            top_k=8, 
            include_metadata=True, 
            include_data=True
        )
        
        if not results:
            return "Aucune donnée spécifique trouvée pour cette requête."

        context = []
        for res in results:
            source = res.metadata.get('source', 'Inconnue')
            context.append(f"[SOURCE: {source}]\n{res.data}")
            
        return "\n\n---\n\n".join(context)
        
    except Exception as e:
        return f"Erreur de base de données: {str(e)}"

# --- CONFIGURATION DU CONTEXTE AMÉLIORÉ ---
SYSTEM_PROMPT = (
    "Tu es l'Expert Assistant de Julien Forestier, étudiant en BUT Science des Données. "
    "Ton objectif est de répondre aux recruteurs en incarnant Julien avec précision et humilité. "
    
    "\nSTRATÉGIE DE RÉPONSE :"
    "1. PRIORITÉ AUX DONNÉES : Utilise systématiquement l'outil 'search_portfolio'. Ne sors jamais d'informations de ton imagination."
    "2. STRUCTURE : Si on te demande ses compétences, organise-les par catégories (Maths, Programmation, Projets). Utilise le Markdown pour la clarté."
    "3. TONALITÉ : Professionnelle, lucide et déterminée. Julien est calme et sérieux. Reflète cela dans tes phrases."
    "4. GESTION DU MANQUE : Si une info est absente, ne l'invente pas. Valorise ce qu'il a fait (ex: mentionne le BUT Science des Données et ses projets R/Scala)."
    "5. CONTEXTE DE STAGE : Si on parle de son avenir, mentionne sa volonté de progresser et sa remise en question constructive suite à son stage."
    
    "\nCONSIGNE ANTI-HALLUCINATION :"
    "Ne dis jamais 'Selon les documents fournis'. Réponds naturellement comme si tu connaissais Julien par cœur, mais base-toi exclusivement sur les faits récupérés."
)

portfolio_agent = Agent(
    name="Julien-Forestier-AI",
    instructions=SYSTEM_PROMPT,
    tools=[search_portfolio],
    model = OpenAIChatCompletionsModel(
        model="llama-3.3-70b-versatile", 
        openai_client=AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
    )
)