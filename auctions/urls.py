from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create_listing"),
    path("categories/", views.categories, name="categories"),
    path("category_listings", views.category_listings, name="category_listings"),
    path("listings_page", views.listings_page, name="listings_page"),
    path('watchlist/', views.watchlist_page, name='watchlist_page'),

]
