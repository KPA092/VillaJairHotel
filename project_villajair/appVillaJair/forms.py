from django import forms
from .models import Users, Bedrooms, Registers, States
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone



DOCUMENT_TYPE_CHOICES = [
    ('CC', 'Cédula de Ciudadanía'),
    ('TI', 'Tarjeta de Identidad'),
    ('PP', 'Pasaporte'),
    ('CE', 'Cédula de Extranjería'),
]

class UserRegistrationForm(forms.ModelForm):
    check_in_date = forms.DateTimeField(label='Fecha de entrada', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out_date = forms.DateTimeField(label='Fecha de salida', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    document_type = forms.ChoiceField(label='Tipo de Documento', choices=DOCUMENT_TYPE_CHOICES)

    class Meta:
        model = Users
        fields = ['document_type', 'nit', 'full_name', 'email', 'phone_number', 'country', 'age']
        labels = {
            'document_type': 'Tipo de Documento',
            'nit': 'Número de Documento',
            'full_name': 'Nombre completo',
            'email': 'Correo electrónico',
            'phone_number': 'Número de teléfono',
            'country': 'País',
            'age': 'Edad',
        }

    bedroom = forms.ChoiceField(label='Habitación', choices=[])

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        placeholders = {
            'nit': 'Ingrese su número de cédula',
            'full_name': 'Ingrese su nombre completo',
            'email': 'Ingrese su correo electrónico',
            'phone_number': 'Ingrese su número de teléfono',
            'country': 'Ingrese su país',
            'age': 'Ingrese su edad',
        }
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')

        self.fields['phone_number'].widget.attrs.update({'type': 'tel'})
        self.fields['age'].widget.attrs.update()

        bedrooms_choices = [(bedroom.id_bedroom, bedroom.bedroom_name) for bedroom in Bedrooms.objects.filter(deleted_at__isnull=True)]
        self.fields['bedroom'].choices = [('', 'Seleccione una habitación')] + bedrooms_choices

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        document_type = cleaned_data.get('document_type')
        age = cleaned_data.get('age')

        # Verifica si la fecha de entrada es menor que la fecha de salida
        if check_in_date >= check_out_date:
            raise forms.ValidationError("La fecha de entrada debe ser anterior a la fecha de salida")

        # Verifica si la fecha actual está entre la fecha de entrada y salida
        if check_in_date <= timezone.now() <= check_out_date:
            cleaned_data['id_state'] = States.objects.get(id_state=1)
        else:
            cleaned_data['id_state'] = States.objects.get(id_state=2)

        # Verifica si el usuario está activo en este momento
        usuario_nit = cleaned_data.get('nit')
        usuario_activo = Users.objects.filter(nit=usuario_nit, id_state=1).exists()
        if usuario_activo:
            raise forms.ValidationError("Este Huesped en este momento ya se encuentra en el hotel")

        # Verifica si la habitación alcanzó su límite de personas activas
        bedroom_id = cleaned_data.get('bedroom')
        if bedroom_id:
            habitacion = Bedrooms.objects.get(pk=bedroom_id)

            # Verificar el estado de la habitación
            if habitacion.id_state_id == 5:
                raise forms.ValidationError("La habitación está en mantenimiento y no puede ser asignada.")

            usuarios_activos = Users.objects.filter(id_state=1, registers__id_bedroom=bedroom_id).count()

            if usuarios_activos >= habitacion.people_limit:
                raise forms.ValidationError("La habitación ya alcanzó su límite de personas activas")
            
         
            if usuarios_activos > 0:
                        habitacion.id_state = States.objects.get(id_state=3)  
            else:
                        habitacion.id_state = States.objects.get(id_state=4)  

                        habitacion.save()

        # Verifica si la edad es menor a 18 y el tipo de documento es cédula o cédula de extranjería
        if document_type in ['CC', 'CE'] and age < 18:
            raise forms.ValidationError("Los usuarios menores de 18 años no pueden registrarse con cédula o cédula de extranjería")

        if document_type in ['TI'] and age >= 18:
            raise forms.ValidationError("Los usuarios mayores de 18 años no pueden registrarse con tarjeta de identidad")
        return cleaned_data

    def save(self, commit=True):
        try:
            existing_user = Users.objects.get(nit=self.cleaned_data['nit'])
        except Users.DoesNotExist:
            # Si el usuario no existe, guarda el usuario y el registro
            user = super().save(commit=False)
            user.id_state = self.cleaned_data['id_state']
            user.save()

            bedroom_id = self.cleaned_data['bedroom']
            bedroom = Bedrooms.objects.get(id_bedroom=bedroom_id)
            check_in_date = self.cleaned_data['check_in_date']
            check_out_date = self.cleaned_data['check_out_date']
            Registers.objects.create(id_user=user, id_bedroom=bedroom, check_in_date=check_in_date, check_out_date=check_out_date)

            bedroom.update_room_status()  # Actualizar el estado de la habitación

            return user
        else:
            # Si el usuario ya existe, simplemente guarda el registro
            bedroom_id = self.cleaned_data['bedroom']
            bedroom = Bedrooms.objects.get(id_bedroom=bedroom_id)
            check_in_date = self.cleaned_data['check_in_date']
            check_out_date = self.cleaned_data['check_out_date']
            Registers.objects.create(id_user=existing_user, id_bedroom=bedroom, check_in_date=check_in_date, check_out_date=check_out_date)

            bedroom.update_room_status()  # Actualizar el estado de la habitación

            return existing_user

#Solo registros
class RegisterForm(forms.ModelForm):
    user_id = forms.IntegerField(required=True, widget=forms.HiddenInput())

    class Meta:
        model = Registers
        fields = ['check_in_date', 'check_out_date', 'id_bedroom']

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")
        id_bedroom = cleaned_data.get("id_bedroom")

        if check_in_date and check_out_date:
            if check_in_date >= check_out_date:
                raise forms.ValidationError("La fecha de entrada debe ser anterior a la fecha de salida.")
            
        if id_bedroom:
            habitacion = Bedrooms.objects.get(pk=id_bedroom.id_bedroom)  

            if habitacion.id_state_id == 5:
                raise forms.ValidationError("La habitación está en mantenimiento y no puede ser asignada.")

            usuarios_activos = Users.objects.filter(
                id_state=1, 
                registers__id_bedroom=id_bedroom
            ).count()

            if usuarios_activos >= habitacion.people_limit:
                raise forms.ValidationError("La habitación ya alcanzó su límite de personas activas")

        return cleaned_data

    def save(self, commit=True):
        registro = super().save(commit=False)
        user_id = self.cleaned_data.get('user_id')

        if user_id:
            try:
                user = Users.objects.get(pk=user_id)
                if user.id_state.state_name == 'Activo':
                    raise forms.ValidationError("Este Huesped en este momento ya se encuentra en el hotel")
                else:
                    registro.id_user = user
                    if registro.check_in_date <= timezone.now() <= registro.check_out_date:
                        user.id_state = States.objects.get(id_state=1)
                    else:
                        user.id_state = States.objects.get(id_state=2)

                    if commit:
                        user.save()
                        registro.save()
                        registro.id_bedroom.update_room_status()


            except Users.DoesNotExist:
                raise forms.ValidationError("User ID is invalid")
        else:
            raise forms.ValidationError("User ID is missing")

        return registro
     
#login
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input'})
