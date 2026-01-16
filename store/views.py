from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Game, Category, Purchase
from .forms import PurchaseForm


FAV_SESSION_KEY = "favorite_game_ids"


def _get_favorites_set(request) -> set[int]:
    """Read favorites from session and return as a set of ints."""
    raw = request.session.get(FAV_SESSION_KEY, [])
    try:
        return set(int(x) for x in raw)
    except Exception:
        return set()


def _save_favorites_set(request, favs: set[int]) -> None:
    """Save favorites back to session."""
    request.session[FAV_SESSION_KEY] = sorted(favs)
    request.session.modified = True


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

    paginator = Paginator(qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all().order_by("name")
    platforms = Game.Platform.choices

    favorites = _get_favorites_set(request)

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "platforms": platforms,
        "favorites": favorites,
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
    favorites = _get_favorites_set(request)
    is_favorite = game.id in favorites
    return render(request, "store/game_detail.html", {"game": game, "is_favorite": is_favorite})


@require_POST
def favorites_toggle(request, game_id: int):
    """Add/remove a game from favorites using session."""
    game = get_object_or_404(Game, id=game_id)
    favs = _get_favorites_set(request)

    if game.id in favs:
        favs.remove(game.id)
        messages.info(request, f"Прибрано з улюблених: {game.title}")
    else:
        favs.add(game.id)
        messages.success(request, f"Додано в улюблені: {game.title}")

    _save_favorites_set(request, favs)

    # Return to the page user came from (if possible)
    next_url = request.POST.get("next") or reverse("store:game_detail", kwargs={"slug": game.slug})
    return redirect(next_url)


def favorites_list(request):
    favs = _get_favorites_set(request)
    games = Game.objects.filter(id__in=favs).select_related("category").order_by("title")
    return render(request, "store/favorites.html", {"games": games})


def buy_game(request, slug: str):
    """Checkout page for purchasing a single game."""
    game = get_object_or_404(Game, slug=slug)

    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase: Purchase = form.save(commit=False)
            purchase.game = game
            purchase.user = request.user if request.user.is_authenticated else None
            # Demo flow: we mark as PAID immediately (no real payment gateway)
            purchase.status = Purchase.Status.PAID
            purchase.save()

            messages.success(request, "Покупку оформлено ✅ (демо)")
            return redirect("store:purchase_success")
    else:
        # Pre-fill email if user is logged in and has email
        initial = {}
        if request.user.is_authenticated and request.user.email:
            initial["email"] = request.user.email
        form = PurchaseForm(initial=initial)

    return render(request, "store/checkout.html", {"game": game, "form": form})


def purchase_success(request):
    return render(request, "store/purchase_success.html")
