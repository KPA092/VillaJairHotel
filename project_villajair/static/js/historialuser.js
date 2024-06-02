let dataTable
let dataTablaIsInitialized = false

const urlParams = new URLSearchParams(window.location.search)
const userId = urlParams.get('user_id')

const dataTableOptions = {
	columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
		{ orderable: false, targets: [0] },
		{ searchable: false, targets: [0] }
	],
	pageLength: 6,
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

const listaRegistros = async userId => {
	try {
		const response = await fetch(`/listarRegistros/${userId}`)
		const data = await response.json()

		let content = ``
		data.registros.forEach((register, index) => {
			const checkInDate = moment
				.utc(register.check_in_date)
				.tz('America/Bogota')
				.format('YYYY-MM-DD HH:mm')
			const checkOutDate = moment
				.utc(register.check_out_date)
				.tz('America/Bogota')
				.format('YYYY-MM-DD HH:mm')
			content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${checkInDate}</td>
                    <td>${checkOutDate}</td>
                    <td>${register.bedroom_name}</td>
                </tr>
            `
		})
		tablebody_registers.innerHTML = content
	} catch (ex) {
		alert(ex)
	}
}

const initDataTable = async () => {
	if (dataTablaIsInitialized) {
		dataTable.destroy()
	}
	await listaRegistros(userId)

	dataTable = $('#datatable-registers').DataTable(dataTableOptions)

	dataTablaIsInitialized = true
}

window.addEventListener('load', async () => {
	await initDataTable()
})

document.addEventListener('DOMContentLoaded', function () {
	const form = document.getElementById('crearRegistroForm')
	form.addEventListener('submit', async function (event) {
		event.preventDefault()
		const formData = new FormData(form)

		try {
			const response = await fetch(form.action, {
				method: 'POST',
				body: formData
			})

			const data = await response.json()
			console.log(data)
			if (response.ok) {
				if (data.success) {
					await Swal.fire({
						icon: 'success',
						title: '¡Registro exitoso!',
						text: 'El usuario se ha registrado correctamente.'
					})
					await initDataTable()
				} else if (!data.success) {
					let errorMessages = Object.values(
						data.errors || { message: data.message }
					).join('\n')
					await Swal.fire({
						icon: 'error',
						title: '¡Error!',
						text: errorMessages
					})
				}
			} else if (data.errors) {
				let errorMessages = Object.values(data.errors).join('\n')
				await Swal.fire({
					icon: 'error',
					title: '¡Error!',
					text: errorMessages
				})
			}
		} catch (error) {
			await Swal.fire({
				icon: 'error',
				title: 'Error',
				text: 'Error al agregar el registro: ' + error.message
			})
		}
	})
})
