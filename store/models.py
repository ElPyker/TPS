from django.db import models
from django.utils.timezone import now


class Tribe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)  # 🔹 Encripta la contraseña correctamente
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):  
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    tribe = models.ForeignKey('Tribe', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # 🔹 Campo usado para autenticación
    REQUIRED_FIELDS = ['email']  # 🔹 Campos requeridos al crear un usuario

    objects = UserManager()  # 🔹 Define el `UserManager` para manejar usuarios

    def set_password(self, raw_password):
        """🔹 Encripta la contraseña antes de guardarla"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """🔹 Compara la contraseña ingresada con el hash"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Item(models.Model):
    """Modelo para almacenar los items (ingredientes y productos)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    stack = models.PositiveIntegerField(default=1)  # Cantidad máxima de stack
    image = models.ImageField(upload_to='items/', blank=True, null=True)  # Campo para la imagen

    def __str__(self):
        return f"{self.name} (Stack: {self.stack})"


class Recipe(models.Model):
    """Modelo para almacenar recetas en ARK"""
    name = models.CharField(max_length=100, blank=True)  # 🔹 Permitir que se deje vacío
    description = models.TextField(blank=True, null=True)
    output_item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name="recipes"
    )  
    output_quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        """🔹 Asigna automáticamente el nombre del item resultante si no está definido"""
        if not self.name and self.output_item:
            self.name = self.output_item.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # 🔹 El modelo se representará por su nombre


class RecipeIngredient(models.Model):
    """Modelo que relaciona ingredientes con una receta"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # 🔹 Usa el modelo Item ya creado
    quantity = models.PositiveIntegerField()  # 🔹 Cantidad requerida por ingrediente

    def __str__(self):
        return f"{self.quantity}x {self.item.name} en {self.recipe.name}"


class Blueprint(models.Model):
    """Modelo para almacenar Blueprints en ARK"""
    output_item = models.ForeignKey(
        "Item", 
        on_delete=models.CASCADE, 
        related_name="blueprints"
    )  # 🔹 Item que se fabrica con el blueprint
    description = models.TextField(blank=True, null=True)
    output_quantity = models.PositiveIntegerField(default=1)  # 🔹 Cantidad producida por cada blueprint

    @property
    def name(self):
        return f"Blueprint {self.output_item.name}"

    def __str__(self):
        return self.name

class BlueprintMaterial(models.Model):
    """ Materiales necesarios para fabricar un blueprint """
    blueprint = models.ForeignKey(Blueprint, on_delete=models.CASCADE, related_name="materials")
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.item.name} en {self.blueprint.name}"

class Dino(models.Model):
    CATEGORY_CHOICES = [
        ('PvP', 'PvP'),
        ('Soaker', 'Soaker'),
        ('Flyer', 'Flyer'),
        ('Water', 'Water'),
        ('Any', 'Any')
    ]
    
    EGG_TYPE_CHOICES = [
        ('Egg', 'Egg'),
        ('Embryo', 'Embryo'),
        ('Clone', 'Clone')
    ]

    fullname = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='dinos/', null=True, blank=True)  # 🦖 Imagen del Dino
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Any')  # 🦖 Categoría del Dino
    egg_type = models.CharField(max_length=10, choices=EGG_TYPE_CHOICES, default='Egg')  # 🦖 Tipo de reproducción

    def __str__(self):
        return self.fullname  # Esto mostrará el nombre completo del dino


class Genetic(models.Model):
    """ 🔹 Modelo de Genética de Dinosaurios (solo para registros, sin venta) """
    dino = models.ForeignKey("Dino", on_delete=models.CASCADE)
    tribe = models.ForeignKey("Tribe", on_delete=models.CASCADE)

    # 📌 Estadísticas con Base y Mutaciones
    health_base = models.IntegerField()
    health_mutates = models.IntegerField(default=0)

    stamina_base = models.IntegerField()
    stamina_mutates = models.IntegerField(default=0)

    oxygen_base = models.IntegerField()
    oxygen_mutates = models.IntegerField(default=0)

    food_base = models.IntegerField()
    food_mutates = models.IntegerField(default=0)

    weight_base = models.IntegerField()
    weight_mutates = models.IntegerField(default=0)

    damage_base = models.IntegerField()
    damage_mutates = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dino.fullname} - {self.tribe.name}"


class SalePost(models.Model):
    """ 🔹 Publicaciones de Venta de Genéticas """
    PAYMENT_METHODS = [
        ('USD', 'Dólares'),
        ('EUR', 'Euros'),
        ('Item', 'Item del Juego'),
    ]

    tribe = models.ForeignKey("Tribe", on_delete=models.CASCADE)
    genetic = models.ForeignKey(Genetic, on_delete=models.CASCADE)  # 🔹 Asociada a una genética específica
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    discord_contact = models.CharField(max_length=100, blank=True, null=True)  # 🔹 Contacto opcional

    is_for_sale = models.BooleanField(default=True)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='USD')
    item_payment = models.ForeignKey("Item", null=True, blank=True, on_delete=models.SET_NULL)
    price_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.tribe.name}"


class Combo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    is_for_sale = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.tribe.name}"

class ComboDetail(models.Model):
    combo = models.ForeignKey(Combo, related_name="details", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.item.name} en {self.combo.name}"

class Price(models.Model):
    PRICE_TYPES = [
        ("Coins", "Coins"),
        ("Item", "Game Item"),
    ]

    combo = models.ForeignKey("Combo", related_name="prices", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=PRICE_TYPES)
    item = models.ForeignKey("Item", null=True, blank=True, on_delete=models.CASCADE, default=None)  # ✅ Ahora permite `null`
    quantity = models.PositiveIntegerField(null=True, blank=True, default=None)  # ✅ Ahora permite `null`
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)  # ✅ Ahora permite `null`

    def __str__(self):
        return f"{self.combo.name} - {self.type} - {self.amount if self.type == 'Coins' else self.item.name}"

class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)
    short_code = models.CharField(max_length=10, unique=True)
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, related_name="accounts")  # Relación con Tribe

    def __str__(self):
        return f"{self.name} ({self.short_code})"




STATUS_CHOICES = [
    ('tribelog', 'TribeLog'),
    ('playing', 'Playing'),
    ('afk', 'AFK'),
]


class Session(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    player = models.ForeignKey('User', on_delete=models.CASCADE)  # ✅ Usar User en lugar de Player
    start_time = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=[
        ('playing', 'Playing'),
        ('gachatower', 'GachaTower'),
        ('afk', 'AFK')
    ], default='playing')
    afk_text = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # 🔹 Nueva columna

    def __str__(self):
        return f"{self.player.username} - {self.account.name} ({self.status})"



class SessionLog(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ Usar User en lugar de Player
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self):
        return f"{self.player.username} - {self.account.name} ({self.duration})"
