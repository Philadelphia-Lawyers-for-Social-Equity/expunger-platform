# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = "petition"

urlpatterns = [
    path("", views.PetitionerFormView.as_view(), name="petitioner_form"),
    path("petition/", views.PetitionFormView.as_view(), name="petition_form")
    ]
