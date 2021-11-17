from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin


# 21.9 mixin을 통해 리다이렉트 설정
class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("core:home")
