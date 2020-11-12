from django import forms
from django.contrib import admin
from django.db import models as dj_models
from trumbowyg.widgets import TrumbowygWidget
from .models import Post,Category,Comment,Views,Likes,Reply,Newsletter,EmailMarketing

class LikesFilter(admin.SimpleListFilter):
	title="likes"
	parameter_name="greaterThan"
	custom_dict={
					'1': '0',
					'2': '50',
					'3': '100',
					'4': '150',
					'5': '200',
				}
	def lookups(self,request,model_admin):
		return (
			("1", "> 0",),
			("2","> 50",),
			("3","> 100",),
			("4","> 150",),
			("5","> 200",),
		)
	def queryset(self, request, queryset):
		for a,b in self.custom_dict.items():
			if self.value()==a:
				return queryset.filter(likes__gt=b)
		return queryset

def mk_published(modeladmin, request, queryset):
	queryset.update(
		draft=False,
	)
mk_published.short_description="Mark as published"

def mk_draft(modeladmin, request, queryset):
	queryset.update(
		draft=True,
	)
mk_draft.short_description="Mark as draft"

class BlogAdmin(admin.ModelAdmin):
	list_display=('title','author','category','count_likes','count_views','draft',)
	list_filter = ('draft','author','category', LikesFilter,)
	search_fields=['title']
	actions=[mk_draft,mk_published]
	fields=(
		"title",
		"title_slug",
		"author",
		'category',
		'draft',
		'content',
	)
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


def send_campaigns_verified_only(modeladmin, request, queryset):
	for user in queryset:
		user.email_users(only_verified=True)
send_campaigns_verified_only.short_description="Send campaigns to verified emails only"

def send_campaigns(modeladmin, request, queryset):
	for user in queryset:
		user.email_users()
send_campaigns.short_description="Send the marked campaigns to all emails"

class EmailMarketingAdmin(admin.ModelAdmin):
	list_display=('subject','email_lists','count_sent','count_reject','amount',)
	list_filter = ('date',)
	search_fields=['subject']
	actions=[send_campaigns,send_campaigns_verified_only]
	fields=(
		"subject",
		"message",
	)
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

class CommentAdmin(admin.ModelAdmin):
	list_display=('name','post','has_reply','date',)
	list_filter = ('date','has_reply',)
	search_fields = ('name','post','comment',)

class NewsletterAdmin(admin.ModelAdmin):
	list_display=('email','verified',)
	list_filter = ('verified',)
	search_fields=['email']

# Register your models here.
admin.site.register(Post, BlogAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Views)
admin.site.register(Likes)
admin.site.register(Reply)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(EmailMarketing, EmailMarketingAdmin)