from rest_framework import serializers
from .models import Tribe, User, Item, Dino, Genetic, Combo, ComboDetail


class TribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribe
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


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
