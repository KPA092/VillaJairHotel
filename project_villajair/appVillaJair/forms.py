from django import forms
from .models import Users, Bedrooms, Registers
from django.contrib.auth.forms import AuthenticationForm


#Registrar usuarios

class UserRegistrationForm(forms.ModelForm):
    check_in_date = forms.DateTimeField(label='Fecha de entrada', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out_date = forms.DateTimeField(label='Fecha de salida', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Users
        fields = ['nit', 'full_name', 'email', 'phone_number', 'country', 'age']
        labels = {
            'nit': 'Número de cédula',
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
        self.fields['age'].widget.attrs.update({'min': '18'})

        # Obtener solo los nombres de las habitaciones para el campo desplegable
        self.fields['bedroom'].choices = [(bedroom.id_bedroom, bedroom.bedroom_name) for bedroom in Bedrooms.objects.all()]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        bedroom_id = self.cleaned_data['bedroom']
        bedroom = Bedrooms.objects.get(id_bedroom=bedroom_id)
        check_in_date = self.cleaned_data['check_in_date']
        check_out_date = self.cleaned_data['check_out_date']
        Registers.objects.create(id_user=user, id_bedroom=bedroom, check_in_date=check_in_date, check_out_date=check_out_date)
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input'})
        self.fields['password'].widget.attrs.update({'class': 'input'})