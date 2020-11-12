from django.urls import path
from .views import BlogPage, BlogDetailPage, BlogCategory, BlogAuthor, activate_email

urlpatterns = [
	path('blog/', BlogPage.as_view(), name='blog'),
	path('blog/<str:title_slug>/', BlogDetailPage.as_view(), name='blog-detail'),
	path('blog/category/<str:category>/', BlogCategory.as_view(), name='blog-category'),
	path('blog/author/<str:username>/', BlogAuthor.as_view(), name='blog-author'),
	path("activate/<slug:uidb64>/<slug:token>/", activate_email, name="activate_email"),
]