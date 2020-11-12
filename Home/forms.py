from django import forms
from django.core.validators import validate_email
from .models import Contact

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ('name','company','email',
			'business_phone','mobile_phone','address',
			'state','country','client','meeting','phrase',
			'referred','other','message','d_date','file_one','file_two','file_three','file_four',)
	def clean_email(self):
		email = self.cleaned_data.get('email')
		validate_email(email)
		return email
	def save(self, commit=False):
		contact = super(ContactForm, self).save(commit)
		if commit:
			contact.save()
		return contact