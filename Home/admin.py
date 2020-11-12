from django.contrib import admin
from django.db import models as dj_models
from trumbowyg.widgets import TrumbowygWidget
from .models import Contact, Service, Industry

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
	list_display=('name','email','client',)
	list_filter=('client', 'country', 'state',)

# Custom model admin to add wysiwyg to services and industry
class IndustryAdmin(admin.ModelAdmin):
	formfield_overrides={
		dj_models.TextField:{ 'widget': TrumbowygWidget() }
	}
	
	class Media:
		css={
			'all':("trumbo/ui/trumbowyg.min.css",)
		}
		js=(
			'js/jquery.js',
		)

admin.site.register(Contact, ContactAdmin)
admin.site.register(Service, IndustryAdmin)
admin.site.register(Industry, IndustryAdmin)
