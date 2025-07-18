// script.js
function search() {
  const query = document.getElementById("searchBox").value;
  const responseText = document.getElementById("voyaResponse");
  const resultsArea = document.getElementById("results");
  resultsArea.innerHTML = "";

  if (!query.trim()) {
    responseText.innerText = "Non cercare nulla. Voya approva.";
    return;
  }

  responseText.innerText = `Voya sta cercando: "${query}"...`;

  // Simulazione risultati
  const results = [
    { title: "Cos'è Voyager?", url: "https://voyager-search.netlify.app/#cose" },
    { title: "La filosofia di Voya", url: "https://voyager-search.netlify.app/#voya" },
    { title: `Risultati per '${query}'`, url: `https://voyager-search.netlify.app/#search?q=${query}` }
  ];

  results.forEach(r => {
    const card = document.createElement("div");
    card.className = "result-card";
    card.innerHTML = `<a href="${r.url}" target="_blank">${r.title}</a>`;
    resultsArea.appendChild(card);
  });
}