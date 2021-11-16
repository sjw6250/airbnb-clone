from django import views
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    # 21.6
    # views에 UpdateProfileView 클래스를 만들고 이걸 이용한다.
    # 그리고 name의 update 를 html에서 {% url 'users:update' %} 이런 식으로 호출한다.
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    # 21.7 패스워드 변경
    path("update-passwod/", views.UpdatePasswordView.as_view(), name="password"),
]
