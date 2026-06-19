from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
        label='Fecha',
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Información adicional (opcional)',
        }),
        label='Notas',
    )

    class Meta:
        model = Booking
        fields = ['date', 'notes']

    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service

    def clean_date(self):
        from datetime import date
        d = self.cleaned_data['date']
        if d < date.today():
            raise forms.ValidationError('La fecha no puede ser en el pasado.')
        if self.service:
            day = d.weekday()
            has_availability = self.service.availabilities.filter(day_of_week=day).exists()
            if not has_availability:
                raise forms.ValidationError('El servicio no está disponible ese día.')
        return d
