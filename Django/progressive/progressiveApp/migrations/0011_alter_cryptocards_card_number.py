# Generated by Django 5.0.2 on 2024-03-02 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0010_cryptocards_card_holder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocards',
            name='card_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]