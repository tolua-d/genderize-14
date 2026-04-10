from django.urls import path
from app import views

urlpatterns = [
    path('api/classify', views.GenderizedViewSet.as_view({
        "get": "get_gender_classified_name"
    })),
]
