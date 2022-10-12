from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
import pytest

@pytest.mark.unit
class UserTests:
    def test_create_user(self):
        user = UserModel('test username', 'test password')
        expected_username = 'test username'
        expected_password = 'test password'

        actual_username = user.username
        actual_password = user.password

        assert actual_username == actual_username, 'The created user name not equal to expected.'
        assert actual_password == expected_password, 'The created user password not equal to expected.'


@pytest.mark.unit
class ItemTests:
    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)
        expected_name = 'test'
        expected_price = 19.99
        expected_store_id = 1

        actual_name = item.name
        actual_price = item.price
        actual_store_id = item.store_id

        assert actual_name == expected_name, "The name of the item after creation does not equal the constructor argument."
        assert actual_price == expected_price, "The price of the item after creation does not equal the constructor argument."
        assert actual_store_id == expected_store_id, "The store_id of the item after creation does not equal the constructor argument."
        assert not item.store
        
    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected_json = {
            'name': 'test',
            'price': 19.99
        }

        actual_json = item.json()

        assert actual_json == expected_json, f"The JSON export of the item is incorrect. Received {actual_json}, expected {expected_json}."


@pytest.mark.unit
class StoreTests:
    def test_create_store(self):
        store = StoreModel('test store')
        expected_name = 'test store'

        actual_name = store.name

        assert actual_name == expected_name, 'The name of the store after creation does not equal to the constructor argument.'
    