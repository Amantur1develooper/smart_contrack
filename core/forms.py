from django import forms
from core.models import User
from .models import Contract

class UserForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, label='Изображение лица', widget=forms.FileInput(
        attrs={'accept': 'image/*', 'class': 'form-control'}))
    password_m = forms.ImageField(required=False, label='Изображение паспорта', widget=forms.FileInput(
        attrs={'accept': 'image/*', 'class': 'form-control'}))
    
    idpassword = forms.CharField(label='ID Password', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    firstname = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.ModelForm):        
    class Meta:
        model = User
        fields = ['email','image','idpassword', 'firstname', 'lastname', 'phone','password']
        

from django import forms
from .models import User  # Убедитесь, что импортировали модель User

class ContractForm(forms.Form):
    buyer = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    seller = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    item = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    payment_terms = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    delivery_terms = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    warranty = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    dispute_resolution = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    podpis1 = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    podpis2 = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

