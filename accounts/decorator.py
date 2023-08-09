from django.shortcuts import redirect

def redirect_authenticated_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view


def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
