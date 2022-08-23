from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    UsersViewSet,
    IngredientsViewSet,
    RecipeViewSet,
    TagsViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')

subscriptions = UsersViewSet.as_view({'get': 'subscriptions', })


urlpatterns = [
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
