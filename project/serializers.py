from rest_framework import serializers
from project.models import Project
from django.db import IntegrityError


class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, allow_blank=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["founder", "created_at", "updated_at", "is_active"]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "A project with this title already exists for this founder."
                    ]
                }
            )
