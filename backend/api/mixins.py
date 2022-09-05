from rest_framework import mixins, viewsets

from api.permissions import IsAuthorAdminOrReadOnly


class RetrieveListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthorAdminOrReadOnly,)
    pagination_class = None

