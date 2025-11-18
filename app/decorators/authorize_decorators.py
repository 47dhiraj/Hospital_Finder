from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
import sweetify



def role_required(required_roles, url='login', redirect_field_name=REDIRECT_FIELD_NAME):

    if not isinstance(required_roles, (list, tuple)):
        required_roles = [required_roles]


    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            user = request.user

            # User must be logged in
            if not user.is_authenticated:
                sweetify.error(request, "Access Denied!", text="Login required.", timer=2000)
                redirect_url = reverse(url) + f"?{redirect_field_name}={request.path}"
                return redirect(redirect_url)


            # Check if user matches any required role
            for role in required_roles:
                if getattr(user, role, False) is True:
                    return view_func(request, *args, **kwargs)


            # User does not have permission
            sweetify.error(request, "Access Denied!", text="You don't have permission.", timer=2000)
            redirect_url = reverse(url) + f"?{redirect_field_name}={request.path}"
            return redirect(redirect_url)


        return wrapper


    return decorator

