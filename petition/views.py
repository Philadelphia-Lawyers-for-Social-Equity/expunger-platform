import io
import os
import jinja2
from docxtpl import DocxTemplate

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from . import forms
from . import models

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


class PetitionerFormView(LoginRequiredMixin, View):
    form_class = forms.PetitionerForm
    template_name = "petition/petitioner_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name,
                      {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            next_form = forms.PetitionForm(initial=form.cleaned_data)
            return render(request, PetitionFormView.template_name,
                          {"form": next_form})

        return render(request, self.template_name, {'form': form})


class PetitionFormView(LoginRequiredMixin, View):
    form_class = forms.PetitionForm
    template_name = "petition/petition_form.html"

    def get(self, request, *args, **kwargs):
        return redirect('petition:petitioner_form')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        profile = request.user.expungerprofile

        if form.is_valid():
            context = {
                "organization": profile.organization,
                "attorney": profile.attorney,
                "petitioner": form.get_petitioner(),
                "petition": form.get_petition(),
                "docket": form.get_docket_id(),
                "restitution": form.get_restitution(),
            }
            docx = os.path.join(BASE_DIR, "petition", "templates",
                "petition", "petition.docx")
            document = DocxTemplate(docx)

            jinja_env = jinja2.Environment()
            jinja_env.filters['comma_join'] = lambda v: ",".join(v)

            document.render(context, jinja_env)
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'attachment; filename="petition.docx"'
            document.save(response)

            return response
    
        return render(request, PetitionFormView.template_name, {"form": form})
