El archivo `index.html` ha sido actualizado con el código JavaScript que consume el endpoint GET `/solicitudes` y renderiza dinámicamente las publicaciones activas en tarjetas.

El contenido del archivo `index.html` es el siguiente:
```html
<html>
<head>
	<title>QuienLoTiene</title>
	<script>
		fetch('/solicitudes')
			.then(response => response.json())
			.then(data => {
				const solicitudesContainer = document.getElementById('solicitudes-container');
				data.forEach(solicitud => {
					const solicitudCard = document.createElement('div');
					solicitudCard.innerHTML = `
						<h2>${solicitud.title}</h2>
						<p>${solicitud.description}</p>
					`;
					solicitudesContainer.appendChild(solicitudCard);
				});
			});
	</script>
</head>
<body>
	<h1>QuienLoTiene</h1>
	<div id="solicitudes-container"></div>
</body>
</html>
```
Se ha creado un contenedor con el id `solicitudes-container` donde se renderizarán las tarjetas de las publicaciones activas. El código JavaScript utiliza la función `fetch` para consumir el endpoint GET `/solicitudes` y obtener la lista de publicaciones activas en formato JSON. Luego, se crea un elemento `div` para cada publicación y se agrega al contenedor `solicitudes-container`.

El archivo `index.html` ha sido modificado para que, al cargar la página, se muestren las publicaciones activas en tarjetas o una lista visual.