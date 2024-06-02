let dataTable
let dataTableIsInitialized = false

const dataTableOptions = {
	columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5, 6, 7] },
		{ orderable: false, targets: [7] },
		{ searchable: false, targets: [0, 5, 6, 7] }
	],
	pageLength: 8,
	destroy: true,
	language: {
		autoFill: {
			cancel: 'Cancelar',
			fill: 'Llenar',
			fillHorizontal: 'Llenar celdas horizontalmente',
			fillVertical: 'Llenar celdas verticalmente',
			info: 'Información'
		},
		buttons: {
			copy: 'Copiar',
			copySuccess: { _: 'Copiado con éxito', 1: 'Fila copiada con éxito' },
			copyTitle: 'Tabla Copiada',
			createState: 'Crear estado',
			pageLength: {
				_: 'ver %d filas',
				'-1': 'Ver todas las Filas',
				1: 'Ver una fila'
			},
			renameState: 'Renombrar',
			updateState: 'Actualizar',
			csv: 'CSV',
			excel: 'Excel',
			pdf: 'PDF',
			collection: 'Colección',
			colvis: 'Visibilidad Columna',
			colvisRestore: 'Restaurar Visibilidad',
			copyKeys:
				'Presione Inicio + C para copiar la información de la tabla. Para Cancelar hacer clic en este mensaje para o ESC',
			print: 'Imprimir',
			removeAllStates: 'Eliminar todos los estados',
			removeState: 'Eliminar',
			savedStates: 'Estados Guardados',
			stateRestore: 'Estado %d'
		},
		datetime: {
			months: {
				0: 'Enero',
				1: 'Febrero',
				10: 'Noviembre',
				11: 'Diciembre',
				2: 'Marzo',
				3: 'Abril',
				4: 'Mayo',
				5: 'Junio',
				6: 'Julio',
				7: 'Agosto',
				8: 'Septiembre',
				9: 'Octubre'
			},
			weekdays: {
				0: 'Dom',
				1: 'Lun',
				2: 'Mar',
				3: 'Mié',
				4: 'Jue',
				5: 'Vie',
				6: 'Sáb'
			},
			amPm: ['am', 'pm'],
			previous: 'Anterior',
			next: 'Siguiente',
			hours: 'Hora',
			minutes: 'Minuto',
			seconds: 'Segundo',
			unknown: 'Desconocido'
		},
		editor: {
			close: 'Cerrar',
			create: {
				button: 'Nuevo',
				submit: 'Crear',
				title: 'Crear nueva entrada'
			},
			edit: {
				button: 'Editar',
				submit: 'Actualizar',
				title: 'Editar Registro'
			},
			remove: {
				button: 'Borrar',
				submit: 'Borrar',
				title: 'Borrar',
				confirm: {
					_: 'Está seguro de eliminar %d registros',
					1: 'Está seguro de eliminar 1 registro'
				}
			},
			multi: {
				info:
					'Los elementos seleccionados contienen diferentes valores para esta entrada. Para editar y configurar todos los elementos de esta entrada en el mismo valor, haga clic o toque aquí, de lo contrario, conservar sus valores individuales.',
				noMulti: 'Múltiples valores',
				title: 'Valores múltiples',
				restore: 'Deshacer cambios'
			},
			error: { system: 'Ha ocurrido un error del sistema ( Más Información)' }
		},
		emptyTable: 'Tabla Vacía',
		infoEmpty: 'Sin información',
		lengthMenu: 'Entradas',
		loadingRecords: 'Cargando...',
		searchBuilder: {
			button: { _: 'Creador de búsquedas (%d)', 0: 'Creador de búsquedas' },
			clearAll: 'Quitar filtro',
			data: 'Datos',
			logicAnd: 'Y',
			logicOr: 'O',
			value: 'Valor',
			add: 'Agregar condición',
			condition: 'Condición',
			conditions: {
				date: {
					after: 'Después',
					before: 'Antes',
					between: 'Entre',
					empty: 'Vacío',
					equals: 'Igual',
					not: 'No',
					notBetween: 'No Entre',
					notEmpty: 'No Vacío'
				},
				number: {
					between: 'Entre',
					empty: 'Vacío',
					equals: 'Igual',
					gt: 'Mayor',
					gte: 'Mayor o Igual',
					lt: 'Menor',
					lte: 'Menor o Igual',
					not: 'No',
					notBetween: 'No Entre',
					notEmpty: 'No vacío'
				},
				string: {
					contains: 'Contiene',
					empty: 'Vacío',
					endsWith: 'Termina en',
					equals: 'Iguales',
					not: 'No',
					notEmpty: 'No Vacío',
					startsWith: 'Empieza en',
					notContains: 'No Contiene',
					notStartsWith: 'No empieza en',
					notEndsWith: 'No finaliza en'
				},
				array: {
					equals: 'Iguales',
					empty: 'Vacío',
					contains: 'Contiene',
					not: 'No',
					notEmpty: 'No Vacío',
					without: 'Con'
				}
			},
			deleteTitle: 'Eliminar regla',
			leftTitle: 'Izquierda',
			rightTitle: 'Derecha',
			title: { 0: 'Generador de Consultas', _: 'Generador de Consultas (%d)' }
		},
		searchPanes: {
			clearMessage: 'Borrar Filtro',
			collapseMessage: 'Desplegar todo',
			loadMessage: 'Cargando información',
			showMessage: 'Mostrar todos',
			title: 'Filtros Activos - %d',
			collapse: { 0: 'Paneles de Búsqueda', _: 'Paneles de Búsqueda (%d)' },
			count: 'Cuenta',
			countFiltered: 'Cuenta Filtro',
			emptyPanes: 'No hay información'
		},
		searchPlaceholder: 'Búsqueda en tabla',
		select: {
			cells: { _: '%d celdas seleccionadas', 1: '1 celda seleccionada' },
			columns: { _: '%d columnas seleccionadas', 1: '1 columna seleccionada' },
			rows: { 1: 'Fila seleccionada', _: 'Filas Seleccionadas' }
		},
		aria: {
			sortAscending: 'Activar para ordenar ascendente',
			sortDescending: 'Activar para ordenar descendente'
		},
		decimal: '.',
		infoFiltered: 'filtrado de _MAX_ entradas totales',
		infoThousands: ',',
		paginate: {
			first: 'Primero',
			last: 'Último',
			next: 'Siguiente',
			previous: 'Anterior'
		},
		processing: 'Procesando...',
		search: 'Buscar:',
		thousands: ',',
		zeroRecords: 'No se encontró información',
		stateRestore: {
			creationModal: {
				button: 'Crear',
				columns: {
					search: 'Búsqueda columnas',
					visible: 'Visibilidad de columna'
				},
				name: 'Nombre:',
				order: 'Ordenar',
				paging: 'Paginado',
				scroller: 'Posición desplazamiento',
				search: 'Buscar',
				searchBuilder: 'Generador de Consultas',
				select: 'Seleccionar',
				title: 'Crear Nuevo Estado',
				toggleLabel: 'Incluir:'
			},
			duplicateError: 'Ya existe un estado con este nombre',
			emptyError: 'El nombre no puede estar vacío',
			emptyStates: 'Estado sin Guardar',
			removeConfirm: 'Está seguro de eliminar el estado %d?',
			removeError: 'Error al eliminar el estado',
			removeJoiner: 'y',
			removeSubmit: 'Eliminar',
			removeTitle: 'Eliminar Estado',
			renameButton: 'Eliminar',
			renameLabel: 'Nuevo nombre para %s',
			renameTitle: 'Renombrar Estado'
		},
		info: 'Mostrando _START_ a _END_ de _TOTAL_ entradas',
		infoPostFix: ''
	}
}

