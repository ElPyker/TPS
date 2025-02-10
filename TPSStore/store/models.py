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
    name = models.CharField(max_length=100)
    description = models.TextField()
    stack = models.IntegerField(default=0)


class Dino(models.Model):
    fullname = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname  # Esto mostrará el nombre completo del dino



class Genetic(models.Model):
    dino = models.ForeignKey(Dino, on_delete=models.CASCADE)
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
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
    sale_format = models.CharField(
        max_length=50, choices=[('egg', 'Egg'), ('baby', 'Baby'), ('grown', 'Grown'), ('embryo', 'Embryo')]
    )
    is_for_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Combo(models.Model):
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_available = models.BooleanField(default=True)


class ComboDetail(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

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
