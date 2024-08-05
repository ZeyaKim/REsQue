from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    founder = models.ForeignKey(
        "account.CustomUser", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        unique_together = ["title", "founder"]

    def __str__(self):
        return self.title


class ProjectInvitation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        "account.CustomUser", on_delete=models.CASCADE, related_name="inviter"
    )
    invitee_email = models.EmailField()
