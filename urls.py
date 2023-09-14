"""
URL configuration for projektKoncowy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PlanowanieLotow.views import hello_world, Login, Logout, AddFlightPlan, AddAirport, AirportList, AddAircraft, AircraftList, FlightList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    # path('', homepage),
    path('add_flight_plan/', AddFlightPlan.as_view()),
    path('add_airport/', AddAirport.as_view(), name='add_airport'),
    path('airport_list/', AirportList.as_view()),
    path('add_aircraft/', AddAircraft.as_view(), name='add_aircraft'),
    path('aircraft_list/', AircraftList.as_view()),
    path('flights_list/', FlightList.as_view())
]

