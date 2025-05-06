//static/core/js/v-index.js

document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('game-grid');

  function renderGames(games) {
    grid.innerHTML = '';
    if (games.length === 0) {
      grid.innerHTML = '<p class="text-center">No hay juegos en esta categoría.</p>';
      return;
    }
    games.forEach(j => {
      const col = document.createElement('div');
      col.className = 'col-md-4 col-sm-6';
      col.innerHTML = `
        <div class="card h-100 shadow-sm">
          <img src="${j.cover}" class="card-img-top" alt="${j.titulo}" loading="lazy">
          <div class="card-body">
            <h5 class="card-title">${j.titulo}</h5>
            <p class="card-text">${j.resumen}</p>
          </div>
        </div>`;
      grid.appendChild(col);
    });
  }

  function loadAllGames() {
    fetch('/api/juegos/')
      .then(r => r.json())
      .then(renderGames);
  }

  document.getElementById('all-games').addEventListener('click', loadAllGames);

  document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const catId = btn.getAttribute('data-cat-id');
      fetch(catId
        ? `/api/juegos/?categoria=${catId}`
        : '/api/juegos/'
      )
        .then(r => r.json())
        .then(renderGames);
    });
  });

  // Cargar todos al inicio
  loadAllGames();
});

