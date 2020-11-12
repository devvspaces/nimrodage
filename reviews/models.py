from django.db import models

# Create your models here.

class Reviews(models.Model):
	company = models.CharField(max_length=225, unique=True)
	comment = models.TextField()
	services = models.ManyToManyField('Home.Service')

	def __str__(self):
		return f'Review {self.company}'
