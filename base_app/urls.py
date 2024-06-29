from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.event_list, name='event'),
    path('admin_events/', views.admin_event_list, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/create/', views.create_event, name='add'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit'),
    path('events/<int:event_id>/purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('default/', views.default, name='default'),
    path('playground/', views.playground, name='playground'),
    path('mypage/', views.dash, name='mypage'),
    path('success/', views.success, name='success'),
    path('events/', views.display_events, name='display_events'),
     path('process_payment/', views.process_payment, name='process_payment'),
     path('', views.index, name='index'),
    path('payment/', views.payment, name='payment'),
    path('display_events/', views.display_events, name='display_events'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('save_cash_payment/', views.save_cash_payment, name='save_cash_payment'),
    path('api/get_purchased_event_ids/', views.get_purchased_event_ids, name='get_purchased_event_ids'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
