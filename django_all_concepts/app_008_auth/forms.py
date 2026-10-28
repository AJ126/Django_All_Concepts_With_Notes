
from django import forms
from django.contrib.auth.models import User

class PasswordShowWidget(forms.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs.update({'class': 'form-control', 'id': 'password', 'placeholder': 'Enter password',})
        input_html = super().render(name, value, attrs, renderer)
        
        return forms.utils.mark_safe(
            '<div class="input-group">'
            f'{input_html}'
            '<button type="button" class="btn btn-outline-secondary" '
            'onclick="togglePassword()" aria-label="Show password">'
            '<i class="bi bi-eye" id="passwordIcon"></i>'
            '</button>'
            '</div>'
        )

        # return forms.utils.mark_safe(
        #     '<div class="input-group">'
        #     f'{input_html}'
        #     '<button type="button" class="btn btn-outline-secondary" '
        #     'onclick="togglePassword()"><i>&#xf06e;</i></button>'
        #     '</div>'
        # )

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username',
        'id': 'username'
    }))
    password = forms.CharField(widget=PasswordShowWidget())
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter first name',
        'id': 'first_name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter last name',
        'id': 'last_name'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address',
        'id': 'email'
    }))

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
