import traceback

from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer
)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    IngredientsRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    TagsRecipe
)
from users.mixins import IsSubscribedMixin
from users.models import Follow

User = get_user_model()


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserListSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    username = serializers.CharField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User


class UserSubscribeSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    username = serializers.CharField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
            'is_subscribed'
        )

    def validate(self, data):
        author = data['followed']
        user = data['follower']
        if user == author:
            raise serializers.ValidationError('You can`t follow for yourself!')
        if Follow.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError('You have already subscribed!')
        return data

    def create(self, validated_data):
        subscribe = Follow.objects.create(**validated_data)
        subscribe.save()
        return subscribe

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        if recipes_limit is None:
            recipes = obj.recipes.all()
        else:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        serializer = serializers.ListSerializer(child=RecipeSerializer())
        return serializer.to_representation(recipes)

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name'
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'slug'


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(
        read_only=True,
        many=True
    )
    ingredients = IngredientsRecipeSerializer(
        many=True,
        source='recipe_ingredients'
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(
        max_value=32767,
        min_value=1
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def get_status_func(self, data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = self.context.get('request').user
        callname_function = format(traceback.extract_stack()[-2][2])
        if callname_function == 'get_is_favorited':
            return FavoriteRecipe.objects.filter(
                recipe=data.id,
                user=user
            )
        elif callname_function == 'get_is_in_shopping_cart':
            return ShoppingCart.objects.filter(
                recipe=data,
                user=user
            )
        else:
            return False

    def get_is_favorited(self, data):
        return self.get_status_func(data)

    def get_is_in_shopping_cart(self, data):
        return self.get_status_func(data)

    def create(self, validated_data):
        context = self.context['request']
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context.get('request').user
        )
        tags_set = context.data['tags']
        for tag in tags_set:
            TagsRecipe.objects.create(
                recipe=recipe,
                tag=Tag.objects.get(id=tag)
            )
        ingredients_set = context.data['ingredients']
        for ingredient in ingredients_set:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientsRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient_model,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        context = self.context['request']
        tags_set = context.data['tags']
        recipe = instance
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.tags.set(tags_set)
        IngredientsRecipe.objects.filter(recipe=instance).delete()
        ingredients_req = context.data['ingredients']
        for ingredient in ingredients_req:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientsRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient_model,
                amount=ingredient['amount']
            )
        return instance

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class FavoritedSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
        source='recipe.id'
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time'
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image'
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name'
    )

    def validate(self, data):
        recipe = data['recipe']
        user = data['user']
        if user == recipe.author:
            raise serializers.ValidationError('You are the author!')
        if FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError('You have already subscribed!')
        return data

    def create(self, validated_data):
        favorite = FavoriteRecipe.objects.create(**validated_data)
        favorite.save()
        return favorite

    class Meta:
        model = FavoriteRecipe
        fields = (
            'id',
            'cooking_time',
            'name',
            'image'
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
        source='recipe.id'
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time'
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image'
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name'
    )

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'cooking_time',
            'name',
            'image'
        )
