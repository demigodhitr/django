# Generated by Django 5.0.2 on 2024-03-03 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0012_remove_customuser_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='Withdrawal_pin',
            field=models.IntegerField(default=0),
        ),
    ]
