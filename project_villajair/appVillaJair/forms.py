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

#Registrar usuarios
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

        self.fields['bedroom'].choices = [(bedroom.id_bedroom, bedroom.bedroom_name) for bedroom in Bedrooms.objects.filter(deleted_at__isnull=True)]

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        # Verifica si la fecha de entrada es menor que la fecha de salida
        if check_in_date >= check_out_date:
            raise forms.ValidationError("La fecha de entrada debe ser anterior a la fecha de salida")

        # Verifica si la fecha actual está entre la fecha de entrada y salida
        if check_in_date <= timezone.now() <= check_out_date:
            cleaned_data['id_state'] = States.objects.get(id_state=1)  
        else:
            cleaned_data['id_state'] = States.objects.get(id_state=2) 
        return cleaned_data
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ingresado ya esta registrado.")
        return email
    
        

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
            return user
        else:
            # Si el usuario ya existe, simplemente guarda el registro
            bedroom_id = self.cleaned_data['bedroom']
            bedroom = Bedrooms.objects.get(id_bedroom=bedroom_id)
            check_in_date = self.cleaned_data['check_in_date']
            check_out_date = self.cleaned_data['check_out_date']
            Registers.objects.create(id_user=existing_user, id_bedroom=bedroom, check_in_date=check_in_date, check_out_date=check_out_date)

    


#login
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input'})

