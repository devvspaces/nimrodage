# Generated by Django 3.1.1 on 2020-10-29 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0020_auto_20201029_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmarketing',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]