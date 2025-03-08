from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

#User Creation Form
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.USER_ROLES)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    is_admin = forms.BooleanField(required=False, label="Register as Admin")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_admin')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    class Meta: 
        model = get_user_model()

#User Edit form (Admin)
class UserEditForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=CustomUser.USER_ROLES,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    membership_status = forms.ChoiceField(
        choices=CustomUser.MEMBERSHIP_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role','membership_status', 'is_admin']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Add User Form (Admins)
class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'password']
        widgets = {
            'role': forms.Select(choices=CustomUser.USER_ROLES),
        }