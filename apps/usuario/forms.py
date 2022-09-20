from django import forms
from .models import User
import re 
from django.utils.translation import gettext as _

class SetPasswordForm(forms.Form):

    new_password1 = forms.CharField(label = "Nueva Contraseña", widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label = "Confirmar Contraseña", widget = forms.PasswordInput(attrs={'class': 'form-control'}))
       
    def clean_new_password1(self):        
        sf_error1 =  forms.ValidationError( _("La contraseña es muy corta. Debe contener al menos 6 caracteres."), code='password_too_short',)
        sf_error2 =  forms.ValidationError( _("La contraseña debe ser alfanumérica."), code='password_isalnum', )        
        sf_error3 =  forms.ValidationError( _("La contraseña no debe contener espacios."), code='password_spaces', )
        sf_errors = [sf_error1,sf_error2,sf_error3]                 

        password = self.cleaned_data['new_password1']
        if len(password) < 6:
            raise forms.ValidationError(sf_errors)
        if password.isalpha()  or password.isdigit() :
            raise forms.ValidationError(sf_errors)  
        if re.search(' ',password)  is not None:
            raise forms.ValidationError(sf_errors)
        return password
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError( _("The two password fields didn't match."), code='password_mismatch',)
        return password2
