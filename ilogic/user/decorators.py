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
