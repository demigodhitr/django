# Generated by Django 5.0.2 on 2024-03-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0007_alter_cryptocards_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocards',
            name='cvv',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
