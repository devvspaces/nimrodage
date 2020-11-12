from django import forms
from .models import NewQuestion

class NewQuestionForm(forms.ModelForm):
	class Meta:
		model = NewQuestion
		fields = ('name','email','question',)