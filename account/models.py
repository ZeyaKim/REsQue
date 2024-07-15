from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager): ...


class CustomUser(AbstractBaseUser):
    def __str__(self):
        return self.uuid
