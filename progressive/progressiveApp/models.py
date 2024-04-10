from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random
import string


# Defines my user manager Custom

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
# Defines my users outside Django default user model

class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'last_name']

    def __str__(self):
        return self.username

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = f'You just created a purse!, {instance.first_name}!'
        message = render_to_string('welcome_email.html', {'user': instance})
        from_email = 'alerts@myprofitpurse.com'
        recipient_list = [instance.email]
        send_mail(
            subject, 
            message, 
            from_email, 
            recipient_list,
            html_message=message,
        )

class UserProfile(models.Model):
    verification_choices = [
        ('Verified', 'Verified'),
        ('Failed', 'Failed'),
        ('Under review', 'Under Review'),
        ('Awaiting', 'Awaiting'),]
    
    trade_choices = [
        ('Active', 'Active'), 
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Paused', 'Paused'),
        ('No Trade', 'No Trade'),]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    can_login = models.BooleanField(default=True)
    Nationality = models.CharField(max_length=50, null=True, blank=True)
    Profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    Deposits = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null=True, blank=True)
    Bonus = models.DecimalField(default=15.00, max_digits=10, decimal_places=2, null=True, blank=True)
    Profits = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null=True, blank=True)

    AccountManager = models.CharField(max_length=255, blank=True, null=True, default='No assigned Trader')

    Withdrawal_limit = models.DecimalField(default=7000.00, max_digits=10, decimal_places=2, null=True, blank=True)
    card_pin = models.IntegerField(default=0)
    TradeIsActive = models.BooleanField(default=False)
    CanWithraw = models.BooleanField(default=False)
    TradeStatus = models.CharField(max_length=30, default='No Trade', choices=trade_choices)
    VerificationStatus = models.CharField(max_length=50, default='Awaiting', null=True, blank=True,choices=verification_choices)
    @property
    def total_balance(self):
        return self.Deposits + self.Bonus + self.Profits
    
    def save(self, *args, **kwargs):
        if not self.card_pin:
            self.card_pin = ''.join(random.choices(string.digits[1:], k=6))
        super().save(*args, **kwargs)



class is_verified(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    verification_code = models.IntegerField()
    creation_time = models.DateTimeField(auto_now_add=True)


class ExchangeRates(models.Model):
    bitcoin_rate = models.DecimalField(decimal_places=10, max_digits=20, null=True, blank=True)
    ethereum_rate = models.DecimalField(decimal_places=10, max_digits=20, null=True, blank=True)
    usdt_rate = models.DecimalField(decimal_places=10, max_digits=20, null=True, blank=True)

class CryptoBalances(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bitcoin_balance = models.DecimalField(decimal_places=10, max_digits=20, null=True, blank=True)
    ethereum_balance = models.DecimalField(decimal_places=10, max_digits=20, null=True, blank=True)
    usdt_balance = models.DecimalField(decimal_places=10, max_digits=20, null=True, blank=True)

@receiver(post_save, sender=ExchangeRates)
def update_crypto_balances(sender, **kwargs):
    exchange_rates = ExchangeRates.objects.first()
    if exchange_rates:
        for user_profile in UserProfile.objects.all():
            crypto_balances, created = CryptoBalances.objects.get_or_create(user=user_profile.user)
            crypto_balances.bitcoin_balance = user_profile.total_balance * exchange_rates.bitcoin_rate
            crypto_balances.ethereum_balance = user_profile.total_balance * exchange_rates.ethereum_rate
            crypto_balances.usdt_balance = user_profile.total_balance * exchange_rates.usdt_rate
            crypto_balances.save()

    else:
        print('No exchange rates found, Unable to Update Balances')
    



class CryptoCards(models.Model):
    card_status_choices = [
        ('Not activated', 'Not activated'),
        ('Activated', 'Activated'),
        ('Blocked', 'Blocked'),]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_holder = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.DateField()
    cvv = models.IntegerField(null=True, blank=True)
    available_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    card_status = models.CharField(max_length=15, default='Not activated', choices=card_status_choices)

    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = ''.join(random.choices(string.digits, k=16))
        if not self.cvv:
            self.cvv = ''.join(random.choices(string.digits, k=3))
        super().save(*args, **kwargs)


class PaymentDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bitcoin_address = models.CharField(max_length=255, blank=True, null=True)
    ethereum_address = models.CharField(max_length=255, blank=True, null=True)
    usdt_TRC20_address = models.CharField(max_length=255, blank=True, null=True)
    usdt_ERC20_address = models.CharField(max_length=255, blank=True, null=True)
    

      
class Notifications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default= 'Welcome!!')
    message = models.TextField(default='Thank you for joining us. Should you have any questions or concerns, kindly open a chat and an admin will be assigned to you.')
    created_at = models.DateTimeField(auto_now_add=True)

#terms and conditions model

class TermsAndCondition(models.Model):
    Title = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    message2 = models.TextField(max_length=5000, null=True, blank=True)

# Withdrawal request model.
class WithdrawalRequest(models.Model):
    options = [
        ('Checking', 'Checking'),
        ('Paid', 'Paid'),
        ('Under review', 'Under review'),
        ('Failed', 'Failed'),
        ('Approved, Pending', 'Approved, Pending'),]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    network = models.CharField(max_length=100, default='no data')
    address = models.CharField(max_length=255, default='no data')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=30, default='Checking', choices=options) 
    created_at = models.DateTimeField(auto_now_add=True)
    RequestID = models.IntegerField(default=00000000, blank=True, null=True)

