from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_staff:
            if not user.is_verified:
                return self.handle_no_permission()
            if not user.is_authenticated:
                return self.handle_no_permission()
            
            if user != self.get_object().author:
                messages.info(request, 'У вас нет авторских прав')
                return redirect('MainPage')
        return super().dispatch(request, *args, **kwargs)
            
            
class IsVerifipdMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_staff:
            if not user.is_authenticated:
                return self.handle_no_permission()
            
            if not user.is_verified:
                messages.info(request, 'Вы не верифицированы')
                return redirect('MainPage')
        return super().dispatch(request, *args, **kwargs)
    
    
class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('Login')
        return super().dispatch(request, *args, **kwargs)
        
        