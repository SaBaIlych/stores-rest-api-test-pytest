import pytest
from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel
import json


@pytest.mark.system
@pytest.mark.usefixtures("setup_app", "setup_tests_system_item")
class ItemTests():
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                expected_status_code = 401

                actual_status_code = resp.status_code
                
                assert actual_status_code == expected_status_code

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers = {'Authorization': self.access_token})
                expected_status_code = 404

                actual_status_code = resp.status_code

                assert actual_status_code == expected_status_code

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()
                resp = client.get('/item/test', headers = {'Authorization': self.access_token})
                expected_status_code = 200

                actual_status_code = resp.status_code

                assert actual_status_code == expected_status_code

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()
                resp = client.delete('/item/test')
                expected_status_code = 200
                expected_message = {'message': 'Item deleted'}

                actual_status_code = resp.status_code
                actual_message = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_message == expected_message

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', json={'price': 100, 'store_id': 1})
                expected_status_code = 201
                expected_payload = {'name': 'test', 'price': 100}

                actual_status_code = resp.status_code
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_payload == expected_payload

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', json={'price': 100, 'store_id': 1})
                resp = client.post('/item/test', json={'price': 100, 'store_id': 1})
                expected_status_code = 400
                expected_message = {'message': "An item with name 'test' already exists."}

                actual_status_code = resp.status_code
                actual_message = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_message == expected_message

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', json={'price': 100, 'store_id': 1})
                expected_status_code = 200
                expected_price = 100
                expected_payload = {'name': 'test', 'price': 100}

                actual_status_code = resp.status_code
                actual_price = json.loads(resp.data)['price']
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_price == expected_price
                assert actual_payload == expected_payload
                
    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()
                expected_price_before_update = 100
                expected_status_code = 200
                expected_price_after_update = 50
                expected_payload_after_update = {'name': 'test', 'price': 50}

                actual_price_before_update = ItemModel.find_by_name('test').price

                assert actual_price_before_update == expected_price_before_update

                resp = client.put('/item/test', json={'price': 50, 'store_id': 1})
                actual_status_code = resp.status_code
                actual_price_after_update = ItemModel.find_by_name('test').price
                actual_payload_after_update = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_price_after_update == expected_price_after_update
                assert actual_payload_after_update == expected_payload_after_update

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()
                resp = client.get('/items')
                expected_status_code = 200
                expected_payload = {'items': [{'name': 'test', 'price': 100}]}

                actual_status_code = resp.status_code
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_payload == expected_payload


@pytest.mark.system
@pytest.mark.usefixtures("setup_app", "setup_tests")
class StoreTests():
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')
                expected_status_code = 201
                expected_payload = {'name': 'test', 'items': []}

                actual_status_code = resp.status_code
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_payload == expected_payload
                assert StoreModel.find_by_name('test')

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                resp = client.post('/store/test')
                expected_status_code = 400
                expected_message = {'message': "A store with name 'test' already exists."}

                actual_status_code = resp.status_code
                actual_message = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_message == expected_message           

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.delete('/store/test')
                expected_status_code = 200
                expected_message = {'message': 'Store deleted'}

                actual_status_code = resp.status_code
                actual_message = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_message == expected_message

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')
                expected_status_code = 200
                expected_payload = {'name': 'test', 'items': []}

                actual_status_code = resp.status_code
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_payload == expected_payload

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test')
                expected_status_code = 404
                expected_message = {'message': 'Store not found'}

                actual_status_code = resp.status_code
                actual_message = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_message == expected_message

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test name', 100, 1).save_to_db()
                resp = client.get('/store/test')
                expected_status_code = 200
                expected_payload = {'name': 'test', 'items': [{'name': 'test name', 'price': 100}]}

                actual_status_code = resp.status_code
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_payload == expected_payload

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/stores')
                expected_status_code = 200
                expected_payload = {'stores': [{'name': 'test', 'items': []}]}

                actual_status_code = resp.status_code
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_payload == expected_payload

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test name', 100, 1).save_to_db()
                resp = client.get('/stores')
                expected_status_code = 200
                expected_payload = {'stores': [{'name': 'test', 'items': [{'name': 'test name', 'price': 100}]}]}

                actual_status_code = resp.status_code
                actual_payload = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_payload == expected_payload

@pytest.mark.system
@pytest.mark.usefixtures("setup_app", "setup_tests")
class UserTests():
    def test_register_user(self):
        with self.app() as client: 
            with self.app_context():
                resp = client.post('/register', json={'username': 'test', 'password': '1234'})
                expected_status_code = 201
                expected_message = {'message': 'User created successfully.'} 

                actual_status_code = resp.status_code
                actual_message = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_message == expected_message
                assert UserModel.find_by_username('test')            

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                auth_resp = client.post('/auth',
                                             json={'username': 'test', 'password': '1234'},
                                            headers = {'Content-Type': 'application/json'})
                expected_key_of_response = 'access_token'

                actual_key_of_response = json.loads(auth_resp.data).keys()

                assert expected_key_of_response in actual_key_of_response

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                resp = client.post('/register', json={'username': 'test', 'password': '1234'})
                expected_status_code = 400
                expected_message = {'message': 'A user with that username already exist'}

                actual_status_code = resp.status_code
                actual_message = json.loads(resp.data)

                assert actual_status_code == expected_status_code
                assert actual_message == expected_message
