from typing import List, Optional, Dict
from pydantic import BaseModel, RootModel, field_validator, ConfigDict
from pydantic import ValidationError
import allure
import json
from functools import wraps



class CreateUser(BaseModel):
    code: int
    message: str
    type: str

    model_config = ConfigDict(extra='forbid')


class CreateOrderResponse(BaseModel):
    id: int
    petId: int
    quantity: int
    shipDate: str
    status: str
    complete: bool

    model_config = ConfigDict(extra='forbid')


class GetFormDataPet(BaseModel):
    code: int
    type: str
    message: str

    model_config = ConfigDict(extra='forbid')


class InventoryModel(RootModel[Dict[str, int]]):
    pass


class Category(BaseModel):
    id: int
    name: str = ''

    model_config = ConfigDict(extra='forbid')


class Tag(BaseModel):
    id: int
    name: str = ''

    model_config = ConfigDict(extra='forbid')


class PetResponse(BaseModel):
    id: int
    name: str = ''
    category: Optional[Category] = None
    photoUrls: List[str] = []
    tags: List[Tag] = []
    status: str

    model_config = ConfigDict(extra='forbid')


    @field_validator('photoUrls', mode='before')
    @classmethod
    def fix_photos(cls, v):
        if v is None:
            return []
        elif not isinstance(v, list):
            return [v]
        return [url for url in v if url is not None]

    @field_validator('tags', mode='before')
    @classmethod
    def fix_tags(cls, v):
        if v is None:
            return []
        if not isinstance(v, list):
            return []
        return [item for item in v if isinstance(item, dict)]


@allure.step('Валидация данных с помощью модели pydantic')
def validate_with_pydantic(model_class):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func_return = func(self, *args, **kwargs)
            if isinstance(func_return, tuple):
                response = func_return[0]
                data = func_return[1]
            else:
                response = func_return
            if response.status_code in (404, 500):
                return response

            try:
                json_data = response.json()
                if json_data == [] and issubclass(model_class, RootModel):
                    validated = model_class([])
                elif isinstance(json_data, list) and issubclass(model_class, RootModel):
                    validated = model_class(json_data)
                else:
                    validated = model_class.model_validate(json_data)
                if isinstance(validated, RootModel):
                    result = validated.model_dump()
                else:
                    result = validated.model_dump()

                allure.attach(
                    json.dumps(result, indent=2, ensure_ascii=False),
                    name=f'Validated {model_class.__name__}',
                    attachment_type=allure.attachment_type.JSON
                )
                if isinstance(func_return, tuple):
                    return response, data
                else:
                    return response
            except ValidationError as e:
                allure.attach(
                    str(e.errors()),
                    name='Validation Errors',
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(f'Ответ не соответствует схеме {model_class.__name__}: {e}')
            except json.JSONDecodeError as e:
                allure.attach(
                    response.text,
                    name='Invalid JSON Response',
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(f'Ответ не является валидным JSON: {e}')

        return wrapper

    return decorator


class PetsListResponse(RootModel):
    root: List[PetResponse]