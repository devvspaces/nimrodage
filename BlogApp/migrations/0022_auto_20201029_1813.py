# Generated by Django 3.1.1 on 2020-10-29 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0021_emailmarketing_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmarketing',
            name='receivers',
            field=models.ManyToManyField(blank=True, related_name='Receivers', to='BlogApp.Newsletter'),
        ),
        migrations.AlterField(
            model_name='emailmarketing',
            name='rejects',
            field=models.ManyToManyField(blank=True, to='BlogApp.Newsletter'),
        ),
        migrations.AlterField(
            model_name='emailmarketing',
            name='sents',
            field=models.ManyToManyField(blank=True, related_name='Sents', to='BlogApp.Newsletter'),
        ),
    ]
