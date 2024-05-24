document.addEventListener('DOMContentLoaded', function () {
    // Cambiar estado de habitacion
    document.querySelectorAll('.estado').forEach(item => {
        item.addEventListener('click', event => {
            const habitacionId = event.target.getAttribute('data-habitacion-id');
            document.getElementById('habitacionIdInput').value = habitacionId;
            console.log('ID de la habitación seleccionada:', habitacionId);
        });
    });

    const estadoForm = document.getElementById('estadoForm');
    if (estadoForm) {
        estadoForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(this);

            fetch('/guardar_cambios/', {
                method: 'POST',
                body: formData,
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Hubo un problema al enviar la solicitud.');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Respuesta del servidor:', data);
                    $('#exampleModal').modal('hide');
                    const habitacionElement = document.querySelector(`.estado[data-habitacion-id="${data.id_bedroom}"]`);
                    if (habitacionElement) {
                        habitacionElement.textContent = data.estado;
                        habitacionElement.classList = `estado ${data.estado.toLowerCase()} text-center mb-0`;
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }

    // Crear habitación
    const crearHabitacionForm = document.getElementById('crearHabitacionForm');
    if (crearHabitacionForm) {
        crearHabitacionForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const formData = new FormData(this);

            try {
                const respuesta = await fetch('/crear_habitacion/', {
                    method: 'POST',
                    body: formData
                });

                if (respuesta.ok) {
                    const datos = await respuesta.json();
                    Swal.fire({
                        icon: 'success',
                        title: '¡Habitación creada exitosamente!',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            $('#modalCreate').modal('hide');
                            window.location.reload();
                        }
                    });
                } else {
                    const errorData = await respuesta.json();
                    if (errorData.excede_tamano) {
                        Swal.fire({
                            icon: 'error',
                            title: '¡Error al crear la habitación!',
                            text: 'La imagen excede el tamaño máximo permitido.'
                        });
                    } else {
                        console.error('Error al crear la habitación:', respuesta.status);
                    }
                }
            } catch (error) {
                console.error('Error de red:', error);
            }
        });
    }

    // Eliminar habitación
    const botonesEliminarHabitacion = document.querySelectorAll('.btn-eliminar-habitacion');
    botonesEliminarHabitacion.forEach(boton => {
        boton.addEventListener('click', function () {
            const habitacionId = boton.getAttribute('data-habitacion-id');
            Swal.fire({
                title: '¿Estás seguro?',
                text: '¡No podrás revertir esto!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, eliminar'
            }).then((result) => {
                if (result.isConfirmed) {
                    eliminarHabitacion(habitacionId);
                }
            });
        });
    });

    async function eliminarHabitacion(habitacionId) {
        try {
            const respuesta = await fetch(`/eliminar_habitacion/${habitacionId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            if (respuesta.ok) {
                const data = await respuesta.json();
                Swal.fire({
                    icon: 'success',
                    title: '¡Habitación eliminada correctamente!',
                }).then(() => {
                    window.location.href = '/habitaciones/';
                });
            } else {
                throw new Error('Error al eliminar la habitación');
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message
            });
        }
    }

    // Función para obtener el valor de la cookie CSRF
    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }

    // Ir a detalle de cada habitación
    document.querySelectorAll('.habitacion-imagen').forEach(card => {
        card.addEventListener('click', function () {
            const habitacionId = card.getAttribute('data-habitacion-id');
            window.location.href = `/detalle_habitacion/${habitacionId}`;
        });
    });

    // Obtener id de la habitación
    const bedroomDiv = document.getElementById('id_bedroom');
    if (bedroomDiv) {
        const habitacionId = bedroomDiv.getAttribute('data-habitacion-id');

        // Editar habitación
        document.querySelectorAll('.btn-editar-habitacion').forEach(button => {
            button.addEventListener('click', function () {
                fetch(`/detalle_habitacionJson/${habitacionId}/`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('nombreHabitacion').value = data.bedroom_name;
                        document.getElementById('limitePersonas').value = data.people_limit;
                        if (data.photo_url) {
                            document.getElementById('fotoHabitacion').src = data.photo_url;
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching habitacion data:', error);
                        alert('Hubo un error al obtener los datos de la habitación.');
                    });
            });
        });
        const editarHabitacionForm = document.getElementById('editarHabitacionForm');
        if (editarHabitacionForm) {
            editarHabitacionForm.addEventListener('submit', function (e) {
                e.preventDefault();
                const formData = new FormData(this);

                fetch(`/update_habitacion/${habitacionId}/`, {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            if (data.excede_tamano) {
                                Swal.fire({
                                    icon: 'error',
                                    title: '¡Error al modificar la habitación!',
                                    text: 'La imagen excede el tamaño máximo permitido.'
                                });
                            } else {
                                console.error(data.error);
                                alert('Hubo un error al actualizar la habitación.');
                            }
                        } else {
                            const card = document.querySelector(`div[data-habitacion-id="${habitacionId}"]`).closest('.habitacion');
                            card.querySelector('.card-header').textContent = data.bedroom_name;
                            card.querySelector('.habitacion-imagen-individual img').src = data.photo_url;

                            Swal.fire({
                                icon: 'success',
                                title: '¡Habitación Modificada exitosamente!',
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    var modal = bootstrap.Modal.getInstance(document.getElementById('modalEdit'));
                                    modal.hide();
                                }
                            });
                        }
                    })
                    .catch(error => {
                        console.error(error);
                        alert('Hubo un error al actualizar la habitación.');
                    });
            });
        }
    }
})
