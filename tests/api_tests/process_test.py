import allure
from api.api_methods import API
from pages.base_page import BasePage


@allure.story('API тесты')
@allure.suite('Блок User')
class TestProcessAPI:
    def setup_method(self):
        self.api_methods = API()
        self.base_methods = BasePage()
        self.created_pet_ids = []
        self.created_order_ids = []
        self.created_usernames = []

    def teardown_method(self):
        for order_id in self.created_order_ids:
            try:
                self.api_methods.delete_pet_order_by_api(order_id)
            except:
                pass

        for pet_id in self.created_pet_ids:
            try:
                self.api_methods.delete_pet_by_api(pet_id)
            except:
                pass

        for username in self.created_usernames:
            try:
                self.api_methods.delete_user_by_api(username)
            except:
                pass


    @allure.tag('ТК-82')
    @allure.severity(severity_level='normal')
    @allure.title('Процесс создание пользователя, вход, заказ питомца')
    def test_create_login_order(self):
        user = self.api_methods.create_user_by_api()[1]
        username = user['username']
        self.created_usernames.append(username)
        self.api_methods.get_user_info_by_api(username)
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet.json()['id']
        self.created_pet_ids.append(pet_id)
        self.api_methods.get_pet_by_api(pet_id)
        api_key = self.api_methods.user_login_by_api(username, user['password'])[1]
        order_response = self.api_methods.order_pet_by_api(pet_id, api_key=api_key)
        order_id = order_response.json()['id']
        self.created_order_ids.append(order_id)
        self.api_methods.get_pet_order_by_api(order_id).json()


    @allure.tag('ТК-83')
    @allure.severity(severity_level='normal')
    @allure.title('Процесс создание питомца, апдейт животного, заказ животного')
    def test_create_update_order(self):
        pet_response = self.api_methods.add_pet_by_api()
        pet = pet_response.json()
        pet_id = pet['id']
        self.created_pet_ids.append(pet_id)
        update_info, data = self.api_methods.update_pet_by_api(pet_id)
        self.base_methods.check_for_no_equality_two_variables(pet, update_info)
        self.base_methods.check_for_equality_two_variables(update_info.json(), data)
        user = self.api_methods.create_user_by_api()[1]
        username = user['username']
        self.created_usernames.append(username)
        self.api_methods.get_user_info_by_api(username)
        self.api_methods.get_pet_by_api(pet_id)
        apy_key = self.api_methods.user_login_by_api(username, user['password'])[1]
        order_response = self.api_methods.order_pet_by_api(pet_id, api_key=apy_key)
        order_id = order_response.json()['id']
        self.created_order_ids.append(order_id)
        self.api_methods.get_pet_order_by_api(order_id).json()


    @allure.tag('ТК-84')
    @allure.severity(severity_level='normal')
    @allure.title('Процесс вход в систему, заказ животного, удаление заказа')
    def test_login_order_delete_order(self):
        pet_response = self.api_methods.add_pet_by_api()
        pet = pet_response.json()
        pet_id = pet['id']
        self.created_pet_ids.append(pet_id)
        user = self.api_methods.create_user_by_api()[1]
        username = user['username']
        self.created_usernames.append(username)
        self.api_methods.get_user_info_by_api(username)
        self.api_methods.get_pet_by_api(pet_id)
        api_key = self.api_methods.user_login_by_api(username, user['password'])[1]
        order_response = self.api_methods.order_pet_by_api(pet_id, api_key=api_key)
        order_id = order_response.json()['id']
        self.created_order_ids.append(order_id)
        self.api_methods.get_pet_order_by_api(order_id)
        self.api_methods.delete_pet_order_by_api(order_id, api_key=api_key)
        self.api_methods.get_pet_order_by_api(order_id, status_code=404)
        if order_id in self.created_order_ids:
            self.created_order_ids.remove(order_id)