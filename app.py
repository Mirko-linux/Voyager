import os
import requests
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 🔐 Carica variabili
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")  # Inserisci la tua API Key qui

# 🔌 Connessione Elastic
ELASTIC_URL = "https://my-elasticsearch-project-f6e1a7.es.eu-west-1.aws.elastic.cloud:443"
es = Elasticsearch(ELASTIC_URL, api_key=ELASTIC_API_KEY)

app = Flask(__name__)
CORS(app)

# 🟢 Stato del backend
@app.route("/")
def home():
    return jsonify({"status": "Voyager backend attivo"})

# 🔍 Cerca articoli in Elasticsearch
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    try:
        res = es.search(index="voyager", query={
            "multi_match": {
                "query": query,
                "fields": ["title^3", "description", "tags"],
                "fuzziness": "AUTO"
            }
        })

        hits = res.get("hits", {}).get("hits", [])[:10]
        results = []
        for h in hits:
            source = h["_source"]
            results.append({
                "title": source.get("title", ""),
                "url": source.get("url", ""),
                "description": source.get("description", ""),
                "tags": source.get("tags", [])
            })

        return jsonify(results)

    except Exception as e:
        print("Errore in /search (Elastic):", e)
        return jsonify([{"title": "Errore durante la ricerca semantica", "url": ""}])

@app.route("/news")
def get_news():
    if not NEWS_API_KEY:
        return jsonify([{"title": "Chiave NewsAPI non trovata", "url": "", "image": "", "source": ""}])

    url = f"https://newsapi.org/v2/top-headlines?country=it&apiKey={NEWS_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        articles = data.get("articles", [])[:6]

        results = []
        for a in articles:
            results.append({
                "title": a.get("title", ""),
                "url": a.get("url", ""),
                "image": a.get("urlToImage", ""),
                "source": a.get("source", {}).get("name", "")
            })

        return jsonify(results)

    except Exception as e:
        print("Errore in /news:", e)
        return jsonify([])

# 🚀 Avvia il server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
