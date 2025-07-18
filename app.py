from flask import Flask, request, jsonify
from flask_cors import CORS  # Permette richieste da altri domini (es. Netlify frontend)

app = Flask(__name__)
CORS(app)  # Abilita CORS per sviluppo frontend separato

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    
    # Risultati simulati con link reali al sito Netlify
    fake_results = [
        {"title": "Cos'è Voyager?", "url": "https://voyager-search.netlify.app/#cose"},
        {"title": "La filosofia di Voya", "url": "https://voyager-search.netlify.app/#voya"},
        {"title": f"Risultati per '{query}'", "url": f"https://voyager-search.netlify.app/#search?q={query}"}
    ]
    
    return jsonify(fake_results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)