# Generated by Django 5.0.2 on 2024-03-04 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0015_rename_address_paymentdetails_bitcoin_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='Withdrawal_pin',
        ),
        migrations.AddField(
            model_name='cryptocards',
            name='pin',
            field=models.IntegerField(default=0),
        ),
    ]
