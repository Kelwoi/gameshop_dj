from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("game/<slug:slug>/", views.game_detail, name="game_detail"),

    # Buying
    path("game/<slug:slug>/buy/", views.buy_game, name="buy_game"),
    path("purchase/success/", views.purchase_success, name="purchase_success"),

    # Favorites (session)
    path("favorites/", views.favorites_list, name="favorites"),
    path("favorites/toggle/<int:game_id>/", views.favorites_toggle, name="favorites_toggle"),
]
