from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Ticket, User
from .forms import EventForm, TicketForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlencode
from .models import CashPayment
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def event_list(request):
    events = Event.objects.all()
    current_user = request.user.id
    return render(request, 'event.html', {'events': events, 'current_user': current_user})

@login_required
def admin_event_list(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'dash/event_list.html', {'events': events})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('mypage')
    else:
        form = EventForm()
    return render(request, 'dash/add_event.html', {'form': form})

import logging
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EventForm
from .models import Event, User

logger = logging.getLogger(__name__)
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            participants = User.objects.filter(user_type='Participant')
            for participant in participants:
                send_notification(participant.email, event)
            return redirect('events')
    else:
        form = EventForm(instance=event)
    return render(request, 'dash/edit_event.html', {'form': form})

def send_notification(email, event):
    subject = f"Event Updated: {event.title}"
    message = f"The event '{event.title}' has been updated. Here are the new details:\n\n" \
              f"Title: {event.title}\n" \
              f"Description: {event.description}\n" \
              f"Start Time: {event.start_time}\n" \
              f"End Time: {event.end_time}\n" \
              f"Location: {event.location}\n" \
              f"Price: {event.price}\n"
    from_email = 'info@hisobu.co.tz'
    try:
        send_mail(subject, message, from_email, [email])
        logger.info(f'Email sent to {email} regarding event {event.title}')
    except Exception as e:
        logger.error(f'Failed to send email to {email}: {e}')

@login_required
def purchase_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.participant = request.user
            ticket.event = event
            ticket.save()
            return redirect('my_tickets')
    else:
        form = TicketForm(initial={'event': event})
    return render(request, 'purchase_ticket.html', {'form': form, 'event': event})

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(participant=request.user)
    return render(request, 'my_tickets.html', {'tickets': tickets})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # Ensure username is set to email
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'Event Organizer':
                    return redirect('mypage')  # Redirect to the contact page for event organizers
                else:
                    return redirect('event')  # Redirect to the index page for participants

        # Display an error message for invalid credentials
        messages.error(request, 'Umekosea email au password. Tafadhali jaribu tena au jisajili kwanza!', extra_tags='error-red')

        if request.POST.get('rememberme'):
            # Set a longer session expiry for "Remember me" users
            request.session.set_expiry(1209600)  # Two weeks in seconds
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('login')


def default(request):
    return render(request, 'default.html')

from django.shortcuts import render, get_object_or_404
from .models import Event

@login_required
def dash(request, event_id=None):
    kukus = Event.objects.all()
    event = None
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    return render(request, 'dash/index.html', {'event': event, 'kukus': kukus})

def playground(request):
    data = User.objects.filter(phone__gt=2)
    return render(request, 'playground.html', {'data': data})

def success(request):
    return render(request, 'success.html')

def payment(request):
    return render(request, 'payment.html')


def display_events(request):
    events = Event.objects.all()  # Fetch all events
    return render(request, 'user_events.html', {'events': events})

def process_payment(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        price = request.POST.get('price')

        # Add the necessary parameters for Flutterwave
        flutterwave_url = "https://flutterwave.com/pay"
        params = {
            'tx_ref': f'event_{event_id}',
            'amount': price,
            'currency': 'TZS',  # Adjust currency as needed
            'redirect_url': 'http://yourdomain.com/payment_success',  # URL to handle after payment
            'payment_options': 'card, banktransfer',
            'customer': {
                'email': 'dummy@example.com',  # Dummy email
                'phonenumber': '1234567890',  # Dummy phone number
                'name': 'John Doe',  
            },
            'customizations': {
                'title': 'Event Ticket',
                'description': f'Ticket for {event_id}',
            }
        }

        # Redirect to the Flutterwave payment page with parameters
        redirect_url = f"{flutterwave_url}?{urlencode(params)}"
        return redirect(redirect_url)

    return redirect('events')  # Redirect back to events if not a POST request
def index(request):
    events = [
        {"id": 1, "title": "Event 1", "description": "Description 1", "start_time": "10:00 AM", "location": "Location 1", "price": 2500},
        {"id": 2, "title": "Event 2", "description": "Description 2", "start_time": "11:00 AM", "location": "Location 2", "price": 3000}
    ]
    return render(request, 'dash/index.html', {'events': events})

from django.http import JsonResponse, HttpResponseBadRequest
import json
@csrf_exempt
def save_cash_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event_id = data.get('event_id')
        participant_id = data.get('participant_id')
        purchase_time = data.get('purchase_time')

        # Save the data to the database
        cash_payment = CashPayment(
            event_id=event_id,
            participant_id=participant_id,
            purchase_time=purchase_time
        )
        cash_payment.save()

        # Return a success response
        return JsonResponse({'success': True})

    # Return an error response if request method is not POST
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def get_purchased_event_ids(request):
    user = request.user
    purchased_event_ids = CashPayment.objects.filter(participant_id=user.id).values_list('event_id', flat=True)
    return JsonResponse({'purchased_event_ids': list(purchased_event_ids)})

# utils.py or views.py
#kodi zangu za email
from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user_email):
    subject = 'Welcome to Our Service'
    message = 'Thank you for signing up for our service.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

# views.py
#kodi zangu za emai
from django.shortcuts import render, redirect
from .models import User
from .views import send_welcome_email
from .forms import UserRegistrationForm  # Assuming you have a form for user registration

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user.email)
            return redirect('events')  # Redirect to a success page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
