from django.urls import path
from .views import Index, ContactView, IndustryView, ServiceView

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('certs/', Index.as_view(template_name='Home/certs.html'), name='certs'),
	path('safety/', Index.as_view(template_name='Home/safety.html'), name='safety'),
	path('needs/', Index.as_view(template_name='Home/needs.html'), name='needs'),
	path('contact/', ContactView.as_view(), name='contact'),
	path('industry/<str:slug>/', IndustryView.as_view(), name='industry'),
	path('service/<str:slug>/', ServiceView.as_view(), name='service'),
]