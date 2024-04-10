# Generated by Django 5.0.2 on 2024-02-27 18:54

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('Profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('Deposits', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('Bonus', models.DecimalField(blank=True, decimal_places=2, default=15.0, max_digits=10, null=True)),
                ('Profits', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('Withdrawal_limit', models.DecimalField(blank=True, decimal_places=2, default=7000.0, max_digits=10, null=True)),
                ('TradeIsActive', models.BooleanField(default=False)),
                ('CanWithraw', models.BooleanField(default=False)),
                ('TradeStatus', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Completed', 'Completed'), ('Canceled', 'Canceled'), ('Paused', 'Paused'), ('No Trade', 'No Trade')], default='No Trade', max_length=30)),
                ('VerificationStatus', models.CharField(blank=True, choices=[('Verified', 'Verified'), ('Failed', 'Failed'), ('Under review', 'Under Review'), ('Awaiting', 'Awaiting')], default='Awaiting', max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]