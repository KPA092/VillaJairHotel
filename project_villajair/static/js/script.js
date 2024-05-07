//Ejecutar función en el evento click
document.getElementById('btn_open').addEventListener('click', open_close_menu)

//Declaramos variables
var side_menu = document.getElementById('menu_side')
var btn_open = document.getElementById('btn_open')
var body = document.getElementById('body')
var log_out = document.getElementById('log_out_')

//Evento para mostrar y ocultar menú
function open_close_menu() {
	body.classList.toggle('body_move')
	side_menu.classList.toggle('menu__side_move')
	log_out.classList.toggle('log_out_container_move') // Agregar o eliminar clase al abrir/cerrar menú
}

//Si el ancho de la página es menor a 760px, ocultará el menú al recargar la página

if (window.innerWidth < 760) {
	body.classList.add('body_move')
	side_menu.classList.add('menu__side_move')
}

//Haciendo el menú responsive(adaptable)

window.addEventListener('resize', function () {
	if (window.innerWidth > 760) {
		body.classList.remove('body_move')
		side_menu.classList.remove('menu__side_move')
	}

	if (window.innerWidth < 760) {
		body.classList.add('body_move')
		side_menu.classList.add('menu__side_move')
	}
})

// // Scrip para moverse entre las secciones del menu
// var enlacesMenu = document.querySelectorAll('.options__menu a')
// // Asignar evento clic a cada enlace del menú
// enlacesMenu.forEach(function (enlace) {
// 	enlace.addEventListener('click', function (event) {
// 		// Prevenir el comportamiento predeterminado de los enlaces
// 		event.preventDefault()
// 		// Obtener el ID de la sección a mostrar desde el atributo href del enlace
// 		var seccionId = this.getAttribute('href').substring(1)
// 		// Mostrar la sección correspondiente
// 		mostrarSeccion(seccionId)
// 	})
// })

// function mostrarSeccion(seccionId) {
// 	// Ocultar todas las secciones
// 	var secciones = document.querySelectorAll('.seccion')
// 	secciones.forEach(function (seccion) {
// 		seccion.style.display = 'none'
// 	})
// 	// Mostrar la sección correspondiente al enlace seleccionado
// 	document.getElementById(seccionId).style.display = 'block'
// }
// // Por defecto, mostrar la sección de inicio al cargar la página
// window.onload = function () {
// 	mostrarSeccion('inicio')
// }

// // Clic del menu lateral
// document.addEventListener('DOMContentLoaded', function () {
// 	var optionsMenuLinks = document.querySelectorAll('.options__menu a')

// 	optionsMenuLinks.forEach(function (link) {
// 		link.addEventListener('click', function (event) {
// 			// Evitar el comportamiento predeterminado del enlace
// 			event.preventDefault()

// 			// Eliminar la clase "selected" de todos los enlaces
// 			optionsMenuLinks.forEach(function (link) {
// 				link.classList.remove('selected')
// 			})

// 			// Agregar la clase "selected" solo al enlace clicado
// 			this.classList.add('selected')
// 		})
// 	})
// })
