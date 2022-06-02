from rest_framework.viewsets import ModelViewSet

from .serializers import NotesModelSerializer


class NotesAPIView(ModelViewSet):
    serializer_class = NotesModelSerializer

    def get_queryset(self):
        return self.request.user.notes.filter(is_active=True)
