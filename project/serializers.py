from rest_framework import serializers
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def to_internal_value(self, data):
        errors = {}
        if "title" in data:
            if not isinstance(data["title"], str):
                errors["title"] = ["이 필드는 문자열이어야 합니다."]
            else:
                data["title"] = data["title"].strip()
        if "description" in data:
            if not isinstance(data["description"], str):
                errors["description"] = ["이 필드는 문자열이어야 합니다."]
            else:
                data["description"] = data["description"].strip()

        if errors:
            raise serializers.ValidationError(errors)

        return super().to_internal_value(data)
