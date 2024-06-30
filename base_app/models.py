from django.db import models
from django.contrib.auth.models import AbstractUser,Group


class User(AbstractUser):
    USER_TYPE = [
        ('Event Organizer', 'Event Organizer'),
        ('Participant', 'Participant')
    ]

    phone = models.CharField(max_length=15)
    user_type = models.CharField(
        max_length=30, choices=USER_TYPE, default='Event Organizer')

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Ensure user is active
        self.is_active = True
        self.is_staff = True

        # Assign user to the appropriate group
        if self.user_type == 'Event Organizer':
            organizer_group, created = Group.objects.get_or_create(
                name='Organizers')
            self.groups.add(organizer_group)

        # Save again to apply changes
        super().save(*args, **kwargs)

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
