// Mostrar productos del carrito
function mostrarCarrito() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let listaCarrito = document.getElementById('listaCarrito');
    let total = document.getElementById('total');
    listaCarrito.innerHTML = ''; // Limpiar lista
    let totalPrecio = 0;

    // Si el carrito está vacío
    if (carrito.length === 0) {
        listaCarrito.innerHTML = '<li class="list-group-item">El carrito está vacío</li>';
    } else {
        // Recorrer productos del carrito
        carrito.forEach((producto, index) => {
            // Crear el elemento principal (li)
            let item = document.createElement('li');
            item.classList.add('list-group-item');

            // Crear contenedor para nombre y precio
            let itemInfo = document.createElement('div');
            itemInfo.classList.add('item-info');
            itemInfo.innerHTML = `<p>${producto.nombre}</p><p>CLP$ ${producto.precio.toLocaleString('es-CL')}</p>`;

            // Crear botón "Eliminar"
            let btnEliminar = document.createElement('button');
            btnEliminar.classList.add('btn', 'btn-danger', 'btn-sm');
            btnEliminar.textContent = 'X';
            btnEliminar.onclick = () => eliminarDelCarrito(index); // Eliminar al hacer click

            // Insertar info y botón al item
            item.appendChild(itemInfo);
            item.appendChild(btnEliminar);

            // Agregar item a la lista del carrito
            listaCarrito.appendChild(item);

            // Sumar al total
            totalPrecio += producto.precio;
        });
    }

    // Mostrar el total actualizado
    total.textContent = `Total: CLP$ ${totalPrecio.toLocaleString('es-CL')}`;
}

// Eliminar un ítem del carrito
function eliminarDelCarrito(index) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito.splice(index, 1); // Elimina por posición
    localStorage.setItem('carrito', JSON.stringify(carrito));
    mostrarCarrito(); // Refrescar vista
}

// Vaciar el carrito completamente (btn)
document.getElementById('vaciarCarrito').addEventListener('click', function () {
    localStorage.removeItem('carrito'); // Elimina del storage
    mostrarCarrito(); // Refresca vista
});

// Agregar un producto al carrito
function agregarAlCarrito(nombre, precio) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito.push({ nombre, precio });
    localStorage.setItem('carrito', JSON.stringify(carrito));
    alert(`${nombre} agregado al carrito.`);

    // Mostrar dinamita (reinicia animación)
    const dinamita = document.getElementById('dinamita');
    dinamita.style.display = 'block';
    const img = dinamita.querySelector('img');
    img.src = img.src;
}

// Mostrar carrito al cargar la página
mostrarCarrito();
