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
