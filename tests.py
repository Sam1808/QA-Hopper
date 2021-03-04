import pytest
import requests
import string
from ast import literal_eval
from datetime import datetime


def get_data():
    with open('load_data.txt', 'r') as file:
        data = file.read()
        data = data.split('\n')
        data = [literal_eval(element) for element in data]
    return data


@pytest.fixture
@pytest.mark.parametrize('test_data', get_data())
def create_subscrider(test_data, api_url):
    requests.delete(api_url)
    requests.post(api_url, json=test_data)


def test_site_status(site_url):
    response = requests.get(site_url)
    assert response.status_code == 200, 'Server is not available'


def test_api_site_status(api_url):
    response = requests.get(api_url)
    assert response.status_code == 200, 'Server API is not available'


def test_api_site_headers(api_url):
    response = requests.get(api_url)
    assert response.headers['Content-Type'] == "application/json", 'The headers of Server API is not JSON'


@pytest.mark.parametrize('test_data', get_data())
def test_delete_all_subscribers(create_subscrider, test_data, api_url):
    requests.delete(api_url)
    check_response = requests.get(api_url).json()
    assert len(check_response) == False, 'Should be zero entries'


@pytest.mark.parametrize('test_data', get_data())
def test_create_subscriber(create_subscrider, test_data, api_url):
    check_response = requests.get(api_url).json()

    assert len(check_response) == True, 'Should receive data'
    assert check_response[0]['email'] == test_data['email'], 'Sent EMAIL should be equal received EMAIL'
    assert check_response[0]['name'] == test_data['name'], 'Sent NAME should be equal received NAME'
    assert len(check_response[0]['name']) > 0, 'There is no Name of subscriber'


@pytest.mark.parametrize('test_data', get_data())
def test_subscribe_period(create_subscrider, test_data, api_url):
    print(test_data['comment'])
    check_response = requests.get(api_url).json()
    assert len(check_response) == True, 'Should receive data'

    subscribe_created_at = datetime.strptime(check_response[0]['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
    subscribe_expired_at = datetime.strptime(check_response[0]['expired_at'], '%Y-%m-%dT%H:%M:%S.%f')
    time = subscribe_expired_at - subscribe_created_at
    if test_data['time'].lstrip(string.digits).startswith('d'):
        assert test_data['time'].rstrip(string.ascii_letters) == str(time.days), 'Sent TIME should be equal received TIME'

    if test_data['time'].lstrip(string.digits).startswith('s'):
        assert test_data['time'].rstrip(string.ascii_letters) == str(time.seconds), 'Sent TIME should be equal received TIME'

    if test_data['time'].lstrip(string.digits).startswith('m'):
        assert test_data['time'].rstrip(string.ascii_letters) == str(time.seconds // 60), 'Sent TIME should be equal received TIME'

    assert int(time.total_seconds()) > 0, 'The TIME should be greater than zero'
