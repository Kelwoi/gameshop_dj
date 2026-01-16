from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self) -> str:
        return self.name

class Game(models.Model):
    class Platform(models.TextChoices):
        PC = "PC", "PC"
        PS = "PlayStation", "PlayStation"
        XBOX = "Xbox", "Xbox"
        SWITCH = "Switch", "Switch"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="games")
    platform = models.CharField(max_length=20, choices=Platform.choices, default=Platform.PC)
    price_czk = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Гра"
        verbose_name_plural = "Ігри"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("store:game_detail", kwargs={"slug": self.slug})
    


from django.conf import settings

class Purchase(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        CANCELED = "CANCELED", "Canceled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchases",
    )
    game = models.ForeignKey("Game", on_delete=models.PROTECT, related_name="purchases")
    email = models.EmailField()
    full_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Purchase #{self.id} - {self.game.title}"


