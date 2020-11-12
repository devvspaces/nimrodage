from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from .forms import NewQuestionForm
from .models import Faq
from Home.models import Service, Industry

# Create your views here.
class FaqPage(ListView):
	template_name = 'FAQ/faq.html'
	context_object_name = 'faqs'
	model = Faq
	paginate_by = 6
	def get_context_data(self, page=1):
		context={}
		context['title']='Frequently asked questions'
		context['klass']='faqPage'
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		context['faqs']= Paginator(self.get_queryset(),self.paginate_by).page(page)
		return context
	def get(self, request):
		gets = request.GET.get('page')
		if gets == None:
			gets = 1
		context=self.get_context_data(gets)
		return render(self.request, self.template_name, context)
	def post(self, request):
		search = request.POST.get('search')
		context=self.get_context_data()
		if search:
			sets = self.get_queryset().filter(question__icontains = search)
			context['faqs'] = sets
		else:
			form = NewQuestionForm(request.POST)
			if form.is_valid():
				newq = form.save()
				messages.success(self.request, 'Your question has been delivered, your answer will be mailed to you.')
				return redirect('faq')
			for i in form:
				txt = []
				for a in i.errors:
					txt.append(a)
				txt = '<br>'.join(txt)
				context[i.name+'_e'] = txt
				context[i.name+'_h'] = i.help_text
				context[i.name] = i.value()
		return render(self.request, self.template_name, context)
