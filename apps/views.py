import base64
import random
import json

from django.core.files.base import ContentFile
from redis import Redis

from apps.forms import RegisterForm
from apps.tasks import send_email

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, FormView, DetailView, DeleteView

from apps.models import User, Driver
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "register.html"

    def form_valid(self, form):

        otp_code = random.randint(
            100000,
            999999
        )

        send_email(
            form.cleaned_data["email"],
            otp_code
        )

        data = {
            "first_name":
                form.cleaned_data[
                    "first_name"
                ],

            "last_name":
                form.cleaned_data[
                    "last_name"
                ],

            "phone":
                form.cleaned_data[
                    "phone"
                ],

            "email":
                form.cleaned_data[
                    "email"
                ],

            "language":
                form.cleaned_data[
                    "language"
                ],

            "status":
                form.cleaned_data[
                    "status"
                ],

            "otp_code":
                otp_code,
        }

        if (
                form.cleaned_data["status"]
                ==
                User.Status.DRIVER
        ):

            data.update({
                "car_mark":
                    form.cleaned_data[
                        "car_mark"
                    ],

                "car_model":
                    form.cleaned_data[
                        "car_model"
                    ],

                "car_number":
                    form.cleaned_data[
                        "car_number"
                    ],
            })

            prava = self.request.FILES.get(
                "prava_image"
            )

            if prava:
                data["prava_name"] = (
                    prava.name
                )

                data["prava_image"] = (
                    base64.b64encode(
                        prava.read()
                    ).decode()
                )

        rd = Redis(
            decode_responses=True
        )

        rd.set(
            form.cleaned_data["phone"],
            json.dumps(data),
            ex=120
        )

        return render(
            self.request,
            "otp_code.html",
            {
                "phone":
                    form.cleaned_data[
                        "phone"
                    ],

                "email":
                    form.cleaned_data[
                        "email"
                    ],
            }
        )


class OTPView(View):

    def post(self, request):

        phone = request.POST.get(
            "phone"
        )

        otp_code = request.POST.get(
            "otp_code"
        )

        rd = Redis(
            decode_responses=True
        )

        data = rd.get(phone)

        if not data:
            return redirect(
                "register"
            )

        data = json.loads(data)

        if str(
                data["otp_code"]
        ) != str(otp_code):
            return redirect(
                "register"
            )

        user = User.objects.create(
            first_name=
            data["first_name"],

            last_name=
            data["last_name"],

            phone=
            data["phone"],

            email=
            data["email"],

            language=
            data["language"],

            status=
            data["status"],
        )

        if (
                user.status
                ==
                User.Status.DRIVER
        ):

            driver = Driver.objects.create(
                user=user,
                car_mark=data[
                    "car_mark"
                ],
                car_model=data[
                    "car_model"
                ],
                car_number=data[
                    "car_number"
                ],
                prava_confirm=False,
                reyting=0,
                travel_count=0,
            )

            if data.get(
                    "prava_image"
            ):
                driver.prava_image.save(
                    data["prava_name"],

                    ContentFile(
                        base64.b64decode(
                            data[
                                "prava_image"
                            ]
                        )
                    )
                )

        rd.delete(phone)

        return redirect("home")


class HomeView(TemplateView):
    template_name = 'home.html'
