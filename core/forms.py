from django import forms
from .models import Patient, Doctor, PatientDoctorMapping
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'address']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'contact_number', 'email']

class MappingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from view
        super().__init__(*args, **kwargs)
        if user:
            # Restrict patient choices to those owned by the user
            self.fields['patient'].queryset = Patient.objects.filter(user=user)

    class Meta:
        model = PatientDoctorMapping
        fields = ['patient', 'doctor']