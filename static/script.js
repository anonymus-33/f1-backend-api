function cargarDatos() {
    fetch('/api/live-data')
    .then(res => res.json())
    .then(data => {
        const cuerpo = document.getElementById('body-pilotos');
        cuerpo.innerHTML = '';
        data.pilotos.forEach(p => {
            cuerpo.innerHTML += `<tr>
                <td>${p.Position}</td>
                <td>${p.Abbreviation}</td>
                <td>${p.TeamName}</td>
            </tr>`;
        });
    });
}
setInterval(cargarDatos, 5000);
cargarDatos();