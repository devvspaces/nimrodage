import random
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, CreateView, DetailView
from reviews.models import Reviews
from FAQ.models import Faq
from BlogApp.forms import NewsletterForm

# My local modules
from .forms import ContactForm
from .models import Service, Industry


class Index(TemplateView):
	template_name = 'Home/index.html'
	context_object_name = 'dexes'
	def get(self, request):
		return render(request, self.template_name, self.get_context_data())
	def post(self, request):
		context=self.get_context_data()
		form = NewsletterForm(request.POST)
		email=request.POST.get('email')
		if form.is_valid():
			news_mail=form.save()
			messages.success(self.request, f'Verify your email {news_mail.email} by clicking the link we sent to your mail to receive our updates')
		else:
			email_errors=''
			for i in form:
				for a in i.errors:
					email_errors+=a
					email_errors+='<br>'
			context['email'] = email
			context['email_errors'] = email_errors
		return render(request, self.template_name, context)
	def get_context_data(self):
		context = super(Index, self).get_context_data()
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		if self.template_name.find('certs') != -1:
			context['title']='Certs and Standards'
		elif self.template_name.find('safety') != -1:
			context['title']='Safety'
		elif self.template_name.find('needs') != -1:
			context['title']='Providing your needs'
		elif self.template_name.find('index') != -1:
			context['reviews'] = random.sample(list(Reviews.objects.all()),3)
			context['faqs']= random.sample(list(Faq.objects.all()),3)

		return context

class IndustryView(DetailView):
	template_name = 'Home/industry.html'
	context_object_name = 'industry'
	model = Industry

	def get_context_data(self, **kwargs):
		context = super(IndustryView, self).get_context_data()
		industry = self.get_object()
		context['title']=industry.name
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		return context

class ServiceView(DetailView):
	template_name = 'Home/service.html'
	context_object_name = 'service'
	model = Service

	def get_context_data(self, **kwargs):
		context = super(ServiceView, self).get_context_data()
		service = self.get_object()
		context['title']=service.name
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		return context

class ContactView(CreateView):
	template_name='Home/contact.html'
	form_class = ContactForm
	success_url = 'contact'
	def get(self, request):
		return render(request, self.template_name, self.get_context_data())
	def get_context_data(self):
		context={}
		context['title']='Contact Us'
		context['klass']='contactPage'
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		for i in self.get_form():
			txt = []
			for a in i.errors:
				txt.append(a)
			txt = '<br>'.join(txt)
			context[i.name+'_e'] = txt
			context[i.name+'_h'] = i.help_text
			context[i.name] = i.value()
		return context
	def form_valid(self, request):
		contact=self.get_form().save()
		messages.success(self.request, 'Your message has been delivered, you will get a reply soon')
		return redirect('contact')
	def form_invalid(self, request):
		return render(self.request, 'Home/contact.html', self.get_context_data())