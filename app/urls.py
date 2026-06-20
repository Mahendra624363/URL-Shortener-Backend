from django.urls import path
from .views import UrlShortenView, RedirectUrlView

urlpatterns = [
    path("shorten/", UrlShortenView.as_view(),name='shorten'),
    path("<str:code>/", RedirectUrlView.as_view(),name="redirecturl"),
]