#wallet address model

class WalletAddress(models.Model):
    bitcoin = models.CharField(max_length=150)

    ethereum = models.CharField(max_length=150)

    tether_USDT = models.CharField(max_length=150)

    ERC20_address = models.CharField(max_length=150)

# Deposit model

class Deposit(models.Model):
    options = [
        ('No deposit', 'No Deposit'),
        ('Invalid', 'Invalid'),
        ('Failed', 'Failed'),
        ('Under review', 'Under review'),
        ('Confirmed', 'Confirmed'),
        ('Credited', 'Credited'),]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    DepositAmount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True, blank=True)
    Network = models.CharField(max_length=100, null=True, blank=True)
    Proof = models.ImageField(upload_to='payments/', null=True, blank=True)
    status = models.CharField(max_length=50, default='', choices=options)
    requestID = models.CharField(default='', max_length=8, null=True, blank=True)
    Confirmed = models.BooleanField(default=False)
    not_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.requestID:
            self.requestID = ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

class IDME(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True )
    DOB = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    id_front = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    id_back = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    phone = models.CharField(max_length=20, default='', blank=True, null=True)


class Charts(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deposits = models.CharField(max_length= 10, editable=False, default='Deposits', verbose_name='deposits', blank=True)
    deposits_day_one = models.CharField(max_length=10, default=0, null=True, blank=True)
    deposits_day_two = models.CharField(max_length=10, default=0, null=True, blank=True)
    deposits_day_three = models.CharField(max_length=10, default=0, null=True, blank=True)
    deposits_day_four = models.CharField(max_length=10, default=0, null=True, blank=True)
    deposits_day_five = models.CharField(max_length=10, default=0, null=True, blank=True)
    
    profits = models.CharField(max_length= 10, editable=False, verbose_name='profits', default='Profits', blank=True)
    profits_day_one = models.CharField(max_length=10, default=0, null=True, blank=True)
    profits_day_two = models.CharField(max_length=10, default=0, null=True, blank=True)
    profits_day_three = models.CharField(max_length=10, default=0, null=True, blank=True)
    profits_day_four = models.CharField(max_length=10, default=0, null=True, blank=True)
    profits_day_five = models.CharField(max_length=10, default=0, null=True, blank=True)

    losses = models.CharField(max_length= 10, editable=False, default='Profits', blank=True, verbose_name='losses')
    losses_day_one = models.CharField(max_length=10, default=0, null=True, blank=True)
    losses_day_two = models.CharField(max_length=10, default=0, null=True, blank=True)
    losses_day_three = models.CharField(max_length=10, default=0, null=True, blank=True)
    losses_day_four = models.CharField(max_length=10, default=0, null=True, blank=True)
    losses_day_five = models.CharField(max_length=10, default=0, null=True, blank=True)




class WebsiteVisitors(models.Model):
    fullName = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

 
    # Create your models here.
