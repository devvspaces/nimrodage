# Generated by Django 3.1.1 on 2020-10-05 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('email', models.EmailField(help_text='e.g. nimrodage@gmail.com', max_length=255)),
                ('business_phone', models.CharField(help_text='format is +234-9033234234', max_length=16)),
                ('mobile_phone', models.CharField(help_text='format is +234-9033234234', max_length=16)),
                ('address', models.TextField()),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('client', models.CharField(choices=[('N', 'New'), ('E', 'Existing')], max_length=1)),
                ('meeting', models.CharField(choices=[('G', 'Google/Internet search'), ('R', 'Referral'), ('O', 'Other')], max_length=1)),
                ('phrase', models.CharField(help_text='What phrase did you search?', max_length=255)),
                ('referred', models.CharField(help_text='Who referred you?', max_length=255)),
                ('other', models.CharField(help_text='How did you hear about us?', max_length=255)),
                ('message', models.TextField()),
                ('d_date', models.CharField(help_text='e.g., Next month, December 9th, ASAP, etc.', max_length=255)),
                ('s_date', models.DateTimeField()),
                ('uid', models.CharField(max_length=64)),
            ],
        ),
    ]
