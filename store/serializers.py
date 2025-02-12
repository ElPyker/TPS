from rest_framework import serializers
from .models import Tribe, User, Item, Dino, Genetic, Combo, ComboDetail, Account, Session, SessionLog, Recipe, RecipeIngredient, Blueprint, BlueprintMaterial
from django.contrib.auth.hashers import make_password

class TribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribe
        fields = ['id', 'name']  # 🔹 Solo enviamos el nombre de la tribu


class UserSerializer(serializers.ModelSerializer):
    tribe_name = serializers.CharField(source="tribe.name", read_only=True)
    tribe = serializers.PrimaryKeyRelatedField(queryset=Tribe.objects.all(), allow_null=True, required=False)

    password = serializers.CharField(write_only=True, required=False, allow_blank=True)  # 🔹 `write_only` evita mostrarlo en GET

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tribe', 'tribe_name', 'role', 'is_active', 'is_superuser', 'is_staff', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # 🔹 Permite actualizar sin mostrarlo en GET

    def create(self, validated_data):
        """🔹 Encripta la contraseña antes de crear el usuario"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # 🔹 Encripta la contraseña correctamente
        else:
            raise serializers.ValidationError({"password": "Debe ingresar una contraseña."})
        user.save()
        return user

    def update(self, instance, validated_data):
        """🔹 Permite actualizar la contraseña si se proporciona"""
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)  # 🔹 Usa `make_password` para encriptar correctamente
        return super().update(instance, validated_data)

    def get_tribe_name(self, obj):
        return obj.tribe.name if obj.tribe else None  # 🔹 Si no tiene tribu, devuelve None



class DinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dino
        fields = '__all__'

class GeneticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genetic
        fields = '__all__'

class ComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = '__all__'

class ComboDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboDetail
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'short_code', 'tribe']
        read_only_fields = ['tribe']  # 🔹 Tribe no se debe enviar en el JSON del frontend




class SessionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='player.username', read_only=True)  # 🔹 Usa 'player' si aún no has cambiado a 'user'

    class Meta:
        model = Session
        fields = ['id', 'account', 'player', 'user_name', 'start_time', 'status', 'afk_text']


    def get_player_name(self, obj):
        return obj.player.nickname if obj.player else "uwu"

    def get_account_name(self, obj):
        return obj.account.name if obj.account else "uwu"


class SessionLogSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)  # 🔹 Cambia PlayerSerializer a UserSerializer
    account = AccountSerializer(read_only=True)

    class Meta:
        model = SessionLog
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['item', 'item_name', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    output_item_name = serializers.CharField(source="output_item.name", read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'output_item', 'output_item_name', 'output_quantity', 'ingredients']


class BlueprintMaterialSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = BlueprintMaterial
        fields = ['id', 'item', 'item_name', 'quantity']


class BlueprintSerializer(serializers.ModelSerializer):
    materials = BlueprintMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Blueprint
        fields = ['id', 'name', 'description', 'crafting_station', 'materials']