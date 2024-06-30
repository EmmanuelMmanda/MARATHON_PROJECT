
from asyncio.log import logger
from django.core.mail import send_mail
from django.conf import settings


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

