from django import forms
from .models import Event, Ticket

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'title'
            }),
            'uzito_wa_tukio': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'placeholder': 'YYYY-MM-DD HH:MM:SS',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'placeholder': 'YYYY-MM-DD HH:MM:SS',
                'type': 'datetime-local'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'description',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('Event Organizer', 'Event Organizer'),
        ('Participant', 'Participant')
    ]
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone', 'username', 'password1', 'password2','user_type']
