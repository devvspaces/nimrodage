from django.urls import path
from .views import ReviewPage

urlpatterns = [
	path('reviews/', ReviewPage.as_view(), name='reviews'),
]