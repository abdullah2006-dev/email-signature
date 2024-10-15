# Generated by Django 5.1.1 on 2024-09-11 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('job_title', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
