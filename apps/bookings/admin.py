from django.contrib import admin
from .models import Service, Availability, Booking


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_minutes', 'capacity', 'price', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'price']
    inlines = [AvailabilityInline]


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['service', 'day_of_week', 'start_time', 'end_time']
    list_filter = ['service', 'day_of_week']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'date', 'start_time', 'end_time', 'status', 'created_at']
    list_filter = ['status', 'service', 'date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'service__name']
    list_editable = ['status']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
