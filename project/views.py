from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from project.models import Project
from project.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(founder=self.request.user)
