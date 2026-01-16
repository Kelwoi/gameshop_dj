from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Game
from decimal import Decimal
import random

class Command(BaseCommand):
    help = "Seeds the database with demo categories and games."

    def handle(self, *args, **options):
        categories = ["Action", "RPG", "Indie", "Strategy", "Racing", "Horror"]
        cat_objs = []
        for name in categories:
            obj, _ = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            cat_objs.append(obj)

        titles = [
            "Nebula Raiders", "Castle of Bytes", "Shadow Alley", "Turbo Circuit",
            "Pixel Kingdom", "Deep Space Tactics", "Nightmare Hotel", "Rusty Arena",
            "Cursed Forest", "Skyline Drift", "Quantum Quest", "Iron Dawn",
            "Frozen Signal", "Nova Runner", "Witchcraft Protocol", "Dungeon Courier",
            "Signal Lost", "Mecha Frontier", "Zero Hour Siege", "Silent Metro",
        ]

        platforms = [c[0] for c in Game.Platform.choices]

        created = 0
        for t in titles:
            slug = slugify(t)
            if Game.objects.filter(slug=slug).exists():
                continue
            Game.objects.create(
                title=t,
                slug=slug,
                category=random.choice(cat_objs),
                platform=random.choice(platforms),
                price_czk=Decimal(random.randrange(199, 1499)),
                in_stock=random.choice([True, True, True, False]),
                short_description="Демо-гра для каталогу. Можна редагувати в адмінці.",
                description="Це демонстраційний опис. Додай реальний контент через Django admin.",
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded demo data: {created} games."))
