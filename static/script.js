// Variable global para almacenar la sesión actual, empezamos sin nada
let sesionActual = null; 

function cargarDatos(tipoSesion) {
    sesionActual = tipoSesion;
    console.log(`Cargando datos para: ${tipoSesion}...`);
    
    // Mostramos un mensaje de carga mientras responde la API
    const cuerpo = document.getElementById('body-pilotos');
    cuerpo.innerHTML = '<tr><td colspan="4">Cargando datos de ' + tipoSesion + '...</td></tr>';
    
    fetch(`/api/live-data/${tipoSesion}`)
    .then(res => res.json())
    .then(data => {
        cuerpo.innerHTML = ''; // Limpiamos el mensaje de carga

        if (data.pilotos && data.pilotos.length > 0) {
            data.pilotos.forEach(p => {
                const fila = `<tr>
                    <td>${p.Position || '-'}</td>
                    <td>${p.Abbreviation}</td>
                    <td>${p.TeamName}</td>
                    <td>${p.FullName}</td>
                </tr>`;
                cuerpo.innerHTML += fila;
            });
        } else {
            cuerpo.innerHTML = '<tr><td colspan="4">No hay datos para esta sesión.</td></tr>';
        }
    })
    .catch(err => {
        console.error("Error:", err);
        cuerpo.innerHTML = '<tr><td colspan="4">Error de conexión.</td></tr>';
    });
}

// Ya no llamamos a cargarDatos() al inicio para que no cargue nada por defecto