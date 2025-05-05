//static/core/js/v-index.js

document.addEventListener('DOMContentLoaded', () => {
  let allGames = [];

  // 1) Carga inicial de 15 juegos (sin filtrar)
  async function fetchGames(categoria = '') {
    const url = new URL('/api/juegos/', window.location.origin);
    url.searchParams.set('limit', 15);
    if (categoria) url.searchParams.set('categoria', categoria);

    try {
      const res = await fetch(url);
      const data = await res.json();
      allGames = categoria ? data : data;  // opcionalmente podrías cachear sólo el "todos"
      renderGames(data);
    } catch (err) {
      console.error('Error cargando juegos:', err);
      document.getElementById('game-grid')
        .innerHTML = '<p class="text-danger">No se pudieron cargar los juegos.</p>';
    }
  }

  // 2) Renderizado de tarjetas
  function renderGames(juegos) {
    const grid = document.getElementById('game-grid');
    grid.innerHTML = '';

    if (juegos.length === 0) {
      grid.innerHTML = '<p class="text-center">No hay juegos en esta categoría.</p>';
      return;
    }

    juegos.forEach(j => {
      const col = document.createElement('div');
      col.className = 'col-6 col-md-4 col-lg-3';
      col.innerHTML = `
        <div class="card h-100 shadow-sm">
          <img src="${j.cover}" class="card-img-top" alt="${j.titulo}" loading="lazy">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title text-truncate">${j.titulo}</h5>
            <p class="card-text text-truncate">${j.resumen}</p>
            <a href="/shop/juego/${j.id}/" class="btn btn-primary btn-sm mt-auto">
              Jugar
            </a>
          </div>
        </div>`;
      grid.appendChild(col);
    });
  }

  // 3) Enlazar eventos de los botones
  document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const catId = btn.dataset.catId;
      fetchGames(catId);
    });
  });

  document.getElementById('all-games').addEventListener('click', () => {
    fetchGames();  // sin categoría => todos
  });


});
