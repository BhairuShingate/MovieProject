# Generated by Django 5.2.2 on 2025-06-23 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=250)),
                ('address', models.TextField(max_length=255)),
            ],
        ),
    ]
