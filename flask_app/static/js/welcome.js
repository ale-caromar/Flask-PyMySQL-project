// Define la clase Welcome que extiende React.Component
class Welcome extends React.Component {
    // Constructor del componente
    constructor() {
        super(); // Llama al constructor de la clase base
        this.state = { show: true }; // Inicializa el estado con show en true
    }

    // Método que se ejecuta después de que el componente se ha montado en el DOM
    componentDidMount() {
        // Configura un temporizador para ocultar el mensaje después de 6 segundos
        setTimeout(() => {
            this.setState({ show: false }); // Cambia el estado a false para dejar de mostrar
        }, 6000); // Tiempo en milisegundos
    }

    // Método de renderizado
    render() {
        // Si el estado show es falso, no renderiza nada
        if (!this.state.show) return null;

        // Renderiza el contenido del componente
        return React.createElement(
            'div', // Crea un div principal para el mensaje de bienvenida
            { className: 'welcome-message' }, // Clase CSS para el contenedor
            // Mensaje de bienvenida
            React.createElement(
                'h1', // Encabezado de nivel 1
                null, // No se pasan props
                '¡Bienvenido!' // Texto del encabezado
            ),
            React.createElement(
                'h2', // Encabezado de nivel 2
                null, // No se pasan props
                'Estos son nuestros servicios' // Texto del encabezado
            ),
            // Div para los iconos de servicios
            React.createElement(
                'div', // Crea un div para contener los iconos
                { className: 'welcome-icons' }, // Clase CSS para el contenedor de iconos
                // Icono de gestión de agenda
                React.createElement(
                    'div', // Div para el icono de gestión de agenda
                    { className: 'icon' }, // Clase CSS para el icono
                    React.createElement('i', { className: 'fas fa-calendar-alt' }), // Icono
                    React.createElement('p', null, 'Gestión de agenda') // Descripción del servicio
                ),
                // Icono de pacientes
                React.createElement(
                    'div', // Div para el icono de pacientes
                    { className: 'icon' }, // Clase CSS para el icono
                    React.createElement('i', { className: 'fas fa-user-friends' }), // Icono
                    React.createElement('p', null, 'Pacientes') // Descripción del servicio
                ),
                // Icono de historia clínica
                React.createElement(
                    'div', // Div para el icono de historia clínica
                    { className: 'icon' }, // Clase CSS para el icono
                    React.createElement('i', { className: 'fas fa-file-alt' }), // Icono
                    React.createElement('p', null, 'Historia clínica') // Descripción del servicio
                )
            )
        );
    }
}

// Renderiza el componente Welcome en el DOM
document.addEventListener('DOMContentLoaded', function () {
    // Busca el contenedor donde se renderizará el componente
    const reactContainer = document.getElementById('react-dashboard');
    if (reactContainer) {
        // Renderiza el componente Welcome dentro del contenedor encontrado
        ReactDOM.render(
            React.createElement(Welcome), // Crea una instancia del componente Welcome
            reactContainer // Especifica el contenedor en el DOM
        );
    }
});
