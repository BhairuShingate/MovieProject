# Generated by Django 5.2.2 on 2025-06-23 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theaters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('row_label', models.CharField(max_length=1)),
                ('seat_type', models.CharField(choices=[('regular', 'Regular'), ('silver', 'Silver'), ('gold', 'Gold')], default='Regular', max_length=50)),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='theaters.theater')),
            ],
        ),
    ]
