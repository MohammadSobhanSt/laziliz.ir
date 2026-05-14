from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about yourself...',
            'rows': 4
        }),
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio']


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about yourself (optional)...',
            'rows': 4
        }),
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'password']
   
    def clean_email(self):
        email = self.cleaned_data.get('email')
            
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
    
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

         
class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a confirmation field for better UX
        self.fields['confirm_delete'] = forms.BooleanField(
            required=True,
            label="Confirm deletion",
            widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        )