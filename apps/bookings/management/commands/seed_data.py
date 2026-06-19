from django.core.management.base import BaseCommand
from apps.bookings.models import Service, Availability


SERVICES = [
    {
        'name': 'Consulta Médica General',
        'description': 'Consulta con médico general para diagnóstico y tratamiento de enfermedades comunes. Incluye revisión de signos vitales y prescripción si es necesario.',
        'duration_minutes': 30,
        'capacity': 1,
        'price': '80.00',
        'days': [0, 1, 2, 3, 4],  # Lunes a Viernes
        'start_time': '08:00',
        'end_time': '18:00',
    },
    {
        'name': 'Sesión de Psicología',
        'description': 'Sesión individual con psicólogo clínico. Atención de ansiedad, depresión, estrés y otros aspectos emocionales. Ambiente confidencial y seguro.',
        'duration_minutes': 50,
        'capacity': 1,
        'price': '120.00',
        'days': [0, 1, 2, 3, 4],  # Lunes a Viernes
        'start_time': '09:00',
        'end_time': '17:00',
    },
    {
        'name': 'Clase de Yoga',
        'description': 'Clase grupal de yoga para todos los niveles. Mejora flexibilidad, equilibrio y bienestar mental. Trae tu esterilla o solicita una prestada.',
        'duration_minutes': 60,
        'capacity': 10,
        'price': '35.00',
        'days': [0, 2, 4],  # Lunes, Miércoles, Viernes
        'start_time': '07:00',
        'end_time': '08:00',
    },
]


class Command(BaseCommand):
    help = 'Crea datos de ejemplo: 3 servicios con disponibilidad de lunes a viernes'

    def handle(self, *args, **options):
        created_count = 0
        for data in SERVICES:
            service, created = Service.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'duration_minutes': data['duration_minutes'],
                    'capacity': data['capacity'],
                    'price': data['price'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Servicio creado: {service.name}'))
            else:
                self.stdout.write(f'  Servicio ya existe: {service.name}')

            for day in data['days']:
                Availability.objects.get_or_create(
                    service=service,
                    day_of_week=day,
                    defaults={
                        'start_time': data['start_time'],
                        'end_time': data['end_time'],
                    }
                )

        self.stdout.write(self.style.SUCCESS(
            f'\nListo. {created_count} servicios nuevos creados. '
            'Ejecuta `python manage.py createsuperuser` para acceder al admin.'
        ))
