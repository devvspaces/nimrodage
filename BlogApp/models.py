from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, send_mass_mail
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


from .managers import PostManager
from .tokens import email_confirm_token

User = get_user_model()

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=225, unique=True)
	title_slug = models.CharField(max_length=225, blank=True)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	category = models.ForeignKey('BlogApp.Category', on_delete = models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	content = models.TextField(blank=True)
	likes = models.ManyToManyField('BlogApp.Likes', blank=True)
	views = models.ManyToManyField('BlogApp.Views', blank=True)
	draft = models.BooleanField(default=False)

	postadmin = PostManager()

	def get_absolute_url(self):
		return reverse('blog-detail', args=[self.title_slug])

	def __str__(self):
		return self.title.title()

	def count_likes(self):
		return self.likes.count()
	def count_views(self):
		return self.views.count()

class Category(models.Model):
	name = models.CharField(max_length=225)

	def __str__(self):
		return self.name.title()

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	name = models.CharField(max_length=225)
	email = models.EmailField(help_text='Your email is protected and not seen by any third party.')
	comment = models.TextField()
	date = models.DateTimeField(auto_now=True)
	has_reply = models.BooleanField(default=False, editable=False)
	reply = models.OneToOneField('BlogApp.Reply', on_delete=models.CASCADE, blank=True, null=True)

	def email_user(self, fail=True):
		message=render_to_string("Blog/new_reply.html",{
			'email_name': settings.EMAIL_NIMRODAGE,
			'name': self.name or self.email.split('@')[0],
			'comment': self.comment,
			'reply': self.reply.content,
			'post': self.post.title,
			'link': reverse('blog-detail', args=[self.post.title_slug]),
			'domain': settings.SITE_DOMAINX,
		})
		print(message)
		return send_mail('Nimrod Age Newsletter', message, settings.EMAIL_NIMRODAGE, [self.email], fail)

	class Meta:
		ordering=['-date']

	def __str__(self):
		return self.name

class Reply(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	date = models.DateTimeField(auto_now=True)

class Views(models.Model):
	viewer = models.CharField(max_length=225)

class Likes(models.Model):
	viewer = models.ForeignKey('BlogApp.Views', on_delete=models.CASCADE)

class Newsletter(models.Model):
	email = models.EmailField(unique=True)
	verified = models.BooleanField(default=False)

	def __str__(self):
		return self.email

	def new_email(self, fail=True):
		message=render_to_string("Blog/new_email.html",{
			'email_name': settings.EMAIL_NIMRODAGE,
			'name': self.email.split('@')[0],
		})
		return send_mail('Nimrod Age Newsletter', message, settings.EMAIL_NIMRODAGE, [self.email], fail)
	def email_user(self, subject, message, fail=True):
		return send_mail(subject, message, settings.EMAIL_NIMRODAGE, [self.email], fail)

class EmailMarketing(models.Model):
	subject = models.CharField(max_length=255)
	message = models.TextField()
	sents = models.ManyToManyField(Newsletter, related_name='Sents', blank=True)
	rejects = models.ManyToManyField(Newsletter, blank=True)
	amount = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.subject

	def email_lists(self):
		return Newsletter.objects.count()

	def count_sent(self):
		return self.sents.count()

	def count_reject(self):
		return self.rejects.count()

	def email_users(self, fail=True, only_verified=False):
		sending=[]
		results = Newsletter.objects.all()
		if only_verified:
			results = results.filter(verified=True)
		for user in results:
			message=render_to_string("Blog/newsletter_mail.html",{
				'email_name': settings.EMAIL_NIMRODAGE,
				'name': user.email.split('@')[0].title(),
				'message': self.message,
				'subject': self.subject,
			}),
			sent=send_mail(self.subject, message, settings.EMAIL_NIMRODAGE, [user.email], fail)
			if sent:
				self.sents.add(user)
			else:
				self.rejects.add(user)
			sending.append(sent)
		if results:
			self.amount += 1
			self.save()
		return sending


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance,**kwargs):
	instance.title_slug = instance.title.replace(' ','_').lower()

@receiver(post_save, sender=Views)
def create_like(sender, instance,created,**kwargs):
	if created:
		like = Likes.objects.create(viewer=instance)

@receiver(pre_save, sender=Comment)
def create_reply(sender, instance,**kwargs):
	if instance.reply:
		instance.has_reply=True
		instance.email_user()

@receiver(pre_save, sender=Newsletter)
def new_newsletter(sender, instance,**kwargs):
	if instance.verified:
		instance.new_email()
	else:
		uid=urlsafe_base64_encode(force_bytes(instance.pk))
		token=email_confirm_token.make_token(instance)
		subject=f"{instance.email.split('@')[0].title()} Nimrod Age Newsletter"
		message=render_to_string("Blog/activation_email.html",{
			'name': instance.email.split('@')[0].title(),
			"uid": uid,
			"token": token,
			"domain": settings.SITE_DOMAINX,
			'email_name': settings.EMAIL_NIMRODAGE,
		})
		sent=instance.email_user(subject,message)
		print(sent, '\n\n')
