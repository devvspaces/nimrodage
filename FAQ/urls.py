from django.urls import path
from .views import FaqPage

urlpatterns = [
	path('faq/', FaqPage.as_view(), name='faq'),
]