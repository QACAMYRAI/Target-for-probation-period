import pytest
import allure
from pages.base_page import BasePage
from api.api_methods import API


@allure.story('API тесты')
@allure.suite('Блок Pet')
class TestApiPet:
    def setup_method(self):
        """Инициализация перед каждым тестом"""
        self.api_methods = API()
        self.base_methods = BasePage()
        self.created_pet_ids = []

    def teardown_method(self):
        """Очистка после каждого теста"""
        for pet_id in self.created_pet_ids:
            try:
                self.api_methods.delete_pet_by_api(pet_id)
            except Exception as e:
                print(f"Warning: Failed to delete pet {pet_id}: {e}")
                allure.attach(f"Cleanup error for pet {pet_id}: {str(e)}",
                              name="Cleanup Warning",
                              attachment_type=allure.attachment_type.TEXT)


    @allure.severity(severity_level='normal')
    @allure.title('Тесты добавления питомца')
    @pytest.mark.parametrize(
        "name, status, remove_keys, expected_code",
        [
            pytest.param("Барсик", "available", None, 200, marks=[allure.tag("ТК-1")]),
            pytest.param(None, "pending", None, 200, marks=[allure.tag("ТК-2")]),
            pytest.param("Шарик", None, None, 200, marks=[allure.tag("ТК-3")]),
            pytest.param(None, None, None, 200, marks=[allure.tag("ТК-4")]),

            pytest.param("Рекс", "available", ["category"], 200, marks=[allure.tag("ТК-5")]),
            pytest.param("Кеша", "available", ["photoUrls"], 200, marks=[allure.tag("ТК-6")]),
            pytest.param("Гав", "available", ["tags"], 200, marks=[allure.tag("ТК-7")]),
            pytest.param("Пушок", "available", ["category", "photoUrls", "tags"], 200, marks=[allure.tag("ТК-8")]),

            pytest.param("", "available", None, 200, marks=[allure.tag("ТК-9")]),
            pytest.param("   ", "available", None, 200, marks=[allure.tag("ТК-10")]),
            pytest.param("Тест", "invalid_status", None, 200, marks=[allure.tag("ТК-11")]),

            pytest.param("", "available", ["category"], 200, marks=[allure.tag("ТК-12")]),
            pytest.param("Тест", "wrong", ["photoUrls"], 200, marks=[allure.tag("ТК-13")])
        ]
    )
    def test_add_new_pet(self, name, status, remove_keys, expected_code):
        response = self.api_methods.add_pet_by_api(
            pet_id=None,
            name=name,
            status=status,
            category=None,
            photo_urls=None,
            tags=None,
            remove_keys=remove_keys,
            status_code=expected_code
        )
        if expected_code == 200 and 'id' in response:
            self.created_pet_ids.append(response['id'])


    @allure.severity(severity_level='normal')
    @allure.title('Тесты обновление информации о питомце')
    @pytest.mark.parametrize(
        "name, status, remove_keys, status_code",
        [
            pytest.param("НовоеИмя", "sold", None, 200, marks=[allure.tag("ТК-14")]),
            pytest.param(None, "pending", None, 200, marks=[allure.tag("ТК-15")]),
            pytest.param("Имя", None, None, 200, marks=[allure.tag("ТК-16")]),
            pytest.param("Имя", "available", ["category"], 200, marks=[allure.tag("ТК-17")]),
            pytest.param("Имя", "available", ["photoUrls", "tags"], 200, marks=[allure.tag("ТК-18")]),
            pytest.param("", "available", None, 200, marks=[allure.tag("ТК-19")]),
            pytest.param("Тест", "invalid", None, 200, marks=[allure.tag("ТК-20")]),
        ]
    )
    def test_update_pet_info(self, name, status, remove_keys, status_code):
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet.json()['id']
        self.created_pet_ids.append(pet_id)
        old_info = self.api_methods.get_pet_by_api(pet_id).json()
        update_info = self.api_methods.update_pet_by_api(pet_id,
                                                         name=name,
                                                         status=status,
                                                         remove_keys=remove_keys,
                                                         status_code=status_code
                                                         ).json()
        new_pet_info = self.api_methods.get_pet_by_api(pet_id).json()
        self.base_methods.check_for_no_equality_two_variables(old_info, update_info)
        self.base_methods.check_for_equality_two_variables(update_info, new_pet_info)


    @allure.tag("ТК-21")
    @allure.severity(severity_level='normal')
    @allure.title('Тесты получение информации о питомце')
    def test_get_pet_info(self):
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet.json()['id']
        self.created_pet_ids.append(pet_id)
        update_info = self.api_methods.update_pet_by_api(pet_id).json()
        new_pet_info = self.api_methods.get_pet_by_api(pet_id).json()
        self.base_methods.check_for_equality_two_variables(update_info, new_pet_info)


    @allure.tag("ТК-22")
    @allure.severity(severity_level='normal')
    @allure.title('Тесты удаление информации о питомце')
    def test_delete_pet_info(self):
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet.json()['id']
        self.api_methods.delete_pet_by_api(pet_id)
        self.api_methods.get_pet_by_api(pet_id, status_code=404)


    @allure.severity(severity_level='normal')
    @allure.title('Тесты фильтрация питомцев по статусу')
    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("available", marks=[allure.tag("ТК-23")]),
            pytest.param("pending", marks=[allure.tag("ТК-24")]),
            pytest.param("sold", marks=[allure.tag("ТК-25")])
        ]
    )
    def test_filter_by_status_pet_info(self, status):
        pet_list = self.api_methods.find_pet_with_status_by_api(status).json()
        self.base_methods.check_all_have_key(pet_list, "status", status)

    @allure.tag("ТК-26")
    @allure.severity(severity_level='normal')
    @allure.title('Тесты фильтрация питомцев по тегам')
    @pytest.mark.skip(reason="Не работает метод со стороны API")
    def test_filter_by_tags_pet_info(self):
        pet_list = self.api_methods.find_pet_with_tag_by_api('string').json()
        self.base_methods.check_all_have_key(pet_list, "string", 'string')


    @allure.severity(severity_level='normal')
    @allure.title('Тесты обновление информации о питомце на основе данных из формы')
    @pytest.mark.skip(reason="Не работает метод со стороны API")
    @pytest.mark.parametrize(
        "name, status, remove_keys, status_code",
        [
            pytest.param("НовоеИмя", "sold", None, 200, marks=[allure.tag("ТК-27")]),
            pytest.param(None, "pending", None, 200, marks=[allure.tag("ТК-28")]),
            pytest.param("Имя", None, None, 200, marks=[allure.tag("ТК-29")]),
            pytest.param("Имя", "available", ["category"], 200, marks=[allure.tag("ТК-30")]),
            pytest.param("Имя", "available", ["photoUrls", "tags"], 200, marks=[allure.tag("ТК-31")]),
            pytest.param("", "available", None, 200, marks=[allure.tag("ТК-32")]),
            pytest.param("Тест", "invalid", None, 200, marks=[allure.tag("ТК-33")]),
        ]
    )
    def test_update_pet_info_with_form_data(self, name, status, remove_keys, status_code):
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet['id']
        self.created_pet_ids.append(pet_id)
        old_info = self.api_methods.get_pet_by_api(pet_id).json()
        update_info = self.api_methods.update_pet_by_api_with_form_data(pet_id,
                                                                        name=name,
                                                                        status=status,
                                                                        remove_keys=remove_keys,
                                                                        status_code=status_code
                                                                        ).json()
        new_pet_info = self.api_methods.get_pet_by_api(pet_id).json()
        self.base_methods.check_for_no_equality_two_variables(old_info, update_info)
        self.base_methods.check_for_equality_two_variables(update_info, new_pet_info)


    @allure.tag("ТК-34")
    @allure.severity(severity_level='normal')
    @allure.title('Тесты загрузка изображения питомца')
    def test_upload_pet_image(self):
        pet = self.api_methods.add_pet_by_api()
        pet_id = pet.json()['id']
        self.created_pet_ids.append(pet_id)
        self.api_methods.upload_pet_image_by_api(pet_id).json()
        self.api_methods.get_pet_by_api(pet_id).json()


@allure.tag("ТК-35")
@allure.severity(severity_level='normal')
@allure.story('API тесты')
@allure.suite('Блок Store')
@allure.title('Тесты получение карты кодов и количества')
@pytest.mark.skip(reason="Не работает метод со стороны API")
def test_get_map_of_status_code():
    api_methods = API()
    api_methods.get_a_map_status_code_api()