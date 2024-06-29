from django.contrib import admin

from base_app.forms import UserRegistrationForm
from .models import CashPayment, Event, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(CashPayment)
class CashPaymentAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'participant_username', 'purchase_time')
    search_fields = ('event__title', 'participant__username')
    list_filter = ('purchase_time',)

    def event_name(self, obj):
        return obj.event.title
    
    def participant_username(self, obj):
        return obj.participant.username
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_time', 'end_time', 'location', 'price')
    list_filter = ('start_time', 'end_time', 'location')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_time'

    def organizer(self, obj):
        return obj.organizer.username


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserRegistrationForm
    form = UserRegistrationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'email', 'user_type'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'phone', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'phone', 'email')
    ordering = ('username',)