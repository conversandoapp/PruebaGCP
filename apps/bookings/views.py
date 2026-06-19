from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, Booking, Availability
from .forms import BookingForm


def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'home.html', {'services': services})


def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'bookings/list.html', {'services': services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    # Próximos 14 días con disponibilidad
    today = date.today()
    available_days = []
    availabilities = service.availabilities.all()
    available_weekdays = set(a.day_of_week for a in availabilities)
    for i in range(14):
        d = today + timedelta(days=i)
        if d.weekday() in available_weekdays:
            slots = availabilities.filter(day_of_week=d.weekday())
            # Excluir slots ya reservados (si capacity == 1)
            confirmed_times = set(
                Booking.objects.filter(
                    service=service, date=d, status__in=['pending', 'confirmed']
                ).values_list('start_time', flat=True)
            )
            day_slots = []
            for slot in slots:
                if slot.start_time not in confirmed_times:
                    day_slots.append(slot)
            if day_slots:
                available_days.append({'date': d, 'slots': day_slots})
    return render(request, 'bookings/detail.html', {
        'service': service,
        'available_days': available_days,
    })


@login_required
def booking_create(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    selected_slot = None

    if request.method == 'POST':
        form = BookingForm(request.POST, service=service)
        if form.is_valid():
            chosen_date = form.cleaned_data['date']
            avail = service.availabilities.filter(day_of_week=chosen_date.weekday()).first()
            if not avail:
                messages.error(request, 'No hay disponibilidad para ese día.')
                return redirect('booking_create', pk=pk)

            already = Booking.objects.filter(
                service=service, date=chosen_date,
                start_time=avail.start_time, status__in=['pending', 'confirmed']
            ).exists()
            if already:
                messages.error(request, 'Ese slot ya está reservado. Por favor elige otra fecha.')
                return redirect('booking_create', pk=pk)

            booking = form.save(commit=False)
            booking.service = service
            booking.user = request.user
            booking.start_time = avail.start_time
            booking.end_time = avail.end_time
            booking.save()
            messages.success(request, '¡Reserva creada con éxito!')
            return redirect('booking_confirm', pk=booking.pk)
    else:
        initial = {}
        selected_slot = None
        date_str = request.GET.get('date')
        if date_str:
            initial['date'] = date_str
            try:
                from datetime import date as date_type
                d = date_type.fromisoformat(date_str)
                selected_slot = service.availabilities.filter(day_of_week=d.weekday()).first()
            except ValueError:
                pass
        form = BookingForm(service=service, initial=initial)

    return render(request, 'bookings/create.html', {
        'service': service,
        'form': form,
        'selected_slot': selected_slot,
    })


@login_required
def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/confirm.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('service')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        if booking.status not in ('cancelled',):
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Reserva cancelada.')
        else:
            messages.warning(request, 'Esta reserva ya estaba cancelada.')
    return redirect('my_bookings')
