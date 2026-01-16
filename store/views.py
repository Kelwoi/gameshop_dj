from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Game, Category

def home(request):
    qs = Game.objects.select_related("category").all()

    # Search
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q) |
            Q(description__icontains=q)
        )

    # Filters
    category_slug = (request.GET.get("category") or "").strip()
    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    platform = (request.GET.get("platform") or "").strip()
    if platform:
        qs = qs.filter(platform=platform)

    min_price = (request.GET.get("min_price") or "").strip()
    max_price = (request.GET.get("max_price") or "").strip()
    if min_price:
        try:
            qs = qs.filter(price_czk__gte=min_price)
        except Exception:
            pass
    if max_price:
        try:
            qs = qs.filter(price_czk__lte=max_price)
        except Exception:
            pass

    in_stock = request.GET.get("in_stock")
    if in_stock == "1":
        qs = qs.filter(in_stock=True)

    paginator = Paginator(qs, 9)  # 9 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all().order_by("name")
    platforms = Game.Platform.choices

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "platforms": platforms,
        "active": {
            "q": q,
            "category": category_slug,
            "platform": platform,
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock == "1",
        }
    }
    return render(request, "store/home.html", context)

def game_detail(request, slug: str):
    game = get_object_or_404(Game.objects.select_related("category"), slug=slug)
    return render(request, "store/game_detail.html", {"game": game})
