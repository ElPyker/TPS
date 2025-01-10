from rest_framework import viewsets
from .models import Tribe, User, Item, Dino, Genetic, Combo, ComboDetail
from .serializers import (
    TribeSerializer, UserSerializer, ItemSerializer,
    DinoSerializer, GeneticSerializer, ComboSerializer, ComboDetailSerializer
)


class TribeViewSet(viewsets.ModelViewSet):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class DinoViewSet(viewsets.ModelViewSet):
    queryset = Dino.objects.all()
    serializer_class = DinoSerializer


class GeneticViewSet(viewsets.ModelViewSet):
    queryset = Genetic.objects.all()
    serializer_class = GeneticSerializer


class ComboViewSet(viewsets.ModelViewSet):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer


class ComboDetailViewSet(viewsets.ModelViewSet):
    queryset = ComboDetail.objects.all()
    serializer_class = ComboDetailSerializer
