from django.db import models


class Tribe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name  # Esto mostrará el nombre de la tribu en los desplegables

from django.contrib.auth.hashers import make_password

class User(models.Model):
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Si la contraseña no está hasheada, la hasheamos
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

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
