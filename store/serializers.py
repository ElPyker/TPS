from rest_framework import serializers
from .models import Price, Tribe, User, Item, Dino, Genetic, Combo, ComboDetail, Account, Session, SessionLog, Recipe, RecipeIngredient, Blueprint, BlueprintMaterial, SalePost
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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Dino
        fields = ['id', 'fullname', 'name', 'image', 'image_url', 'category', 'egg_type']

    def get_image_url(self, obj):
        """ Retorna la URL completa de la imagen """
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return None


class GeneticSerializer(serializers.ModelSerializer):
    dino_name = serializers.CharField(source='dino.fullname', read_only=True)
    tribe_name = serializers.CharField(source='tribe.name', read_only=True)

    class Meta:
        model = Genetic
        fields = [
            'id', 'dino', 'dino_name', 'tribe', 'tribe_name',
            'health_base', 'health_mutates',
            'stamina_base', 'stamina_mutates',
            'oxygen_base', 'oxygen_mutates',
            'food_base', 'food_mutates',
            'weight_base', 'weight_mutates',
            'damage_base', 'damage_mutates',
        ]

    def get_item_payment_image(self, obj):
        """ 🔹 Retorna la URL de la imagen del item de pago si existe """
        if obj.item_payment and obj.item_payment.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.item_payment.image.url)
        return None

class SalePostSerializer(serializers.ModelSerializer):
    genetic_data = GeneticSerializer(source='genetic', read_only=True)

    class Meta:
        model = SalePost
        fields = [
            'id', 'tribe', 'genetic', 'genetic_data',
            'title', 'description', 'discord_contact',
            'is_for_sale', 'payment_method', 'item_payment', 'price_amount'
        ]

class PriceSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    item_image = serializers.ImageField(source="item.image", read_only=True)

    class Meta:
        model = Price
        fields = ["id", "type", "amount", "item", "item_name", "item_image", "quantity"]

    def validate(self, data):
        """ Validar que Coins tenga amount y que Item tenga quantity e item """
        if data["type"] == "Coins":
            if data.get("amount") is None:
                raise serializers.ValidationError("Debe proporcionar un monto si el tipo es Coins.")
        elif data["type"] == "Item":
            if data.get("item") is None or data.get("quantity") is None:
                raise serializers.ValidationError("Debe proporcionar un item y cantidad si el tipo es Item.")
        return data


class ComboDetailSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())  # ✅ Solo acepta el ID
    item_name = serializers.CharField(source="item.name", read_only=True)
    item_image = serializers.ImageField(source="item.image", read_only=True)

    class Meta:
        model = ComboDetail
        fields = ["id", "item", "item_name", "item_image", "quantity"]



class ComboSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, required=False)
    details = ComboDetailSerializer(many=True, required=False)

    class Meta:
        model = Combo
        fields = ["id", "name", "description", "tribe", "is_available", "is_for_sale", "prices", "details"]

    def create(self, validated_data):
        prices_data = validated_data.pop("prices", [])
        details_data = validated_data.pop("details", [])

        combo = Combo.objects.create(**validated_data)

        # ✅ Guardar detalles correctamente con solo el ID del item
        for detail in details_data:
            ComboDetail.objects.create(combo=combo, item_id=detail["item"].id, quantity=detail["quantity"])

        # ✅ Guardar precios correctamente con solo el ID del item
        for price in prices_data:
            if price["type"] == "Item":
                Price.objects.create(combo=combo, type=price["type"], item_id=price["item"].id, quantity=price["quantity"])
            else:
                Price.objects.create(combo=combo, type=price["type"], amount=price["amount"])

        return combo

    def update(self, instance, validated_data):
        prices_data = validated_data.pop("prices", [])
        details_data = validated_data.pop("details", [])

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.is_available = validated_data.get("is_available", instance.is_available)
        instance.is_for_sale = validated_data.get("is_for_sale", instance.is_for_sale)
        instance.save()

        instance.details.all().delete()
        for detail in details_data:
            ComboDetail.objects.create(combo=instance, item_id=detail["item"], quantity=detail["quantity"])

        instance.prices.all().delete()
        for price in prices_data:
            if price["type"] == "Item":
                Price.objects.create(combo=instance, type=price["type"], item_id=price["item"], quantity=price["quantity"])
            else:
                Price.objects.create(combo=instance, type=price["type"], amount=price["amount"])

        return instance




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
    image = serializers.ImageField(required=False)  # Asegura que se incluya la imagen

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'stack', 'image'] 


class RecipeIngredientSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    recipe_name = serializers.CharField(source="recipe.name", read_only=True)
    item_image = serializers.SerializerMethodField()  # 🔹 Nuevo campo para la imagen

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'recipe_name', 'item', 'item_name', 'item_image', 'quantity']

    def get_item_image(self, obj):
        """ Devuelve la URL de la imagen del ingrediente (si tiene) """
        request = self.context.get('request')  # Para hacer la URL absoluta
        if obj.item.image:
            return request.build_absolute_uri(obj.item.image.url) if request else obj.item.image.url
        return None  # Si el item no tiene imagen




class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    output_item_name = serializers.CharField(source="output_item.name", read_only=True)
    output_item_image = serializers.ImageField(source="output_item.image", read_only=True)  

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'output_item', 'output_item_name', 'output_item_image', 'output_quantity', 'ingredients']
        read_only_fields = ['name']  # 🔹 Evita que se edite manualmente en la API




class BlueprintMaterialSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    item_image = serializers.ImageField(source="item.image", read_only=True)

    class Meta:
        model = BlueprintMaterial
        fields = ['id', 'blueprint', 'item', 'item_name', 'item_image', 'quantity']


class BlueprintSerializer(serializers.ModelSerializer):
    output_item_name = serializers.CharField(source="output_item.name", read_only=True)
    output_item_image = serializers.ImageField(source="output_item.image", read_only=True)
    name = serializers.SerializerMethodField()
    materials = BlueprintMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Blueprint
        fields = ['id', 'name', 'description', 'output_item', 'output_item_name', 'output_item_image', 'output_quantity', 'materials']

    def get_name(self, obj):
        return f"Blueprint {obj.output_item.name}"