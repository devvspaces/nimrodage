# Generated by Django 3.1.1 on 2020-10-16 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0007_auto_20201016_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='viewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogApp.views'),
        ),
    ]
