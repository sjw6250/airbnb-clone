from django.contrib import messages

# 21.10 LoginRequiredMixin 추가
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

# 21.10 이메일로 접속한 회원인지 체크하는데 login_method 안만들어놔서 일단 주석처리
# class EmailLoginOnlyView(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.login_method == "email"

#     def handle_no_permission(self):
#         messages.error(self.request, "Can't go there")
#         return redirect("core:home")


# 21.9 mixin을 통해 리다이렉트 설정
class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


# 21.10 로그인을 하지 않았을 경우 login 페이지로 redirect
class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")
