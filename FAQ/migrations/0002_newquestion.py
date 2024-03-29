# Generated by Django 3.1.1 on 2020-10-11 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('email', models.EmailField(max_length=254)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('answered', models.BooleanField(blank=True, default=False)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
