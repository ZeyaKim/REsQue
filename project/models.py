from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    founder = models.ForeignKey(
        "account.CustomUser", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title
