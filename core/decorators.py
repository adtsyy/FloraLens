from django.shortcuts import redirect
from functools import wraps
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request,*args,**kwargs):
            if not request.user.is_authenticated: return redirect('login')
            if not hasattr(request.user,'profile') or request.user.profile.role != role: return redirect('dashboard')
            return view_func(request,*args,**kwargs)
        return wrapper
    return decorator
