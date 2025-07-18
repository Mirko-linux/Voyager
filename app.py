import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.environ.get("NEWS_API_KEY")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"

    try:
        res = requests.get(url)
        data = res.json()

        results = []
        if data.get("AbstractURL") and data.get("AbstractText"):
            results.append({
                "title": data["Heading"],
                "url": data["AbstractURL"]
            })

        # fallback link if nothing else
        results.append({
            "title": f"Cerca {query} su DuckDuckGo",
            "url": f"https://duckduckgo.com/?q={query}"
        })

        return jsonify(results)

    except Exception as e:
        return jsonify([{"title": "Errore durante la ricerca", "url": ""}])
    
@app.route("/news")
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=it&apiKey={NEWS_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        articles = data.get("articles", [])[:6]  # Limita a 6 notizie

        results = []
        for a in articles:
            results.append({
                "title": a["title"],
                "url": a["url"],
                "image": a["urlToImage"] or "",
                "source": a["source"]["name"]
            })

        return jsonify(results)
    except Exception as e:
        return jsonify([])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # porta fissa o usa os.environ
