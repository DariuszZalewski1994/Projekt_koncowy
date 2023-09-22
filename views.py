from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Airport, Flight, Aircraft, FlightType
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.urls import reverse

# Create your views here.
def hello_world(request):
    hello = "hello world"
    return HttpResponse(hello)

# def homepage(request):
#     return render(request, 'homepage.html')

#Allows the User to log in to let the User access AddFlightPlan(View) funcionality.
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('add_flight_plan')
        else:
            message = "Login or password incorrect"
            return render(request, 'login.html', {'message' : message})

#Gives the User posibility to log out from the app
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


#Main function of the program. Allows the User to submit a flight plan after the User filled the form.
@method_decorator(login_required, name='get')
class AddFlightPlan(View):
    def get(self, request):
        aircraft_types = Aircraft.objects.all()
        airports = Airport.objects.all()
        return render(request, 'add_flight_plan.html', {'aircraft_types': aircraft_types, 'airports':airports})

    def post(self, request):

        aircraft_id = request.POST.get('aircraft')
        aircraft_instance = get_object_or_404(Aircraft, pk=aircraft_id)

        departure_airport_id = request.POST.get('departure_airport')
        arrival_airport_id = request.POST.get('arrival_airport')
        departure_time = request.POST.get('departure_time')
        arrival_time = request.POST.get('arrival_time')
        flight_number = request.POST.get('flight_number')
        flight_type_id = request.POST.get('flight_type')

        flight_type_instance = get_object_or_404(FlightType, pk=flight_type_id)

        departure_airport_instance = get_object_or_404(Airport, pk=departure_airport_id)
        arrival_airport_instance = get_object_or_404(Airport, pk=arrival_airport_id)

        user = request.user

        flightplan = Flight(
            flight_number=flight_number,
            aircraft=aircraft_instance,
            flight_type=flight_type_instance,
            departure_airport=departure_airport_instance,
            departure_time=departure_time, #czy nie trzeba tego dodac do modelu flightnumber?
            arrival_airport=arrival_airport_instance,
            arrival_time=arrival_time,  #czy nie trzeba tego dodac do modelu flightnumber?
            user=user
            )

        flightplan.save()

        successfully_submitted = "Flightplan submitted!"

        return render(request, 'add_flight_plan.html', {'successfully_submitted': successfully_submitted})


#Allows the User to add an airport to the database basing on the filled form.
class AddAirport(View):
    def get(self, request):
        return render(request, 'add_airport.html')

    def post(self, request):

        name = request.POST.get('name')
        icao_code = request.POST.get('icao_code')
        runway_length = request.POST.get('runway_length')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        fuel_availability = request.POST.get('fuel_availability')

        airport = Airport(
            name = name,
            icao_code = icao_code,
            runway_length = runway_length,
            latitude = latitude,
            longitude = longitude,
            fuel_availability = bool(fuel_availability)
            )
        airport.save()

        successfully_added = "Airport added!"

        return render(request, 'add_airport.html', {'successfully_added' : successfully_added})

#Allows the User to add an aircraft to the database basing on the filled form.
class AddAircraft(View):
    def get(self, request):
        return render(request, 'add_aircraft.html')

    def post(selfs, request):

        name = request.POST.get('name')
        flight_range = request.POST.get('flight_range')
        takeoff_runway_length_required = request.POST.get('takeoff_runway_length_required')
        landing_runway_length_required = request.POST.get('landing_runway_length_required')

        aircraft = Aircraft(
            name=name,
            flight_range=flight_range,
            takeoff_runway_length_required=takeoff_runway_length_required,
            landing_runway_length_required=landing_runway_length_required,
            )

        aircraft.save()

        successfully_added = "Aircraft added!"

        return render(request, 'add_aircraft.html', {'successfully_added': successfully_added})

#Allows the User to view list of airports from the database.
class AirportList(View):
    def get(self, request):
        airports = Airport.objects.all()
        return render(request, 'airports_list.html', {'airports': airports})

#Allows the User to view list of aircrafts from the database.
class AircraftList(View):
    def get(self, request):
        aircrafts = Aircraft.objects.all()
        return render(request, 'aircrafts_list.html', {'aircrafts': aircrafts})

#Allows the User to view list of submitted flights from the database. The flights were submitted using AddFlightPlan(View).
class FlightList(View):
    def get(self, request):
        flights = Flight.objects.all()
        return render(request, 'flights_list.html', {'flights': flights})