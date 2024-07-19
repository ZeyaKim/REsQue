from faker import Faker
from dev.test.fake_data.models.fake_model import FakeModel
from account.models import CustomUser


class FakeCustomUser(FakeModel):
    def __init__(self):
        super().__init__(CustomUser)

    def set_required_fields(self):
        return {"email": self._faker.email(), "password": self._faker.password()}
