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

  // 🚀 FETCH al tuo backend online
fetch(`https://voyager-backend-85be.onrender.com/search?q=${encodeURIComponent(query)}`)
  .then(response => response.json())
    .then(results => {
      if (results.length === 0) {
        responseText.innerText = "Voya non ha trovato nulla. Tipico.";
        return;
      }

      results.forEach(r => {
        const card = document.createElement("div");
        card.className = "result-card";
        card.innerHTML = `<a href="${r.url}" target="_blank">${r.title}</a>`;
        resultsArea.appendChild(card);
      });

      responseText.innerText = `Ecco cosa ha trovato Voya:`;
    })
    .catch(error => {
      console.error("Errore nella ricerca:", error);
      responseText.innerText = "Voya ha avuto un crash mentale. Riprova.";
    });
}
const sidebar = document.getElementById("settingsSidebar");
const settingsBtn = document.getElementById("settingsBtn");

settingsBtn.addEventListener("click", () => {
  sidebar.classList.add("show");
});

function closeSidebar() {
  sidebar.classList.remove("show");
}

function saveSettings() {
  const settings = {
    theme: document.getElementById("themeSelect").value,
    language: document.getElementById("langSelect").value,
    stealth: document.getElementById("stealthMode").checked
  };
  localStorage.setItem("voyagerConfig", JSON.stringify(settings));
  closeSidebar();
}
