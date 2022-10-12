from app import app
from db import db
import pytest
from models.user import UserModel
import json


@pytest.fixture(scope="module")
def setup_app():
    global app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    app.config['DEBUG'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    with app.app_context():
        db.init_app(app)
    
@pytest.fixture(scope="function")
def setup_tests(request):
    global app
    with app.app_context():
        db.create_all()
    request.cls.app = app.test_client
    request.cls.app_context = app.app_context
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")    
def setup_tests_system_item(request):
    global app
    with app.app_context():
        db.create_all()
    request.cls.app = app.test_client
    request.cls.app_context = app.app_context
    with request.cls.app() as client:
            with request.cls.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                json={'username': 'test', 'password': '1234'},
                                headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                request.cls.access_token = f'JWT {auth_token}'
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()

    