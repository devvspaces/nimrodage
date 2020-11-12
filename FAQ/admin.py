from django.contrib import admin
from .models import Faq, NewQuestion

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
	list_display=('name','email','answered',)
	list_filter = ('answered',)

admin.site.register(Faq)
admin.site.register(NewQuestion, QuestionAdmin)