from api.permissions import IsAdminOrReadOnly


class PermissionAndPaginationMixin:
    """Миксин для списка тегов и ингридиентов."""

    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
