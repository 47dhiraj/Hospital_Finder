from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
import sweetify



# Map role names to your model fields
ROLE_MAP = {
    "admin": "is_admin",
    "client": "is_client",
}




def role_required(allowed_roles, url='login', redirect_field_name=REDIRECT_FIELD_NAME):

    if not isinstance(allowed_roles, (list, tuple)):
        allowed_roles = [allowed_roles]

    allowed_flags = [ROLE_MAP.get(role) for role in allowed_roles]


    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            user = request.user

            ## First checking if user is authenticated user or not
            if not user.is_authenticated:
                sweetify.error(request, "Access Denied!", text="Login required.", timer=2000)
                redirect_url = reverse(url) + f'?{redirect_field_name}={request.path}'
                return redirect(redirect_url)


            ## Now, checking the user role (user has valid permission or not) 
            for flag in allowed_flags:
                if flag and getattr(user, flag, False):
                    return view_func(request, *args, **kwargs)


            # No allowed role found
            sweetify.error(request, "Access Denied!", text="You don't have permission.", timer=2000)
            redirect_url = reverse(url) + f'?{redirect_field_name}={request.path}'
            return redirect(redirect_url)


        return wrapper


    return decorator
