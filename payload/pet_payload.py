from faker import Faker

class PetPayload:
    def __init__(self):
        self.faker = Faker()


    def create_pet_payload(self, pet_id: int = None,
                       name: str = None,
                       status: str = None,
                       category: str = None,
                       photo_urls: str = None,
                       tags: str = None,
                       remove_keys: str = None):
        payload = {
            "id": pet_id if pet_id is not None else self.faker.random_int(min=1, max=99999),
            "name": name if name is not None else self.faker.first_name(),
            "category": category if category is not None else {
                "id": self.faker.random_int(min=1, max=10),
                "name": self.faker.random_element(elements=("Dogs", "Cats", "Birds", "Fish", "Reptiles"))
            },
            "photoUrls": photo_urls if photo_urls is not None else [
                self.faker.image_url(width=200, height=200)
            ],
            "tags": tags if tags is not None else [
                {
                    "id": self.faker.random_int(min=0, max=10),
                    "name": self.faker.word()
                }
            ],
            "status": status if status is not None else self.faker.random_element(
                elements=("available", "pending", "sold")
            )
        }

        if remove_keys:
            keys_to_remove = [key.lower() for key in remove_keys]
            for key in list(payload.keys()):
                if key.lower() in keys_to_remove:
                    del payload[key]

        return payload


    def update_pet_payload(self, pet_id: int = None,
                       name: str = None,
                       status: str = None,
                       category: str = None,
                       photo_urls: str = None,
                       tags: str = None,
                       remove_keys: str = None):
        payload = {
            "id": pet_id,
            "name": name if name is not None else self.faker.first_name(),
            "category": category if category is not None else {
                "id": self.faker.random_int(min=1, max=10),
                "name": self.faker.random_element(elements=("Dogs", "Cats", "Birds", "Fish", "Reptiles"))
            },
            "photoUrls": photo_urls if photo_urls is not None else [
                self.faker.image_url(width=200, height=200)
            ],
            "tags": tags if tags is not None else [
                {
                    "id": self.faker.random_int(min=0, max=10),
                    "name": self.faker.word()
                }
            ],
            "status": status if status is not None else self.faker.random_element(
                elements=("available", "pending", "sold")
            )
        }

        if remove_keys:
            keys_to_remove = [key.lower() for key in remove_keys]
            for key in list(payload.keys()):
                if key.lower() in keys_to_remove:
                    del payload[key]

        return payload


    def create_pet_order_payload(self,
                                 pet_id: int,
                                 quantity: int = None,
                                 ship_date: str = None,
                                 status: str = 'placed',
                                 complete: bool = True,
                                 remove_keys: str = None):
        if ship_date is None:
            from datetime import datetime
            ship_date = datetime.utcnow().isoformat() + "Z"

        payload = {
            "id": 0,
            "petId": pet_id,
            "quantity": quantity if quantity is not None else self.faker.random_int(min=1, max=10),
            "shipDate": ship_date,
            "status": status,
            "complete": complete
        }

        if remove_keys:
            keys_to_remove = [key.lower() for key in remove_keys]
            for key in list(payload.keys()):
                if key.lower() in keys_to_remove:
                    del payload[key]

        return payload

