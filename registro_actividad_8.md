El archivo `index.html` ha sido actualizado para agregar el formulario de creación de solicitudes y el script en JavaScript que consume la ruta GET `/solicitudes` para mostrar las publicaciones activas dinámicamente en pantalla.

Contenido del archivo `index.html`:

```html
<html>
  <head>
    <title>QuienLoTiene</title>
  </head>
  <body>
    <h1>Crear solicitud</h1>
    <form id='crear-solicitud'>
      <label for='titulo'>Título:</label><br>
      <input type='text' id='titulo' name='titulo'><br>
      <label for='descripcion'>Descripción:</label><br>
      <input type='text' id='descripcion' name='descripcion'><br>
      <button type='submit'>Crear</button>
    </form>
    <div id='solicitudes'></div>
    <script>
      const formulario = document.getElementById('crear-solicitud');
      formulario.addEventListener('submit', function(event) {
        event.preventDefault();
        const titulo = document.getElementById('titulo').value;
        const descripcion = document.getElementById('descripcion').value;
        fetch('/solicitudes', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ titulo: titulo, descripcion: descripcion }),
        })
       .then(response => response.json())
       .then(data => console.log(data))
       .catch(error => console.error('Error:', error));
      });

      fetch('/solicitudes')
     .then(response => response.json())
     .then(data => {
        const solicitudesDiv = document.getElementById('solicitudes');
        data.forEach(solicitud => {
          const solicitudHTML = `<p>Título: ${solicitud.titulo}</p><p>Descripción: ${solicitud.descripcion}</p>`;
          solicitudesDiv.insertAdjacentHTML('beforeend', solicitudHTML);
        });
      })
     .catch(error => console.error('Error:', error));
    </script>
  </body>
</html>
```