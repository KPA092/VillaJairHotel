from django import forms
from .models import Users, Bedrooms, Registers

class UserRegistrationForm(forms.ModelForm):
    check_in_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


    class Meta:
        model = Users
        fields = ['nit', 'full_name', 'email', 'phone_number', 'country', 'age']

    bedroom = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'type': 'tel'})
        self.fields['country'].widget.attrs.update({'placeholder': 'Enter your country'})
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
