import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--site_url',
        action='store',
        default='http://127.1.1.1:4000/',
        help="please specify service URL "
    )
    parser.addoption(
        '--api_url',
        action='store',
        default='http://127.1.1.1:4000/subscriptions',
        help="please specify API service URL "
    )


@pytest.fixture
def site_url(request):
    site_url = request.config.getoption("site_url")
    return site_url


@pytest.fixture
def api_url(request):
    api_url = request.config.getoption("api_url")
    return api_url
