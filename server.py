from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
from langchain_experimental.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Configurazione della chiave API
load_dotenv()
key = os.environ.get("OPENAI_API_KEY")
# Inizializza il modello
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Crea agente
agent = create_csv_agent(llm, 'your_dataset.csv', verbose=True, allow_dangerous_code=True)

# Configura il server Flask
app = Flask(__name__)
CORS(app)  # Abilita CORS per consentire richieste cross-origin


@app.route('/')
def index():
    return jsonify({"message": "Server is running"})


@app.route('/query', methods=['POST'])
def query():
    try:
        # Ricezione domanda dall'utente
        user_question = request.json.get('question')
        
        # Esecuzione domanda sull'agente
        response = agent.run(user_question)
        
        # Risposta inviata al frontend
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
