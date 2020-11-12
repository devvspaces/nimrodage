from django.shortcuts import render
from django.views.generic import ListView
from .models import Reviews
from Home.models import Service, Industry

# Create your views here.
class ReviewPage(ListView):
	model = Reviews
	context_object_name = 'reviews'
	template_name = 'reviews/reviews.html'
	def get_context_data(self):
		context = super(ReviewPage, self).get_context_data()
		context['title']='Reviews'
		context['services']=Service.objects.all()
		context['industries']=Industry.objects.all()
		return context
		