from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView,DetailView
from django.contrib.auth import get_user_model, login
from .forms import *
from .models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# vista de inicio de sesión.
class CustomLoginView(UserPassesTestMixin, LoginView):
    template_name = "data/data_user/login.html"
    login_url = reverse_lazy("usuarios:login_user")

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(f"{reverse_lazy('usuarios:confirm_logout_user')}?next={self.login_url}")

# vista de confirmación de cierre de sesión.
class CustomConfirmLogoutView(UserPassesTestMixin, LoginView):
    template_name = "data/data_user/confirm_logout.html"
    
    def test_func(self):
        return self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect(reverse_lazy("usuarios:login_user"))

# vista de registro de usuarios.
class CustomRegisterUserView(UserPassesTestMixin, CreateView):
    model = get_user_model()
    template_name = "data/data_user/signup.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("home")

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        confirm_logout_url = reverse_lazy("usuarios:confirm_logout_user")
        next_page = reverse_lazy("usuarios:signup_user")
        return redirect(f"{confirm_logout_url}?next={next_page}")

    def get_success_url(self) -> str:
        success_url = super().get_success_url()
        next_page = self.request.GET.get("next")
        if next_page:
            success_url = next_page
        return success_url

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

# vista de cierre de sesión.
class CustomLogoutView(UserPassesTestMixin, LogoutView):
    template_name = 'data/data_user/logout.html'
    success_url = reverse_lazy('usuarios:login_user')
    
    def get_success_url(self) -> str:
        success_url = super().get_success_url()
        next_page = self.request.GET.get("next")
        if next_page:
            success_url = next_page
        return success_url
    
    def test_func(self):
        return self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect(reverse_lazy("usuarios:login_user"))
    
# vista de actualización de datos del usuario.
class CustomUpdateUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "data/myProfile/update_user.html"
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user

# vista de cambio de contraseña del usuario.
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "data/myProfile/change_password.html"
    success_url = reverse_lazy("home")

# restablecer la contraseña
class CustomPasswordResetView(PasswordResetView):
    template_name = 'data/data_user/password_reset_form.html'
    email_template_name = 'data/data_user/password_reset_email.html'
    subject_template_name = 'data/data_user/password_reset_subject.txt'
    success_url = reverse_lazy('usuarios:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'data/data_user/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'data/data_user/password_reset_confirm.html'
    success_url = reverse_lazy('usuarios:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'data/data_user/password_reset_complete.html'

# vista detalles de un usuario.
class AuthorDetailView(DetailView):
    model = User
    template_name = "data/data_user/detail_user/author_detail.html"
    context_object_name = "author"