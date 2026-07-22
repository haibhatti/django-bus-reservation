# Bus Reservation System (Django)

This is a web application I built to manage bus terminal bookings. It handles the whole process from setting up routes to printing passenger tickets. 

I built this project while learning Python and the Django framework to get hands-on experience with backend logic, database models, and user sessions.

## What it does:
* **Admin Side:** Managers can log in to add buses, create routes, and set the exact fare prices for different cities.
* **Employee Side:** Terminal workers can log in, search for a route, and the system will automatically filter which buses go there. It calculates the price instantly using a 3-step booking form.
* **Double-Booking Prevention:** The database is set up to strictly prevent two passengers from being booked on the same seat for the same trip.

## Technologies Used:
* Python / Django
* SQLite (Database)
* HTML / Bootstrap 5 (Frontend)

## How to run it locally:
1. Download or clone the code.
2. Open your terminal and install Django: `pip install django`
3. Run the migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`
5. Open your browser and go to `http://127.0.0.1:8000/`