const listUsersByMonth = async (year, month) => {
	try {
		if (month === '0') {
			await initDataTable()
			return
		}

		const response = await fetch(`/listarUsuariosPorMes/${year}/${month}/`)
		const data = await response.json()

		const filteredData = data.users

		// Limpiamos la tabla antes de agregar nuevas filas
		dataTable.clear()

		// Verificamos si hay usuarios para el mes seleccionado
		if (filteredData.length > 0) {
			// Agregamos las filas solo si hay usuarios
			filteredData.forEach((user, index) => {
				dataTable.row.add([
					index + 1,
					user.full_name,
					user.nit,
					user.email,
					user.phone_number,
					user.age,
					user.country,
					`<div class="btn-action">
                        <a href="#" class="btn btn-primary edit-user" data-id="${user.id_user}" data-bs-toggle="modal" data-bs-target="#editUserModal"><i class="fa-solid fa-user-pen"></i></a>
						<a href="#" class="btn btn-primary view-registers" data-id="${user.id_user}" onclick="viewHistory(${user.id_user})"><i class="fa-solid fa-eye"></i></a>                    </div>`
				])
			})
		}

		// Redibujamos la tabla
		dataTable.draw()

		assignEventListeners()
	} catch (ex) {
		alert(ex)
	}
}

