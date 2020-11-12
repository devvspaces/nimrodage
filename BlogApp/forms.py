from django import forms

from .models import Newsletter, Comment

class NewsletterForm(forms.Form):
	email = forms.EmailField()
	def clean_email(self):
		email = self.data.get('email')
		news = Newsletter.objects.filter(email=email)
		if news.exists() and news.first().verified:
			raise forms.ValidationError('This email has already been verified', code='verified_email')
		if news.exists():
			raise forms.ValidationError('This email already exists', code='existing_email')
		return email
	def save(self, commit=True):
		email = self.data.get('email')
		news = Newsletter.objects.filter(email=email)
		if news.exists():
			return news.first()
		else:
			new_email=Newsletter(email=email)
			if commit:
				new_email.save()
		return new_email

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name','email','comment',)