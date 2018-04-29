from django.urls import path
from .views import add_new_categories


urlpatterns = (
    path('', add_new_categories),
)
