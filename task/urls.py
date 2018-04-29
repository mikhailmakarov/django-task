from django.urls import path
from .views import add_new_categories, get_category


urlpatterns = (
    path('<int:category_id>', get_category),
    path('', add_new_categories),
)
