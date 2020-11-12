from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string


# Create your models here.
class Faq(models.Model):
	question = models.TextField()
	answer = models.TextField()
	date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering=('-date',)

	def __str__(self):
		return f'Question: {self.question[:20]}...?'

class NewQuestion(models.Model):
	name = models.CharField(max_length=225)
	email = models.EmailField()
	question = models.TextField()
	answer = models.TextField(blank=True)
	answered = models.BooleanField(default=False, blank=True)
	date = models.DateTimeField(auto_now=True)

	def email_user(self, fail=True):
		message=render_to_string("FAQ/faq_email.html",{
			"question": self.question,
			"answer": self.answer,
			'email_name': settings.EMAIL_NIMRODAGE,
			'name': self.name or self.email.split('@')[0],
		})
		return send_mail('Answer from Nimrod Age', message, settings.EMAIL_NIMRODAGE, [self.email], fail)

	def __str__(self):
		return f'Question: {self.question[:20]}...?'

@receiver(pre_save, sender=NewQuestion)
def update_question(sender, instance, **kwargs ):
	if len(instance.answer)>0:
		instance.answered = True
	else:
		instance.answered = False 
@receiver(post_save, sender=NewQuestion)
def update_faq(sender, instance, **kwargs):
	if len(instance.answer)>0:
		results = Faq.objects.filter(question__iexact = instance.question)
		if not results.exists():
			# Create new FAQ
			new_faq = Faq.objects.create(question=instance.question, answer=instance.answer)
			instance.email_user()
		else:
			result = results.first()
			if result.answer != instance.answer:
				# Mail new answer to person asking
				instance.email_user()
			result.answer=instance.answer
			result.save()