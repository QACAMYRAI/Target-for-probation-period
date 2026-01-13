import pytest
import allure
from api.api_methods import API
from pages.base_page import BasePage


@allure.story('API тесты')
@allure.suite('Блок User')
class TestStoreAPI:
    def setup_method(self):
        self.api_methods = API()
        self.base_methods = BasePage()
        self.created_users = []

    def teardown_method(self):
        for user_data in self.created_users:
            try:
                username = user_data.get('username')
                if username:
                    self.api_methods.delete_user_info_by_api(username)
            except Exception:
                pass
        self.created_users.clear()


    @allure.tag("ТК-1")
    @allure.severity(severity_level='normal')
    @allure.title('Создание пользователя')
    @pytest.mark.parametrize(
        'user_id, username, first_name, last_name, email, password, phone, user_status, status_code',
        [
            pytest.param(None, "testuser", "Иван", "Иванов", "ivan@test.com", "password123", "+79991234567", 0, 200,
                         marks=[allure.tag("ТК-2")]),
            pytest.param(1001, "john_doe", "John", "Doe", "john@example.com", "qwerty123", "88005553535", 1, 200,
                         marks=[allure.tag("ТК-3")]),
            pytest.param(None, None, None, None, None, None, None, None, 200,
                         marks=[allure.tag("ТК-4")]),
            pytest.param(None, "user_no_phone", "Анна", "Смирнова", "anna@test.com", "pass123", None, 0, 200,
                         marks=[allure.tag("ТК-5")]),
            pytest.param(None, "a", "Short", "User", "short@test.com", "pwd", "123", 0, 200,
                         marks=[allure.tag("ТК-6")]),
            pytest.param(None, "user.name_with.dots", "Name With", "Spaces", "user+tag@domain.com", "p@ssw0rd!",
                         "+7 (999) 123-45-67", 0, 200,
                         marks=[allure.tag("ТК-7")]),
            pytest.param(None, "status_zero", "Zero", "Status", "zero@test.com", "password", "1111111111", 0, 200,
                         marks=[allure.tag("ТК-8")]),
            pytest.param(None, "status_one", "One", "Status", "one@test.com", "password", "2222222222", 1, 200,
                         marks=[allure.tag("ТК-9")]),
            pytest.param(None, "", "Empty", "Username", "empty@test.com", "pass", "4444444444", 0, 400,
                         marks=[allure.tag("ТК-10")]),
            pytest.param(None, "invalid_email_user", "Invalid", "Email", 111, "password", "6666666666", 0,
                         400,
                         marks=[allure.tag("ТК-11")]),
            pytest.param(None, "x" * 50, "A" * 100, "B" * 100, "long_" + "x" * 100 + "@test.com", "p" * 50, "1" * 30, 0,
                         200,
                         marks=[allure.tag("ТК-12")]),
            pytest.param(None, "phone_formats", "Phone", "Formats", "phone@test.com", "password", "+7-999-123-45-67", 0,
                         200,
                         marks=[allure.tag("ТК-13")]),
            pytest.param(None, "negative_status", "Negative", "Status", "negative@test.com", "password", "7777777777",
                         -1, 200,
                         marks=[allure.tag("ТК-14")]),
        ]
    )
    def test_create_user(self, user_id, username, first_name, last_name, email, password, phone, user_status,
                         status_code):
        self.api_methods.create_user_by_api(user_id, username, first_name,
                                            last_name, email, password, phone,
                                            user_status, status_code=status_code)


    @allure.tag("ТК-15")
    @allure.severity(severity_level='normal')
    @allure.title('Обновление пользователя')
    @pytest.mark.parametrize(
        'field, value',
        [
            pytest.param('username', 'newuser', marks=[allure.tag("ТК-16")]),
            pytest.param('firstName', 'НовоеИмя', marks=[allure.tag("ТК-17")]),
            pytest.param('lastName', 'НоваяФамилия', marks=[allure.tag("ТК-18")]),
            pytest.param('email', 'new@email.com', marks=[allure.tag("ТК-19")]),
            pytest.param('password', 'newpass', marks=[allure.tag("ТК-20")]),
            pytest.param('phone', '1234567890', marks=[allure.tag("ТК-21")]),
            pytest.param('userStatus', 1, marks=[allure.tag("ТК-22")]),
        ]
    )
    def test_update_user_single_field(self, field, value):
        response, user = self.api_methods.create_user_by_api()
        self.created_users.append(user)
        old_data = self.api_methods.get_user_info_by_api(user['username']).json()
        update_payload = old_data.copy()
        update_payload[field] = value
        self.api_methods.updated_user_by_api(user['username'], *update_payload.values())
        new_username = value if field == 'username' else user['username']
        new_data = self.api_methods.get_user_info_by_api(new_username).json()
        self.base_methods.check_for_no_equality_two_variables(old_data, new_data)


    @allure.tag("ТК-23")
    @allure.severity(severity_level='normal')
    @allure.title('Тест удаления пользователя')
    def test_delete_user_info(self):
        response, user = self.api_methods.create_user_by_api()
        self.api_methods.delete_user_info_by_api(user['username'])
        self.api_methods.get_user_info_by_api(user['username'], status_code=404)


    @allure.tag("ТК-24")
    @allure.severity(severity_level='normal')
    @allure.title('Тест неудачного удаления пользователя')
    @pytest.mark.parametrize(
        'user_name, status_code',
        [
            pytest.param('non_existing_user_123', 404, marks=[allure.tag("ТК-25")]),
            pytest.param('', 405, marks=[allure.tag("ТК-26")]),
            pytest.param('user with spaces', 404, marks=[allure.tag("ТК-27")]),
        ]
    )
    def test_wrong_delete_user_info(self, user_name, status_code):
        response, user = self.api_methods.create_user_by_api()
        self.created_users.append(user)
        self.api_methods.delete_user_info_by_api(user_name, status_code=status_code)
        self.api_methods.get_user_info_by_api(user['username'], status_code=200)


    @allure.tag("ТК-28")
    @allure.severity(severity_level='normal')
    @allure.title('Тест логин/логаут пользователя')
    def test_login_logout_user(self):
        response, user = self.api_methods.create_user_by_api()
        self.created_users.append(user)
        self.api_methods.user_login_by_api(user['username'], user['password'])
        self.api_methods.user_logout_by_api()


    @allure.tag("ТК-29")
    @allure.severity(severity_level='normal')
    @allure.title('Тест добавления пользователей списком')
    def test_add_users_with_list(self):
        response, data = self.api_methods.create_users_with_list_by_api()
        for user in data:
            self.created_users.append(user)
            self.api_methods.get_user_info_by_api(user['username'])
            self.api_methods.delete_user_info_by_api(user['username'])


    @allure.tag("ТК-30")
    @allure.severity(severity_level='normal')
    @allure.title('Тест добавления пользователей массивом')
    def test_add_users_with_array(self):
        response, data = self.api_methods.create_users_with_array_by_api()
        for user in data:
            self.created_users.append(user)
            self.api_methods.get_user_info_by_api(user['username'])
            self.api_methods.delete_user_info_by_api(user['username'])