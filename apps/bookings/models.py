from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    duration_minutes = models.IntegerField(verbose_name='Duración (minutos)')
    capacity = models.IntegerField(default=1, verbose_name='Capacidad por slot')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Precio')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['name']

    def __str__(self):
        return self.name


class Availability(models.Model):
    DAYS = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        related_name='availabilities', verbose_name='Servicio'
    )
    day_of_week = models.IntegerField(choices=DAYS, verbose_name='Día de la semana')
    start_time = models.TimeField(verbose_name='Hora inicio')
    end_time = models.TimeField(verbose_name='Hora fin')

    class Meta:
        verbose_name = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidades'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.service.name} — {self.get_day_of_week_display()} {self.start_time:%H:%M}–{self.end_time:%H:%M}"


class Booking(models.Model):
    STATUS = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ]
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT,
        related_name='bookings', verbose_name='Servicio'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='bookings', verbose_name='Usuario'
    )
    date = models.DateField(verbose_name='Fecha')
    start_time = models.TimeField(verbose_name='Hora inicio')
    end_time = models.TimeField(verbose_name='Hora fin')
    status = models.CharField(
        max_length=20, choices=STATUS, default='pending', verbose_name='Estado'
    )
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.service.name} {self.date}"
