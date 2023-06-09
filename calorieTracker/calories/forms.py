from .models import Food
from django import forms

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FoodForm(forms.Form):
    #kada bih mogla i neki search ubaciti
	#nisam models.Form stavljala jer bi to ponsitilo ovaj select
		optionsSelects=()
		for food in Food.objects.all():
			optionsSelects+=(str(food),str(food)),
		food = forms.ChoiceField(choices=optionsSelects)
		quantity=forms.IntegerField()
		food.widget.attrs.update({"class": "form-control"})
		quantity.widget.attrs.update({"class": "form-control"})
        
    
    
  

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super(UserCreationForm,self).__init__(*args, **kwargs)
		#fields je dictionary
		for name,field in self.fields.items():
			field.widget.attrs.update({'class':'form-control'})

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	
	
       