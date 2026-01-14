import allure
import pytest
from api.api_methods import API


@allure.story('API тесты')
@allure.suite('Блок Store')
class TestStoreAPI:
    def setup_method(self):
        self.api_methods = API()
        self.created_pet_ids = []
        self.created_order_ids = []


    def teardown_method(self):
        for pet_id in self.created_pet_ids:
            try:
                self.api_methods.delete_pet_by_api(pet_id)
            except:
                pass
        for order_id in self.created_order_ids:
            try:
                self.api_methods.delete_pet_order_by_api(order_id)
            except:
                pass


    @allure.tag('ТК-37')
    @allure.severity(severity_level='normal')
    @allure.title('Тест получения карты кодов и количества')
    def test_get_map_of_status_code(self):
        self.api_methods.get_a_map_status_code_api().json()


    @allure.severity(severity_level='normal')
    @allure.title('Тест заказа питомца')
    @pytest.mark.parametrize('quantity, ship_date, status, complete, remove_keys, status_code',
                             [
                                 pytest.param(1, None, 'placed', True, None, 200,
                                              marks=[allure.tag('ТК-38')]),
                                 pytest.param(2, '2024-12-31T23:59:59.999Z', 'approved', True, None, 200,
                                              marks=[allure.tag('ТК-39')]),
                                 pytest.param(3, None, 'placed', False, None, 200,
                                              marks=[allure.tag('ТК-40')]),
                                 pytest.param(1, None, 'placed', True, ['id'], 200,
                                              marks=[allure.tag('ТК-41')]),
                                 pytest.param('sad', None, 'placed', True, None, 500,
                                              marks=[allure.tag('ТК-42')]),
                                 pytest.param(5, None, 'aced', True, None, 200,
                                              marks=[allure.tag('ТК-43')]),
                                 pytest.param(1, None, 'placed', True, 'quantity', 200,
                                              marks=[allure.tag('ТК-44')]),
                                 pytest.param(1, None, 'placed', True, 'petId', 200,
                                              marks=[allure.tag('ТК-45')]),
                                 pytest.param(1, None, 'placed', True, 'shipDate', 200,
                                              marks=[allure.tag('ТК-46')]),
                                 pytest.param(1, None, 'placed', True, 'status', 200,
                                              marks=[allure.tag('ТК-47')]),
                                 pytest.param(1, None, 'placed', True, 'complete', 200,
                                              marks=[allure.tag('ТК-48')]),
                                 pytest.param(1, '2023-01-01T00:00:00.000Z', 'placed', True, None, 200,
                                              marks=[allure.tag('ТК-49')]),
                                 pytest.param(1, '2030-12-31T23:59:59.999Z', 'placed', True, None, 200,
                                              marks=[allure.tag('ТК-50')]),
                                 pytest.param(1, '2024/12/31 23:59:59', 'placed', True, None, 500,
                                              marks=[allure.tag('ТК-51')]),
                                 pytest.param(1, '2024-12-31T23:59:59.999', 'placed', True, None, 200,
                                              marks=[allure.tag('ТК-52')]),
                                 pytest.param(1, '2025-06-15T12:30:00Z', 'delivered', False, None, 200,
                                              marks=[allure.tag('ТК-53')]),
                             ]
                             )
    def test_order_pet_by_api(self, quantity, ship_date, status, complete, remove_keys, status_code):
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet.json()['id']
        self.created_pet_ids.append(pet_id)
        self.api_methods.order_pet_by_api(pet_id, quantity,
                                          ship_date,
                                          status,
                                          complete,
                                          remove_keys,
                                          status_code).json()


    @allure.tag('ТК-54')
    @allure.severity(severity_level='normal')
    @allure.title('Тест удаления заказа')
    def test_delete_pet_order(self):
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet.json()['id']
        self.created_pet_ids.append(pet_id)
        order_id = self.api_methods.order_pet_by_api(pet_id).json()['id']
        self.created_order_ids.append(order_id)
        self.api_methods.delete_pet_order_by_api(order_id)
        self.api_methods.get_pet_order_by_api(order_id, status_code=404)