# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = "petition"

urlpatterns = [
    path("", views.PetitionerFormView.as_view(), name="petitioner_form"),
    path("petition-form/", views.PetitionFormView.as_view(),
         name="petition_form"),
    path("generate/", views.PetitionAPIView.as_view(),
         name="generate")
    ]
