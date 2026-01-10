from typing import List, Optional
from pydantic import BaseModel, RootModel, field_validator, ConfigDict
from pydantic import ValidationError
import allure
import json
from functools import wraps


class Category(BaseModel):
    id: int
    name: str = ""


class Tag(BaseModel):
    id: int
    name: str = ""


class PetResponse(BaseModel):
    id: int
    name: str = ""
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
            response = func(self, *args, **kwargs)
            if response.status_code == 404:
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
                    result = [item.model_dump() for item in validated.root]
                else:
                    result = validated.model_dump()

                allure.attach(
                    json.dumps(result, indent=2, ensure_ascii=False),
                    name=f"Validated {model_class.__name__}",
                    attachment_type=allure.attachment_type.JSON
                )
                return response
            except ValidationError as e:
                allure.attach(
                    str(e.errors()),
                    name="Validation Errors",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(f"Ответ не соответствует схеме {model_class.__name__}: {e}")
            except json.JSONDecodeError as e:
                allure.attach(
                    response.text,
                    name="Invalid JSON Response",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(f"Ответ не является валидным JSON: {e}")

        return wrapper

    return decorator


class PetsListResponse(RootModel):
    root: List[PetResponse]