const initDataTable = async () => {
	if (dataTableIsInitialized) {
		dataTable.destroy()
	}

	await listUsers()

	dataTable = $('#datatable-users').DataTable(dataTableOptions)
	dataTableIsInitialized = true
}

const listUsers = async () => {
	try {
		const response = await fetch('/listarTodosLosUsuarios/')
		const data = await response.json()

		const tableBody = document.getElementById('tablebody_users')
		tableBody.innerHTML = ''

		data.users.forEach((user, index) => {
			const row = `
                <tr>
                    <td>${index + 1}</td>
                    <td>${user.full_name}</td>
                    <td>${user.nit}</td>
                    <td>${user.email}</td>
                    <td>${user.phone_number}</td>
                    <td>${user.age}</td>
                    <td>${user.country}</td>
                    <td>
                        <div class="btn-action">
                            <a href="#" class="btn btn-primary edit-user" data-id="${
															user.id_user
														}" data-bs-toggle="modal" data-bs-target="#editUserModal"><i class="fa-solid fa-user-pen"></i></a>
														<a href="#" class="btn btn-primary view-registers" data-id="${
															user.id_user
														}" onclick="viewHistory(${
				user.id_user
			})"><i class="fa-solid fa-eye"></i></a>
                        </div>
                    </td>
                </tr>`
			tableBody.innerHTML += row
		})

		assignEventListeners()
	} catch (ex) {
		alert(ex)
	}
}
function viewHistory(userId) {
	window.location.href = `/historial/?user_id=${userId}`
}

function createRegister(userId) {
	window.location.href = `/create_register/?user_id=${userId}`
}

document
	.getElementById('editUserForm')
	.addEventListener('submit', async function (event) {
		event.preventDefault()
		await updateUser()
	})

$(document).ready(async () => {
	await listUsers()
})

/*editar usuario*/
const assignEventListeners = () => {
	document.querySelectorAll('.edit-user').forEach(button => {
		button.addEventListener('click', async function () {
			const userId = this.getAttribute('data-id')
			await loadUserData(userId)
		})
	})
}

const loadUserData = async userId => {
	try {
		const response = await fetch(`/get_user/${userId}/`)
		const user = await response.json()

		document.getElementById('editUserId').value = user.id
		document.getElementById('editFullName').value = user.full_name
		document.getElementById('editEmail').value = user.email
		document.getElementById('editPhoneNumber').value = user.phone_number
		document.getElementById('editAge').value = user.age
		document.getElementById('editCountry').value = user.country
	} catch (ex) {
		alert('Error loading user data: ' + ex)
	}
}

