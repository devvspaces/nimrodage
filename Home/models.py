from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .utils import makeCode, create_slug

# Create your models here.
class Contact(models.Model):
	CLIENT_TYPE=(
		('N','New',),
		('E','Existing'),
	)
	MEETING_TYPE=(
		('G','Google/Internet search',),
		('R','Referral'),
		('O','Other'),
	)
	name = models.CharField(max_length=255)
	company = models.CharField(max_length=255, blank=True)
	email = models.EmailField(max_length=255, help_text='e.g. nimrodage@gmail.com')
	business_phone = models.CharField(max_length=16, help_text='format is +234-9033234234', blank=True)
	mobile_phone = models.CharField(max_length=16, help_text='format is +234-9033234234', blank=True)
	address = models.TextField(blank=True)
	state = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	client = models.CharField(choices=CLIENT_TYPE, max_length=1)
	meeting = models.CharField(choices=MEETING_TYPE, max_length=1, blank=True)
	phrase = models.CharField(max_length=255, help_text='What phrase did you search?', blank=True)
	referred = models.CharField(max_length=255, help_text='Who referred you?', blank=True)
	other = models.CharField(max_length=255, help_text='How did you hear about us?', blank=True)
	message = models.TextField()
	d_date = models.CharField(max_length=255, help_text='e.g., Next month, December 9th, ASAP, etc.', blank=True)
	s_date = models.DateTimeField(auto_now_add=True)
	uid = models.CharField(max_length=64, blank=True, editable=False)
	file_one = models.FileField(blank=True)
	file_two = models.FileField(blank=True)
	file_three = models.FileField(blank=True)
	file_four = models.FileField(blank=True)

	def __str__(self):
		return f'Contact {self.name}'

@receiver(post_save, sender=Contact)
def create_profile(sender, instance,created,**kwargs ):
	if created:
		instance.uid = makeCode()
		instance.save()

def _image_upload(instance, filename):
    return f'Industry/{instance.slug}/{filename}'

def _image_upload2(instance, filename):
    return f'Service/{instance.slug}/{filename}'

class Service(models.Model):
	name = models.CharField(max_length=225)
	data = models.TextField(blank=True)
	slug = models.CharField(max_length=225, blank=True, editable=False)
	image = models.ImageField(upload_to=_image_upload2)

	class Meta:
		ordering=['name']

	def __str__(self):
		return f'{self.name}'

class Industry(models.Model):
	name = models.CharField(max_length=225)
	data = models.TextField(blank=True)
	slug = models.CharField(max_length=225, blank=True, editable=False)
	image = models.ImageField(upload_to=_image_upload)

	class Meta:
		ordering=['name']
	def __str__(self):
		return f'{self.name}'

@receiver(pre_save, sender=Service)
def create_service(sender, instance, **kwargs):
	instance.slug = instance.name.replace(' ','_').lower()

@receiver(pre_save, sender=Industry)
def create_industry(sender, instance, **kwargs):
	create_service(sender, instance,**kwargs)