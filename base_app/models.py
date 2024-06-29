from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE = [
        ('Event Organizer', 'Event Organizer'),
        ('Participant', 'Participant')
    ]
    
    username = models.EmailField(unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=40, default='', null=True, blank=True)
    last_name = models.CharField(
        max_length=40, default='', null=True, blank=True)
    phone = models.CharField(max_length=15)
    user_type = models.CharField(
        max_length=30, choices=USER_TYPE, default='Event Organizer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


class Event(models.Model):
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='tickets')
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tickets')
    purchase_time = models.DateTimeField(auto_now_add=True)



class CashPayment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = "Payments"