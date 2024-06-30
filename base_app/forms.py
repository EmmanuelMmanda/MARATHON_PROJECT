from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Event, Ticket


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time',
                  'end_time', 'location', 'price']
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
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and not self.user.is_superuser:
            self.fields['organizer'].initial = self.user
            self.fields['organizer'].queryset = User.objects.filter(id=self.user.id)
        else:
            self.fields['organizer'].queryset = User.objects.all()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event']


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
        fields = ['first_name', 'last_name', 'email',
                  'phone', 'password1', 'password2', 'user_type']
