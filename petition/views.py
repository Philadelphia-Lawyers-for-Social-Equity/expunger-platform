import logging
import os
import jinja2
from docxtpl import DocxTemplate

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework.views import APIView

from . import forms
from . import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger("django")
logger.info("LogLevel is: %s" % logger.level)
logger.info("DJANGO_LOG_LEVEL: %s" % os.environ.get("DJANGO_LOG_LEVEL"))

class PetitionerFormView(LoginRequiredMixin, View):
    form_class = forms.PetitionerForm
    template_name = "petition/petitioner_form.html"

    def get(self, request, *args, **kwargs):
        logger.debug("PetitionerFormView get")
        form = self.form_class()
        return render(request, self.template_name,
                      {"form": form})

    def post(self, request, *args, **kwargs):
        logger.debug("petitioner form: %s" % form)
        form = self.form_class(request.POST)

        if form.is_valid():
            next_form = forms.PetitionForm(initial=form.cleaned_data)
            logger.debug("PetitionerFormView post")
            return render(request, PetitionFormView.template_name,
                          {"form": next_form})

        logger.debug("invalid petitioner form: %s" % form)
        return render(request, self.template_name, {'form': form})


class PetitionFormView(LoginRequiredMixin, View):
    form_class = forms.PetitionForm
    template_name = "petition/petition_form.html"

    def get(self, request, *args, **kwargs):
        logger.debug("PetitionFormView get")
        return redirect('petition:petitioner_form')

    def post(self, request, *args, **kwargs):
        logger.debug("PetitionFormView post")
        form = self.form_class(request.POST)
        profile = request.user.expungerprofile
        logger.debug("petition post with: %s" % form)

        if form.is_valid():
            context = {
                "organization": profile.organization,
                "attorney": profile.attorney,
                "petitioner": form.get_petitioner(),
                "petition": form.get_petition(),
                "docket": form.get_docket_id(),
                "restitution": form.get_restitution(),
            }
            docx = os.path.join(
                BASE_DIR, "petition", "templates", "petition", "petition.docx")
            document = DocxTemplate(docx)

            jinja_env = jinja2.Environment()
            jinja_env.filters['comma_join'] = lambda v: ",".join(v)

            document.render(context, jinja_env)
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'attachment; filename="petition.docx"'
            document.save(response)

            logger.debug("petition form: %s" % form)
            return response

        logger.debug("invalid petition form: %s" % form)
        return render(request, PetitionFormView.template_name, {"form": form})


class PetitionAPIView(APIView):

    def post(self, request, *args, **kwargs):
        logger.debug("PetitionAPIView post")
        profile = request.user.expungerprofile

        logger.debug(
            "Profile %s found attorney %s" % (profile, profile.attorney))

        context = {
            "organization": profile.organization,
            "attorney": profile.attorney,
            "petitioner":
                models.Petitioner.from_dict(request.data["petitioner"]),
            "petition":
                models.Petition.from_dict(request.data["petition"]),
            "docket":
                models.DocketId.from_dict(request.data["docket"]),
            "restitution":
                models.Restitution.from_dict(request.data["restitution"])
        }

        docx = os.path.join(
            BASE_DIR, "petition", "templates", "petition", "petition.docx")
        document = DocxTemplate(docx)

        jinja_env = jinja2.Environment()
        jinja_env.filters["comma_join"] = lambda v: ", ".join(v)
        jinja_env.filters["date"] = lambda d: "%04d-%02d-%02d" % (
            d.year, d.month, d.day)

        document.render(context, jinja_env)
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = 'attachment; filename="petition.docx"'
        document.save(response)

        logger.debug("PetitionAPIView post")
        return response
