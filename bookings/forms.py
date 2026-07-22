from django import forms
from . models import Ticket, Location

class RouteSearchForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    destination = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['trip', 'passenger_name', 'seat_number']
        
        widgets = {
            'trip': forms.Select(attrs={'class': 'form-select'}),
            'passenger_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'seat_number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '40'}),
        }
