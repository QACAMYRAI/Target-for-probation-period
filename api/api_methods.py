import allure
from payload.pet_payload import PetPayload
from utils.sessions import main_url
import tests
from pathlib import Path
from model.pydentic_model import PetResponse, validate_with_pydantic, PetsListResponse, InventoryModel, GetFormDataPet, \
    CreateOrderResponse


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


    @validate_with_pydantic(GetFormDataPet)
    @allure.step('Обновление информации о питомце через форму по API')
    def update_pet_by_api_with_form_data(self, pet_id: int,
                                         name: str,
                                         status: str,
                                         status_code: int = 200,
                                         remove_keys=''):
        data = {
            "name": name,
            "status": status
        }

        if remove_keys != "":
            for item in remove_keys:
                del data[item]
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = main_url().post(
            f'pet/{pet_id}',
            headers=headers,
            data=data,
            timeout=10,
        )

        assert response.status_code == status_code, (
            f'Статус код {response.status_code} не равен {status_code}\n'
            f'Текст ответа: {response.text}'
        )
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
            file_name = 'images.jpeg'
        else:
            file_name = str(file_path)

        control_docs_dir = Path(tests.__file__).parent.parent.joinpath('control_docs')
        file_path_full = control_docs_dir / file_name

        if not file_path_full.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path_full}")

        with open(file_path_full, 'rb') as file:
            files = {'file': (file_name, file, 'image/jpeg')}

            data = {}
            if additional_metadata is not None:
                data['additionalMetadata'] = str(additional_metadata)

            response = main_url().post(
                f'pet/{pet_id}/uploadImage',
                files=files,
                data=data
            )

        assert response.status_code == status_code, (
            f'Статус код {response.status_code} не равен {status_code}\n'
            f'Текст ответа: {response.text}'
        )

        return response

    @validate_with_pydantic(InventoryModel)
    @allure.step('Получить карту соответствия кодов состояния к количеству API')
    def get_a_map_status_code_api(self, status_code: int = 200):
        response = main_url().get(
            f'store/inventory',
        )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response

    @validate_with_pydantic(CreateOrderResponse)
    @allure.step('Заказ питомца по  APi')
    def order_pet_by_api(self, pet_id: int,
                               quantity: int = None,
                               ship_date: str = None,
                               status: str = 'placed',
                               complete: bool = True,
                               remove_keys: str = None,
                               status_code: int = 200):
        data = PetPayload().create_pet_order_payload(pet_id, quantity, ship_date, status, complete, remove_keys)
        response = main_url().post(f'store/order',
                                   json=data,
                                   timeout=10,
                                   )
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response


    @allure.step('Удалить заказ по APi')
    def delete_pet_order_by_api(self, order_id: str, status_code: int = 200):
        response = main_url().delete(f'store/order/{order_id}')
        assert response.status_code == status_code, (
            f'Статус код {response.status_code} не равен {status_code}\n'
            f'Текст ответа: {response.text}'
        )
        return response

    @validate_with_pydantic(CreateOrderResponse)
    @allure.step('Получить информацию о заказе питомца по APi')
    def get_pet_order_by_api(self, order_id: int, status_code: int = 200):
        response = main_url().get(f'store/order/{order_id}')
        assert response.status_code == status_code, f'Статус код {response.status_code} не равен {status_code}'
        return response