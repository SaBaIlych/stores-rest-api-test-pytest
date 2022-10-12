import pytest
from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel

@pytest.mark.integration
@pytest.mark.usefixtures("setup_app", "setup_tests")
class ItemTests:
    def test_crud(self):
        with self.app_context():
            StoreModel('test').save_to_db() # in case we use postgreSQL or MySQL that can applicate foreign key constraints 
            item = ItemModel('test', 19.99, 1)

            assert not ItemModel.find_by_name('test'), f"Found an item with name {item.name}, but expected not to."

            item.save_to_db()

            assert ItemModel.find_by_name('test'), f"Not found an item with name {item.name}, but expected to."

            item.delete_from_db()

            assert not ItemModel.find_by_name('test'), f"Found an item with name {item.name}, but expected not to."
        
    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test', 19.99, 1)
            expected_store_name = 'test_store'

            store.save_to_db()
            item.save_to_db()

            actual_store_name = item.store.name

            assert actual_store_name == expected_store_name


@pytest.mark.integration
@pytest.mark.usefixtures("setup_app", "setup_tests")
class StoreTests:
    def test_create_store_items_empty(self):
        store = StoreModel('test')
        expected_items_list = []

        actual_items_list = store.items.all()

        assert actual_items_list == expected_items_list, "The store items is not equal to the empty list"

    def test_crud(self):
        with self.app_context():    
            store = StoreModel('test')

            assert not StoreModel.find_by_name('test'), "Found a store with name 'test' even though it wasn't written to the database"

            store.save_to_db()

            assert StoreModel.find_by_name('test'), "Didn't found a store with name 'test even though it was written in database"

            store.delete_from_db()

            assert not StoreModel.find_by_name('test'), "Found a store with name 'test' even though it was delete from the database"

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 100, 1)
            expected_count_items = 1
            expected_item_name = 'test item'

            store.save_to_db()
            item.save_to_db()
            actual_count_items = store.items.count()
            actual_item_name = store.items.first().name

            assert actual_count_items == expected_count_items
            assert actual_item_name == expected_item_name

    def test_store_json_no_items(self):
        store = StoreModel('test')
        expected_json = {
            'name': 'test',
            'items': []
        }

        actual_json = store.json()

        assert actual_json == expected_json

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 100, 1)
            expected_json = {
                'name': 'test',
                'items': [
                    {
                        'name': 'test item',
                        'price': 100
                    }

                ]
            }

            store.save_to_db()
            item.save_to_db()
            actual_json = store.json()

            assert actual_json == expected_json


@pytest.mark.integration
@pytest.mark.usefixtures("setup_app", "setup_tests")
class UserTests:
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', '1234')
            expected_username = 'test'
            expected_id = 1

            assert not UserModel.find_by_username('test')
            assert not UserModel.find_by_id(1)

            user.save_to_db()
            actual_username = UserModel.find_by_username('test').username
            actual_id = UserModel.find_by_id(1).id

            assert actual_username == expected_username
            assert actual_id == expected_id