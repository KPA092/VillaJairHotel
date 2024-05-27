document.addEventListener('DOMContentLoaded', function () {
	const form = document.getElementById('registroForm')
	form.addEventListener('submit', function (event) {
		event.preventDefault()
		const formData = new FormData(form)

		fetch('/registro/', {
			method: 'POST',
			body: formData
		})
			.then(response => {
				if (!response.ok) {
					throw new Error('La solicitud falló.')
				}
				return response.json()
			})
			.then(data => {
				if (data.success) {
					if (data.menor_de_edad) {
						Swal.fire({
							icon: 'warning',
							title: '¡Menor de edad!',
							text: 'Solicitar registro civil de nacimiento autenticado'
						}).then(() => {
							Swal.fire({
								icon: 'success',
								title: '¡Registro exitoso!',
								text: 'El usuario se ha registrado correctamente.'
							}).then(() => {
								window.location.href = '/registro/'
							})
						})
					} else {
						Swal.fire({
							icon: 'success',
							title: '¡Registro exitoso!',
							text: 'El usuario se ha registrado correctamente.'
						}).then(() => {
							window.location.href = '/registro/'
						})
					}
				} else if (data.documento_existente) {
					Swal.fire({
						title: '¡Número de documento existente!',
						text: '¿Desea agregar un nuevo registro al historial del usuario?',
						showCancelButton: true,
						confirmButtonText: 'Aceptar',
						cancelButtonText: 'Cancelar',
						confirmButtonColor: '#3085d6',
						cancelButtonColor: '#d33'
					}).then(result => {
						if (result.isConfirmed) {
							formData.append('add_to_history', 'true')
							fetch('/registro/', {
								method: 'POST',
								body: formData
							})
								.then(response => response.json())
								.then(data => {
									if (data.success) {
										Swal.fire({
											icon: 'success',
											title: '¡Registro agregado al historial!',
											text:
												'Se ha agregado un nuevo registro al historial del usuario.'
										}).then(() => {
											window.location.href = '/registro/'
										})
									} else if (data.errors) {
										let errorMessages = Object.values(data.errors).join('\n')
										Swal.fire({
											icon: 'error',
											title: '¡Error!',
											text: errorMessages
										})
									}
								})
								.catch(error => {
									console.error('Error:', error)
								})
						}
					})
				} else if (data.errors) {
					let errorMessages = Object.values(data.errors).join('\n')
					Swal.fire({
						icon: 'error',
						title: '¡Error!',
						text: errorMessages
					})
				}
			})
			.catch(error => {
				console.error('Error:', error)
			})
	})
})
