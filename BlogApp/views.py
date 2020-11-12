from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import ListView, DetailView

from .forms import NewsletterForm, CommentForm
from .models import Post, Views, Likes, Category, Newsletter
from .utils import createViewer
from .tokens import email_confirm_token

from Home.models import Service, Industry


def activate_email(request, uidb64, token):
	template_name = 'Blog/activation_error.html'
	if request.method != 'POST':
		try:
			uid=force_text(urlsafe_base64_decode(uidb64))
			email=Newsletter.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, Newsletter.DoesNotExist):
			email=None
		if email!=None and email_confirm_token.check_token(email,token):
			email.verified=True
			email.save()
			messages.success(request,f'Your email {email.email} is successfully suscribed to our newsletter. Thanks for registering with our service.')
			return redirect('index')
		else:
			return render(request, template_name)
	context={'title': 'Newsletter Activation Error'}
	form = NewsletterForm(request.POST)
	email=request.POST.get('email')
	if form.is_valid():
		news_mail=form.save()
		messages.success(request, f'Verify your email {news_mail.email} by clicking the link we sent to your mail to receive our updates')
		return redirect('index')
	else:
		for i in form:
			for a in i.errors:
				if a == 'This email already exists':
					news_mail=form.save()
					messages.success(request, f'Verify your email {news_mail.email} by clicking the link we sent to your mail to receive our updates')
					return redirect('index')
		email_errors=''
		for i in form:
			for a in i.errors:
				email_errors+=a
				email_errors+='<br>'
		context['email'] = email
		context['email_errors'] = email_errors
	return render(request, template_name, context)
class BlogPage(ListView):
	template_name = 'Blog/blog.html'
	context_object_name = 'posts'
	paginate_by=2
	model = Post
	extra_context = {'title':'Blog'}

	def post(self, request, **kwargs):
		search=request.POST.get('search')
		email=request.POST.get('email')
		context={}
		context['category']=Category.objects.all()
		posts = self.model.postadmin.all()
		if search:
			context['posts'] = posts.filter(title__icontains=search)
			context['search'] = search
			return render(request, self.template_name, context)
		if email:
			form = NewsletterForm(request.POST)
			if form.is_valid():
				news_mail=form.save()
				messages.success(self.request, f'Your email {news_mail.email} is now suscribed to receive our updates')
			else:
				email_errors=''
				for i in form:
					for a in i.errors:
						email_errors+=a
						email_errors+='<br>'
				context['email'] = email
				context['email_errors'] = email_errors
				pagin=Paginator(posts,self.paginate_by)
				context['posts'] = pagin.page(1)
				context['page_obj'] = pagin.page(1)
				return render(request, self.template_name, context)
		return redirect('blog')

	def get_context_data(self, **kwargs):
		context = super(BlogPage, self).get_context_data()
		context['category']=Category.objects.all()
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		return context

class BlogCategory(BlogPage, ListView):
	def get_queryset(self, **kwargs):
		return self.model.postadmin.filter(category__name=self.kwargs['category'])

	def get_context_data(self, **kwargs):
		context = super(BlogCategory, self).get_context_data()
		context['category']=Category.objects.all()
		context['category_name']=self.kwargs['category']
		context['title']='Category '+self.kwargs['category'].title()
		return context

class BlogAuthor(BlogCategory, ListView):
	def get_queryset(self, **kwargs):
		return self.model.postadmin.get_posts(self.kwargs['username'])

	def get_context_data(self, **kwargs):
		context = super(BlogCategory, self).get_context_data()
		context['category']=Category.objects.all()
		context['author_name']=self.kwargs['username'].title()
		context['title']='Posts by '+self.kwargs['username'].title()
		return context

class BlogDetailPage(DetailView):
	template_name = 'Blog/blog_detail.html'
	model = Post
	slug_url_kwarg = 'title_slug'
	slug_field = 'title_slug'
	context_object_name = 'post'
	
	def get(self, request, title_slug, **kwargs):
		form = CommentForm()
		self.object = get_object_or_404(self.model,title_slug=title_slug)
		# Adding help texts to fields
		if not request.session.get('viewer_id'):
			code = createViewer()
			request.session['viewer_id'] = code
			viewer = Views.objects.create(viewer = code)
			self.object.views.add(viewer)
		else:
			# Check if viewer as ever viewed this post
			viewer = Views.objects.get(viewer=self.request.session.get('viewer_id'))
			qs=self.object.views.filter(viewer=viewer)
			if not qs.exists():
				self.object.views.add(viewer)

		context=self.get_context_data()
		for i in form:
			context[i.name+'_h']=i.help_text
		return render(request, self.template_name, context)

	def post(self, request, title_slug, **kwargs):
		sender = request.POST.get('sender')
		form = CommentForm(request.POST)
		context = self.get_context_data()
		if sender == 'likes':
			# Creating the data that will be sent to javascript
			data={}
			viewer = Views.objects.get(viewer=request.session.get('viewer_id'))
			likes=self.get_object().likes.filter(viewer=viewer)
			if likes.exists():
				self.get_object().likes.remove(likes.first())
				# Data action below to tell javascript if the data was increased or decreased
				data['action']='-'
			else:
				self.get_object().likes.add(Likes.objects.get(viewer=viewer))
				# Data action below to tell javascript if the data was increased or decreased
				data['action']='+'
			if request.is_ajax():
				return JsonResponse(data, status=200)
		if form.is_valid():
			com=form.save(commit=False)
			com.post = self.get_object()
			com.save()
			return redirect(reverse('blog-detail', kwargs={'title_slug': title_slug}))
		else:
			for i in form:
				context[i.name]=i.value()
				e=''
				context[i.name+'_h']=i.help_text
				for a in i.errors:
					e+=(a+'<br>')
				context[i.name+'_e']=e
		return render(request, self.template_name, context)

	def get_context_data(self, **kwargs):
		# context = super(BlogDetailPage, self).get_context_data()
		context={}
		post = self.get_object()
		context['post'] = post
		context['title']=post.title
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		viewer = Views.objects.get(viewer=self.request.session.get('viewer_id'))
		likes=post.likes.filter(viewer=viewer)
		context['similar'] = self.model.postadmin.filter(category__name=post.category.name).exclude(title=post.title)[:4]
		context['category_name']=post.category.name
		if likes.exists():
			context['liked']='active'
		else:
			context['liked']=''
		return context
