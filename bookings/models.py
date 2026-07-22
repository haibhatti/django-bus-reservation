from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Bus(models.Model):
    bus_number= models.CharField(max_length=250, unique=True)
    total_seats = models.IntegerField(default=40)
    def __str__(self):
        return self.bus_number

class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete= models.CASCADE)
    route_name = models.CharField(max_length=255)
    date = models.DateField()
    departure_time = models.TimeField()
    def __str__(self):
        return f"{self.route_name} - {self.date}"

class FareMatrix(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    origin = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='fare_origin')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='fare_dest')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.origin} to {self.destination} - {self.price}"

class Ticket(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=255)
    origin = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='ticket_origin')
    destination = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='ticket_dest')
    seat_number = models.IntegerField()
    fare_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('trip', 'seat_number')
    def __str__(self):
        return f"{self.passenger_name} (Seat: {self.seat_number})"