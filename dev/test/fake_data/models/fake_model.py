import abc
from typing import Any, Type

from django.db.models import Model
from faker import Faker

fake = Faker()


class FakeModel(abc.ABC):
    def __init__(self, model: Type[Model]):
        self._faker = fake
        self._model = model
        self._instance: Model | None = None
        self._required_fields: dict[str, Any] | None = None

    @abc.abstractmethod
    def set_required_fields(self) -> dict[str, Any]:
        """
        하위 클래스에서 반드시 구현해야 하는 추상 메서드
        """
        pass

    @property
    def required_fields(self) -> dict[str, Any]:
        if self._required_fields is None:
            self._required_fields = self.set_required_fields()
        return self._required_fields

    @property
    def instance(self) -> Model:
        if self._instance is None:
            self._instance = self._model(**self.required_fields)
        return self._instance
