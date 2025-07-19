import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
print ("NEWS_API_KEY:", NEWS_API_KEY)   # Debug: verifica se la chiave è caricata correttamente

@app.route("/")
def home():
    return jsonify({"status": "Voyager backend attivo"})

@app.route("/search")
def search():
    query = request.args.get("q", "")
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"

    try:
        res = requests.get(url)
        data = res.json()

        results = []

        # Abstract principale se presente
        if data.get("AbstractURL") and data.get("AbstractText"):
            results.append({
                "title": data["Heading"],
                "url": data["AbstractURL"]
            })

        # RelatedTopics fino a 5 risultati
        for topic in data.get("RelatedTopics", [])[:5]:
            if isinstance(topic, dict):
                if "Text" in topic and "FirstURL" in topic:
                    results.append({
                        "title": topic["Text"],
                        "url": topic["FirstURL"]
                    })
                elif "Topics" in topic:  # se è un gruppo
                    for sub in topic["Topics"][:3]:
                        if "Text" in sub and "FirstURL" in sub:
                            results.append({
                                "title": sub["Text"],
                                "url": sub["FirstURL"]
                            })

        # Fallback finale
        if not results:
            results.append({
                "title": f"Cerca {query} su DuckDuckGo",
                "url": f"https://duckduckgo.com/?q={query}"
            })

        return jsonify(results)

    except Exception as e:
        print("Errore in /search:", e)
        return jsonify([{"title": "Errore durante la ricerca", "url": ""}])
    
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
