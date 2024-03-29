from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import * 


class signupform(UserCreationForm):
    password1= forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    #first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=32, help_text='First name')
    #last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=32, help_text='Last name')
 
    #email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=64, help_text='Enter a valid email address')

    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={'first_name':'First Name','last_name':'Last Name','email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }


class loginform(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class addsubject(forms.ModelForm):  
    class Meta:  
        model = Category  
        fields = ['name','slug']  
        labels = {
            'name': _('Subject Name'),
            'slug': _('Unique Code'),
        }
        

        