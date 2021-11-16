from django.views.generic.edit import UpdateView
from users import models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView

from . import forms


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {"first_name": "Nicoas", "last_name": "Serr", "email": "itn@las.com"}

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"

    # context 에 값을 주면 html 파일에서 {{hello}} 이렇게 써서 TEST를 출력 가능
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["hello"] = "TEST"
    #     return context


# 21.6 Django 에는 UpdateView 가 존재한다
# 21.6 업데이트를 모두 끝내면 get_absolute_url 까지 호출해서 마무리 해준다
class UpdateProfileView(UpdateView):

    # 21.6 모델은 models.py의 User 클래스를 이용한다.
    model = models.User
    # 21.6 템플릿을 html 파일로 만들어주고
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user

    # 21.7 form validation sample
    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


# 21.7 https://ccbv.co.uk/ 여기 가면 어떤게 있는지 다 나옴 view에 대해
class UpdatePasswordView(PasswordChangeView):

    template_name = "users/update-password.html"
