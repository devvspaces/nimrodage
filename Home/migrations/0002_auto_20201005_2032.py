# Generated by Django 3.1.1 on 2020-10-05 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='business_phone',
            field=models.CharField(blank=True, help_text='format is +234-9033234234', max_length=16),
        ),
        migrations.AlterField(
            model_name='contact',
            name='company',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='d_date',
            field=models.CharField(blank=True, help_text='e.g., Next month, December 9th, ASAP, etc.', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile_phone',
            field=models.CharField(blank=True, help_text='format is +234-9033234234', max_length=16),
        ),
        migrations.AlterField(
            model_name='contact',
            name='other',
            field=models.CharField(blank=True, help_text='How did you hear about us?', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phrase',
            field=models.CharField(blank=True, help_text='What phrase did you search?', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='referred',
            field=models.CharField(blank=True, help_text='Who referred you?', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='s_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]