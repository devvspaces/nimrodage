from django.db import models
class PostQuery(models.QuerySet):
    def get_authors_post(self, username):
        return self.filter(author__username=username)
class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuery(model=self.model, using=self._db)
    def get_posts(self, username):
        return self.get_queryset().get_authors_post(username)