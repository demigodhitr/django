# Generated by Django 5.0.2 on 2024-03-05 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0024_alter_exchangerates_bitcoin_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='can_login',
            field=models.BooleanField(default=True),
        ),
    ]