import pytest
from django.test import TestCase
from PlanowanieLotow.views import Login, AddAircraft
from django.test import Client
from django.urls import reverse
from PlanowanieLotow.models import Airport, Aircraft, Flight
from django.contrib.auth.models import User
from django.test import TestCase

@pytest.mark.django_db
def test_add_aircraft():
    client = Client()
    url = reverse('add_aircraft')

    post_content = {
        'name': 'Test',
        'flight_range': '5555',
        'takeoff_runway_length_required': '2222',
        'landing_runway_length_required': '1111',
    }
    response = client.post(url, post_content)

    assert response.status_code == 200

    assert 'Aircraft added!' in str(response.content)

@pytest.mark.django_db
def test_add_airport():
    client = Client()
    url = reverse('add_airport')

    post_content = {
        'name': 'Test',
        'icao_code': 'XXXX',
        'runway_length': '1111',
        'latitude': '52.11111',
        'longitude' : '18.11111',
        'fuel_availability' : True
    }
    response = client.post(url, post_content)

    assert response.status_code == 200

    assert 'Airport added!' in str(response.content)

@pytest.mark.django_db
def test_airport_list():
    client = Client()
    url = reverse('airport_list')

    test_airport = Airport.objects.create(name='XXXX airport',
                                          icao_code='XXXX',
                                          runway_length='1111',
                                          latitude='52.11111',
                                          longitude='18.1111',
                                          fuel_availability=True
                                         )

    response = client.get(url)

    assert response.status_code == 200

    assert 'XXXX airport' in str(response.content)
    assert 'XXXX' in str(response.content)
    assert '1111' in str(response.content)


@pytest.mark.django_db
def test_aircraft_list():
    client = Client()
    url = reverse('aircraft_list')

    test_aircraft = Aircraft.objects.create(name='Test',
                                            flight_range='1111',
                                            takeoff_runway_length_required='2222',
                                            landing_runway_length_required='1111'
                                         )

    response = client.get(url)

    assert response.status_code == 200

    assert 'Test' in str(response.content)
    assert '1111' in str(response.content)

@pytest.mark.django_db
def test_add_flight_plan_access():
    client = Client()
    url = reverse('add_flight_plan')

    user = User.objects.create_user(username='test', password='test')
    client.login(username='test', password='test')

    response = client.get(url)

    assert response.status_code == 200
    assert 'Departure airport:' in str(response.content)



@pytest.mark.django_db
class LoginTestCase(TestCase):
    def test_login(self):
        url = reverse('login')

        user_credentials = {
            'username': 'test',
            'password': 'test',
        }

        User.objects.create_user(**user_credentials)

        response = self.client.post(url, user_credentials)

        self.assertRedirects(response, reverse('add_flight_plan'))

@pytest.mark.django_db
def test_logout():
    client = Client()

    user = User.objects.create_user(username='test', password='test')
    client.login(username='test', password='test')

    assert user.is_authenticated

    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert 'login' in response.url


@pytest.mark.django_db
def test_add_flight_plan_submitting():
    client = Client()
    url_login = reverse('login')
    url_add = reverse('add_flight_plan')

    user = User.objects.create_user(username='test', password='test')
    client.login(username='test', password='test')
    login_data = {
            'username': 'test',
            'password': 'test',
        }
    login_response = client.post(url_login, data=login_data)
    assert login_response.status_code == 302
    # response = client.post(url, login_data)

    # response = client.get(reverse('add_flight_plan'))

    flighta = {
            'flight_number': '1111',
            'aircraft': '1',
            'flight_type': 'cargo',
            'departure_airport': 'EPWA',
            'departure_time': '2023-09-14 12:00:00',
            'arrival_airport': 'KJFK',
            'arrival_time': '2023-09-14 13:00:00',
            'user': user.id
        }

    response = client.post(url_add, flighta)
    # assert 'Flightplan submitted!' in str(response.content)
    assert response.status_code == 200

    # assert 'Flightplan submitted!' in str(response.content)
    # assert Flight.objects.filter(flight_number='1111').exists()
