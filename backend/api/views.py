from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from api.permissions import AuthorOrReadOnly
from api.serializers import (CustomUserSerializer, FavoritedSerializer,
                             IngredientSerializer, RecipeSerializer,
                             ShoppingCartSerializer, TagSerializer,
                             UserSubscribeSerializer)
from api.services import get_shopping_list
from recipes.filters import RecipeFilter
from recipes.models import (FavoriteRecipe, Ingredient,
                            Recipe, ShoppingCart, Tag)
from users.models import CustomUser, Follow

User = CustomUser()


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'actioned':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        followed = get_object_or_404(CustomUser, id=id)
        follower = request.user

        if request.method == 'GET':
            subscribed = (Follow.objects.filter(
                author=followed, user=follower).exists()
            )
            if subscribed is True:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.get_or_create(
                user=follower,
                author=followed
            )
            serializer = UserSubscribeSerializer(
                context=self.get_serializer_context()
            )
            return Response(serializer.to_representation(
                instance=followed),
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            Follow.objects.filter(
                user=follower,
                author=followed
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        current_user = request.user
        followed_list = CustomUser.objects.filter(followed__user=current_user)
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'limit'
        authors = paginator.paginate_queryset(
            followed_list,
            request=request
        )
        serializer = ListSerializer(
            child=UserSubscribeSerializer(),
            context=self.get_serializer_context()
        )
        return paginator.get_paginated_response(
            serializer.to_representation(authors)
        )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = RecipeFilter
    serializer_class = RecipeSerializer
    permission_classes = [AuthorOrReadOnly]

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path='favorite'
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
            favorite_recipe, created = FavoriteRecipe.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if created is True:
                serializer = FavoritedSerializer()
                return Response(
                    serializer.to_representation(instance=favorite_recipe),
                    status=status.HTTP_201_CREATED
                )
        if request.method == 'DELETE':
            FavoriteRecipe.objects.filter(
                user=user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
            recipe, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = ShoppingCartSerializer()
                return Response(
                    serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в корзине покупок'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        try:
            return get_shopping_list(request)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
