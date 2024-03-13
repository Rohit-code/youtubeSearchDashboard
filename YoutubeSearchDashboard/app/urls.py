from django.urls import path
from app.views import SearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
]
