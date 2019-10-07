from django.urls import path
from . import views

app_name = 'expunger'

urlpatterns = [
    path("address/<int:pk>/", views.AddressView.as_view(),
         name="address-detail")
]
