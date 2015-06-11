from django import forms
from django.forms import ModelForm
from models import Game



class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={
		"name" : "log",
		"id" : "login-user",
		"class" : "form-control input",
		"size" : "20",
		"placeholder" : "Enter Username",
		"type" : "text",
	}))

	password = forms.CharField(widget=forms.TextInput(attrs={
		"name" : "Password",
		"id" : "login-password",
		"class" : "form-control input",
		"size" : "20",
		"placeholder" : "Password",
		"type" : "password",
	}))


class GameForm(ModelForm):
	class Meta:
		model = Game
		fields = '__all__'
		exclude = ['attendee_total','field_location_url']

		widgets = { 
			'date': forms.TextInput(attrs={
				"class" : "form-control",
				'id' : 'datepicker'
			}),
			'time': forms.TextInput(attrs={
				"class" : "form-control",
				'id' : 'timepicker',
				'value' : '3:00'
			}),
			'field_address': forms.TextInput(attrs={
				"class" : "form-control",
				'id' : 'fieldAddress' 
			}),
			'opponent': forms.TextInput(attrs={
				"class" : "form-control",
			}),
			'city': forms.TextInput(attrs={
				"class" : "form-control",
				'id' : 'city'
			}),
			'zip_code': forms.NumberInput(attrs={
				"class" : "form-control",
				'id' : 'zip'
			}),
			
    } 

