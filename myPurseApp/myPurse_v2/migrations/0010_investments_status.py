# Generated by Django 5.0 on 2024-05-28 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myPurse_v2', '0009_cardrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='investments',
            name='status',
            field=models.CharField(default='awaiting slot entry', max_length=100),
        ),
    ]
