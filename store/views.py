from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from .models import Tribe, User, Item, Dino, Genetic, Combo, ComboDetail, Account, Session, SessionLog, Recipe, RecipeIngredient, Blueprint, BlueprintMaterial, SalePost
from .serializers import (
    TribeSerializer, UserSerializer, ItemSerializer, DinoSerializer, GeneticSerializer,
    ComboSerializer, ComboDetailSerializer, AccountSerializer,
    SessionSerializer, SessionLogSerializer, RecipeSerializer, RecipeIngredientSerializer, BlueprintSerializer, BlueprintMaterialSerializer, SalePostSerializer
)
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_active:
            raise serializers.ValidationError("Tu cuenta está desactivada.")

        data['user_id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['tribe_name'] = user.tribe.name if user.tribe else None
        data['role'] = user.role
        data['is_superuser'] = user.is_superuser
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """🔹 Retorna el usuario autenticado con su tribu, rol y permisos"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def get_queryset(self):
        """🔹 Superusuarios ven todo, Admins ven solo su tribu, Users solo leen."""
        user = self.request.user
        
        if not user.is_authenticated:  # 🔹 Evita error con AnonymousUser
            return User.objects.none()  # 🔹 No devuelve nada para usuarios no autenticados

        if user.is_superuser:
            return User.objects.all()
        elif user.role == 'admin':
            return User.objects.filter(tribe=user.tribe)
        else:
            return User.objects.filter(id=user.id)  # 🔹 Solo ve su propia info

    def get_permissions(self):
        """🔹 Controla permisos según el rol."""
        user = self.request.user

        if not user.is_authenticated:  # 🔹 Evita error con AnonymousUser
            return [permissions.IsAuthenticated()]

        if user.is_superuser:
            return [permissions.AllowAny()]
        elif user.role == 'admin':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 🔹 Solo usuarios autenticados pueden acceder
def get_current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

class TribeViewSet(viewsets.ModelViewSet):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer


class DinoViewSet(viewsets.ModelViewSet):
    queryset = Dino.objects.all()
    serializer_class = DinoSerializer


class GeneticViewSet(viewsets.ModelViewSet):
    queryset = Genetic.objects.all()
    serializer_class = GeneticSerializer


    def perform_create(self, serializer):
        """ 🔹 Asigna automáticamente la tribu del usuario autenticado """
        serializer.save(tribe=self.request.user.tribe)


class SalePostViewSet(viewsets.ModelViewSet):

    queryset = SalePost.objects.all()
    serializer_class = SalePostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """ 🔹 Asigna automáticamente la tribu del usuario autenticado """
        serializer.save(tribe=self.request.user.tribe)

    def get_queryset(self):
        """ 🔹 Filtra para que los usuarios solo puedan ver publicaciones disponibles """
        return SalePost.objects.filter(is_for_sale=True)

class ComboViewSet(viewsets.ModelViewSet):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer

    def create(self, request, *args, **kwargs):
        # ✅ Asegurarse de que los items en detalles y precios sean solo IDs
        for detail in request.data.get("details", []):
            if isinstance(detail.get("item"), dict):
                detail["item"] = detail["item"].get("id")

        for price in request.data.get("prices", []):
            if price["type"] == "Item" and isinstance(price.get("item"), dict):
                price["item"] = price["item"].get("id")

        return super().create(request, *args, **kwargs)


    def perform_create(self, serializer):
        """ Asigna la tribu automáticamente al crear un combo """
        serializer.save(tribe=self.request.user.tribe)





class ComboDetailViewSet(viewsets.ModelViewSet):
    queryset = ComboDetail.objects.all()
    serializer_class = ComboDetailSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.tribe:
            serializer.save(tribe=self.request.user.tribe)  # 🔹 Asigna la tribu automáticamente
        else:
            raise serializers.ValidationError({"detail": "El usuario no tiene una tribu asignada."})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status', instance.status)
        instance.afk_time_remaining = request.data.get('afk_time_remaining', instance.afk_time_remaining)
        instance.save()
        return Response(SessionSerializer(instance).data)

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        sessions = Session.objects.all().select_related('player')  # 🔹 Asegurar JOIN con `player`
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    

    def destroy(self, request, *args, **kwargs):
        """Finaliza la sesión y guarda el tiempo jugado en SessionLog."""
        try:
            instance = self.get_object()

            if not instance:
                return Response({"error": "Sesión no encontrada."}, status=status.HTTP_404_NOT_FOUND)

            instance.end_time = now()
            duration = instance.end_time - instance.start_time if instance.start_time else None

            # 🔹 Guardar en SessionLog si hay datos válidos
            if duration:
                SessionLog.objects.create(
                    player=instance.player,  # ✅ Ahora usa User en lugar de Player
                    account=instance.account,
                    start_time=instance.start_time,
                    end_time=instance.end_time,
                    duration=duration
                )

            instance.delete()
            return Response({"message": "Sesión finalizada y registrada correctamente."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        account_id = request.data.get('account')
        user = request.user  # ✅ Asegurar que estamos usando el usuario autenticado

        if not account_id:
            return Response({"error": "Debe proporcionar una cuenta."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Verificar que el usuario no tenga otra sesión activa
        active_session = Session.objects.filter(player=user).first()
        if active_session:
            return Response({"error": "Ya estás conectado a otra cuenta."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Verificar que la cuenta no esté ocupada
        existing_session = Session.objects.filter(account_id=account_id).first()
        if existing_session:
            return Response({"error": "Esta cuenta ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Crear la nueva sesión
        session = Session.objects.create(account_id=account_id, player=user, start_time=now(), status="playing")
        return Response(SessionSerializer(session).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Cambia el estado de una sesión"""
        instance = self.get_object()
        instance.status = request.data.get('status', instance.status)
        instance.afk_text = request.data.get('afk_text', instance.afk_text)  # 🔹 Ahora guarda el texto AFK
        instance.save()
        return Response(SessionSerializer(instance).data)    



        
class SessionLogViewSet(viewsets.ModelViewSet):
    queryset = SessionLog.objects.all()
    serializer_class = SessionLogSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]  # 🔹 Permite acceso sin autenticación

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    @action(detail=False, methods=['delete'])
    def delete_by_recipe(self, request):
        """Elimina todos los ingredientes de una receta"""
        recipe_id = request.query_params.get('recipe')
        if not recipe_id:
            return Response({"error": "Se requiere el parámetro 'recipe'."}, status=status.HTTP_400_BAD_REQUEST)
        
        ingredients_deleted, _ = RecipeIngredient.objects.filter(recipe_id=recipe_id).delete()
        return Response({"message": f"{ingredients_deleted} ingredientes eliminados."}, status=status.HTTP_204_NO_CONTENT)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('name')  # 🔹 Orden alfabético
    serializer_class = ItemSerializer

class BlueprintViewSet(viewsets.ModelViewSet):
    queryset = Blueprint.objects.all().order_by("output_item__name")
    serializer_class = BlueprintSerializer

class BlueprintMaterialViewSet(viewsets.ModelViewSet):
    queryset = BlueprintMaterial.objects.all()
    serializer_class = BlueprintMaterialSerializer