import os
import allure
from payload.pet_payload import PetPayload
from utils.sessions import main_url
import tests
from pathlib import Path
from model.pydentic_model import PetResponse, validate_with_pydantic, PetsListResponse


class API:
    @validate_with_pydantic(PetResponse)
    @allure.step('Добавление питомца по APi')
    def add_pet_by_api(self, pet_id: int = None,
                       name: str = None,
                       status: str = None,
                       category: str = None,
                       photo_urls: str = None,
                       tags: str = None,
                       remove_keys: str = None,
                       status_code: int = 200):
        data = PetPayload().create_pet_payload(pet_id, name, status, category, photo_urls, tags, remove_keys)
        response = main_url().post(f'pet',
                                   json=data,
                                   timeout=10,
                                   )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @validate_with_pydantic(PetResponse)
    @allure.step('Обновление информации о питомце по APi')
    def update_pet_by_api(self, pet_id: int,
                          name: str = None,
                          status: str = None,
                          category: str = None,
                          photo_urls: str = None,
                          tags: str = None,
                          remove_keys: str = None,
                          status_code: int = 200):
        data = PetPayload().update_pet_payload(pet_id, name, status, category, photo_urls, tags, remove_keys)
        response = main_url().put(f'pet',
                                  json=data,
                                  timeout=10,
                                  )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @validate_with_pydantic(PetResponse)
    @allure.step('Обновление информации о питомце через форму по APi')
    def update_pet_by_api_with_form_data(self, pet_id: int,
                          name: str = None,
                          status: str = None,
                          category: str = None,
                          photo_urls: str = None,
                          tags: str = None,
                          remove_keys: str = None,
                          status_code: int = 200):
        data = PetPayload().update_pet_payload(pet_id, name, status, category, photo_urls, tags, remove_keys)
        response = main_url().post(f'pet/{pet_id}',
                                   json=data,
                                   timeout=10,
                                   )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @validate_with_pydantic(PetResponse)
    @allure.step('Получить информацию о питомце по APi')
    def get_pet_by_api(self, pet_id: int, status_code: int = 200):
        response = main_url().get(f'pet/{pet_id}')
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @allure.step('Удалить информацию о питомце по APi')
    def delete_pet_by_api(self, pet_id: int, status_code: int = 200):
        response = main_url().delete(f'pet/{pet_id}')
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @validate_with_pydantic(PetsListResponse)
    @allure.step('Найти информацию о питомцах по статусам по API')
    def find_pet_with_status_by_api(self, status: str, status_code: int = 200):
        response = main_url().get(
            f'pet/findByStatus',
            params={'status': status}
        )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @allure.step('Найти информацию о питомцах по тегам по API')
    def find_pet_with_tag_by_api(self, tags:str, status_code: int = 200):
        response = main_url().get(
            f'pet/findByTags',
            params={'tags': tags}
        )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @allure.step('Загрузить фотографию питомца по API')
    def upload_pet_image_by_api(self, pet_id: int, file_path: str = None,
                                additional_metadata: str = None, status_code: int = 200):

        if file_path is None:
            file_path = Path(tests.__file__).parent.parent.joinpath('control_docs/images.jpeg')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        with open(file_path, 'rb') as file:
            file_data = file.read()

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/octet-stream'
        }

        params = {}
        if additional_metadata:
            params['additionalMetadata'] = additional_metadata

        response = main_url().post(
            f'pet/{pet_id}/uploadImage',
            headers=headers,
            params=params,
            data=file_data
        )

        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}\nТекст ответа: {response.text}'
        return response


    @allure.step('Получить карту соответствия кодов состояния к количеству API')
    def get_a_map_status_code_api(self, status_code: int = 200):
        response = main_url().get(
            f'store/inventory',
        )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


