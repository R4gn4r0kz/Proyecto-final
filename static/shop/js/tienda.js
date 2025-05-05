document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/juegos/')
      .then(res => res.json())
      .then(data => {
        const grid = document.getElementById('game-grid');
        grid.innerHTML = '';  // limpia cualquier placeholder
  
        data.forEach(j => {
          // crea columna bootstrap
          const col = document.createElement('div');
          col.className = 'col-6 col-md-4 col-lg-3';
  
          col.innerHTML = `
            <div class="card h-100 shadow-sm">
              <img src="${j.cover}" class="card-img-top" alt="${j.titulo}">
              <div class="card-body d-flex flex-column">
                <h6 class="card-title text-truncate">${j.titulo}</h6>
                <p class="card-text text-truncate">${j.resumen}</p>
                <a href="/shop/juego/${j.id}/" class="btn btn-sm btn-primary mt-auto">
                  Jugar
                </a>
              </div>
            </div>`;
          grid.appendChild(col);
        });
      })
      .catch(err => console.error('Error cargando API de juegos:', err));
  });
  