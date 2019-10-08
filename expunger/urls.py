from django.urls import path
from . import views

app_name = 'expunger'

urlpatterns = [
    path("organizations/", views.OrganizationsView.as_view(),
         name="organizations"),
    path("organization/<int:pk>", views.OrganizationView.as_view(),
         name="organization-detail")
]