/*UPDATE USER*/
function getCookie(name) {
	const cookieValue = document.cookie.match(
		'(^|;)\\s*' + name + '\\s*=\\s*([^;]+)'
	)
	return cookieValue ? cookieValue.pop() : ''
}

document
	.getElementById('editUserForm')
	.addEventListener('submit', async function (event) {
		event.preventDefault()
		await updateUser()
	})

const updateUser = async () => {
	const userId = document.getElementById('editUserId').value
	const userData = {
		full_name: document.getElementById('editFullName').value,
		email: document.getElementById('editEmail').value,
		phone_number: document.getElementById('editPhoneNumber').value,
		age: document.getElementById('editAge').value,
		country: document.getElementById('editCountry').value
	}

	try {
		const response = await fetch(`/updateUser/${userId}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify(userData)
		})

		if (response.ok) {
			Swal.fire({
				title: '¡Éxito!',
				text: 'El usuario se actualizó correctamente',
				icon: 'success',
				confirmButtonText: 'Aceptar'
			}).then(result => {
				if (result.isConfirmed) {
					$('#editUserModal').modal('hide') // Oculta el modal de Bootstrap
					window.location.reload()
				}
			})
		} else {
			// Error al actualizar el usuario
			Swal.fire('Error', 'No se pudo actualizar el usuario.', 'error')
		}
	} catch (ex) {
		// Manejo de errores
		Swal.fire('Error', 'No se pudo actualizar el usuario.', 'error')
	}
}

const updateYearPicker = () => {
	const currentYear = new Date().getFullYear()
	const yearPicker = document.getElementById('yearPicker')
	const options = yearPicker.querySelectorAll('option')
	let yearExists = false
	options.forEach(option => {
		if (parseInt(option.value) === currentYear) {
			yearExists = true
		}
	})
	if (!yearExists) {
		const option = document.createElement('option')
		option.value = currentYear
		option.textContent = currentYear
		yearPicker.appendChild(option)
	}
	yearPicker.value = currentYear
}

$(document).ready(async () => {
	await initDataTable()
	updateYearPicker()
	$('#monthPicker').on('change', function () {
		const selectedMonth = $(this).val()
		const currentYear = new Date().getFullYear()
		listUsersByMonth(currentYear, selectedMonth)
	})
	setInterval(updateYearPicker, 60000)

	$('#downloadPDF').click(async function () {
		const selectedMonth = $('#monthPicker').val()

		// Verificar si se ha seleccionado "Todos"
		if (selectedMonth === '0') {
			const url = '/download_all_users_pdf/'
			$.get(url)
				.done(function () {
					window.location.href = url
				})
				.fail(function (xhr) {
					if (
						xhr.status === 400 &&
						xhr.responseJSON &&
						xhr.responseJSON.message === 'No hay registros'
					) {
						Swal.fire({
							icon: 'warning',
							title: 'No hay registros',
							text: 'No hay usuarios registrados',
							confirmButtonText: 'OK'
						})
					} else {
						Swal.fire({
							icon: 'error',
							title: 'Error',
							text: 'Ha ocurrido un error. Inténtalo de nuevo más tarde',
							confirmButtonText: 'OK'
						})
					}
				})
		} else {
			// Realizar la descarga del PDF para el mes seleccionado
			const url = '/descargar_pdf/?selected_month=' + selectedMonth
			$.get(url)
				.done(function () {
					window.location.href = url
				})
				.fail(function (xhr) {
					if (xhr.status === 400) {
						Swal.fire({
							icon: 'warning',
							title: 'No hay registros',
							text: 'Para el mes seleccionado',
							confirmButtonText: 'OK'
						})
					} else {
						Swal.fire({
							icon: 'error',
							title: 'Error',
							text: 'Ha ocurrido un error. Inténtalo de nuevo más tarde',
							confirmButtonText: 'OK'
						})
					}
				})
		}
	})
})