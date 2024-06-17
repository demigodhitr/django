# Generated by Django 5.0.2 on 2024-03-02 08:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0005_alter_notifications_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField(blank=True, max_length=16, null=True)),
                ('expiry_date', models.DateField()),
                ('cvv', models.IntegerField(blank=True, max_length=3, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
