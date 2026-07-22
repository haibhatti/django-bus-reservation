from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, authenticate
from django.contrib.auth import login, logout
from . models import Ticket, FareMatrix, Trip, Location
from .forms import TicketForm, RouteSearchForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'home.html')
def user_login(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            
            if user is not None:
                login(request, user)
                return redirect('/dashboard/') 
    else:
        fm = AuthenticationForm()
        
    return render(request, 'userlogin.html', {'form': fm})

@login_required(login_url='/employee-login/')
def dashboard_view(request):
    return render(request, 'dashboard.html')
def user_logout(request):
    logout(request)
    return redirect('home')


def view_bookings(request):
    all_tickets = Ticket.objects.all()
    context = {
        'tickets': all_tickets
    }
    return render(request, 'booking_list.html', context)


@login_required(login_url='/employee-login/')
def search_route(request):
    if request.method == 'POST':
        form = RouteSearchForm(request.POST)
        if form.is_valid():
            request.session['search_data'] = {
                'origin_id': form.cleaned_data['origin'].id,
                'destination_id': form.cleaned_data['destination'].id
            }
            return redirect('book_ticket')
    else:
        form = RouteSearchForm()
        
    return render(request, 'search_route.html', {'form': form})
@login_required(login_url='/employee-login/')
def book_ticket(request):

    if 'search_data' not in request.session:
        return redirect('search_route')
        
    search_data = request.session['search_data']
    origin_id = search_data['origin_id']
    destination_id = search_data['destination_id']

    valid_trip_ids = FareMatrix.objects.filter(
        origin_id=origin_id, destination_id=destination_id
    ).values_list('trip_id', flat=True)
    
    valid_trips = Trip.objects.filter(id__in=valid_trip_ids)
    if not valid_trips.exists():
        messages.error(request, "No buses currently operate on this route. Please search another.")
        del request.session['search_data']
        return redirect('search_route')

    if request.method == 'POST':
        form = TicketForm(request.POST)
        form.fields['trip'].queryset = valid_trips
        
        if form.is_valid():
            trip = form.cleaned_data['trip']
            fare_rule = FareMatrix.objects.get(
                trip=trip, origin_id=origin_id, destination_id=destination_id
            )
            request.session['temp_ticket'] = {
                'trip_id': trip.id,
                'passenger_name': form.cleaned_data['passenger_name'],
                'origin_id': origin_id,
                'destination_id': destination_id,
                'seat_number': form.cleaned_data['seat_number'],
                'fare_paid': str(fare_rule.price)
            }
            return redirect('confirm_ticket')
    else:
        form = TicketForm()
        form.fields['trip'].queryset = valid_trips
        
    origin_name = Location.objects.get(id=origin_id).name
    dest_name = Location.objects.get(id=destination_id).name
        
    return render(request, 'book_ticket.html', {
        'form': form, 
        'origin_name': origin_name, 
        'dest_name': dest_name
    })

@login_required(login_url='/employee-login/')
def confirm_ticket(request):
    if 'temp_ticket' not in request.session:
        return redirect('search_route')
        
    data = request.session['temp_ticket']
    
    trip_obj = Trip.objects.get(id=data['trip_id'])
    origin_obj = Location.objects.get(id=data['origin_id'])
    dest_obj = Location.objects.get(id=data['destination_id'])
    
    if request.method == 'POST':
        Ticket.objects.create(
            trip=trip_obj,
            passenger_name=data['passenger_name'],
            origin=origin_obj,
            destination=dest_obj,
            seat_number=data['seat_number'],
            fare_paid=data['fare_paid']
        )
  
        del request.session['temp_ticket']
        if 'search_data' in request.session:
            del request.session['search_data']
        
        messages.success(request, f"Success! Ticket confirmed. Auto-charged: Rs. {data['fare_paid']}")
        return redirect('view_bookings')
        
    context = {
        'trip': trip_obj,
        'passenger': data['passenger_name'],
        'origin': origin_obj,
        'destination': dest_obj,
        'seat': data['seat_number'],
        'price': data['fare_paid']
    }
    
    return render(request, 'confirm_ticket.html', context)

@login_required(login_url='/employee-login/')
def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    valid_trip_ids = FareMatrix.objects.filter(
        origin=ticket.origin, destination=ticket.destination
    ).values_list('trip_id', flat=True)
    valid_trips = Trip.objects.filter(id__in=valid_trip_ids)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        form.fields['trip'].queryset = valid_trips
        
        if form.is_valid():
            updated_ticket = form.save(commit=False)
            fare_rule = FareMatrix.objects.get(
                trip=updated_ticket.trip, origin=ticket.origin, destination=ticket.destination
            )
            updated_ticket.fare_paid = fare_rule.price
            updated_ticket.save()
            
            messages.success(request, f"Ticket for {updated_ticket.passenger_name} successfully updated!")
            return redirect('view_bookings')
    else:
        form = TicketForm(instance=ticket)
        form.fields['trip'].queryset = valid_trips
        
    return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})

@login_required(login_url='/employee-login/')
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        passenger_name = ticket.passenger_name
        
        ticket.delete()
 
        messages.error(request, f"Ticket for {passenger_name} has been cancelled and deleted.")
        return redirect('view_bookings')
      
    return render(request, 'delete_ticket.html', {'ticket': ticket})