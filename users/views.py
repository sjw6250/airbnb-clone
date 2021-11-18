from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView
from django.views.generic.edit import UpdateView

from users import models

from . import forms, mixins, models


class LoginView(mixins.LoggedOutOnlyView, FormView):

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

    # 21.10 로그인에 성공하면 get 파라미터로 담겨있는 next 변수(원래 있던 페이지)로 보내거나 없으면 home으로 보냄
    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

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
class UpdateProfileView(
    mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView
):  # 21.9 Mixin 추가를 통해 메세지 띄워줌

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

    # 21.9 클래스 생성할때 믹스인 추가하고 메세지만 넣어주면 됨
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    # 21.8 UpdateView 만 이용하면 커스터마이징이 힘들고 고정되어있는데 아래를 이용해서 커스텀한다.
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        return form

    # 21.7 form validation sample
    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)


# 21.7 https://ccbv.co.uk/ 여기 가면 어떤게 있는지 다 나옴 view에 대해
class UpdatePasswordView(
    mixins.LoggedInOnlyView,  # 21.10 로그인이 안되어 있으면 로그인 페이지로 이동 시키기 위해 추가
    # 21.10 mixins.EmailLoginOnlyView, 이메일 로그인이 아니면 안되게 하기
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    # 21.9 패스워드 변경 성공하고 absolute url로 이동
    def get_success_url(self):
        return self.request.user.get_absolute_url()
