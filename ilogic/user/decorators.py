from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect

from functools import wraps

# @login_required
def permissions(role=[]):
    def decorator(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            # if request.user.is_superuser:
            #     return func(request, *args, **kwargs)
            if request.user.is_anonymous:
                messages.info(request, 'Anda telah logout.')
                return redirect('/')
            elif request.user.check_permissions(group_list=role):
                return func(request, *args, **kwargs)
            else:
                return HttpResponse(content="Anda Tidak Memiliki Hak Akses, Harap Menghubungi Admin!", status=403)
        return _decorator
    return decorator


def check_device(view_func):
    def wrapper_func(request, *args, **kwargs):
        user_device = request.user.meta
        user_agent = request.META['HTTP_USER_AGENT'].__str__()
        remote_addr = request.META['REMOTE_ADDR'].__str__()
        try:
            remote_port = request.META['REMOTE_PORT'].__str__()
        except:
            remote_port = ''
        current_device = user_agent + remote_addr #+ remote_port

        if user_device != current_device:
            return HttpResponse("Akses terlarang!")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
