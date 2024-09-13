// Espera hasta que todo el contenido del DOM esté completamente cargado antes de ejecutar el código.
document.addEventListener('DOMContentLoaded', () => {
    // Selecciona el contenedor que tiene todas las imágenes del carrusel.
    const images = document.querySelector('.carousel-images'); 
    // Obtiene el botón para mover el carrusel hacia la izquierda (anterior).
    const prevButton = document.getElementById('prevButton');
    // Obtiene el botón para mover el carrusel hacia la derecha (siguiente).
    const nextButton = document.getElementById('nextButton');
    // Obtiene el ancho de una imagen dentro del carrusel. 
    // Esto se usa para calcular cuántos píxeles debe moverse el carrusel.
    const imageWidth = document.querySelector('.carousel-images img').clientWidth;
    // Inicializa el índice de la imagen actual visible. Comienza desde 0 (la primera imagen).
    let index = 0;

    // Función que actualiza la posición del carrusel moviendo las imágenes horizontalmente.
    function updateCarousel() {
        // Ajusta la posición del contenedor de imágenes para mostrar la imagen actual.
        // Se mueve el contenedor horizontalmente usando `translateX`.
        images.style.transform = `translateX(-${index * imageWidth}px)`;
    }
    // Evento que se ejecuta cuando el botón "anterior" es clicado.
    prevButton.addEventListener('click', () => {
        index = (index > 0) ? index - 1 : images.children.length - 1;
        updateCarousel();
    });
    // Evento que se ejecuta cuando el botón "siguiente" es clicado.
    nextButton.addEventListener('click', () => {
        index = (index < images.children.length - 1) ? index + 1 : 0;
        updateCarousel();
    });

    // Rotación automática del carrusel cada 3 segundos.
    setInterval(() => {
        nextButton.click(); // Simula un clic en el botón siguiente cada 3 segundos.
    }, 3000); // // Cambia la imagen cada 3 segundos.
});
