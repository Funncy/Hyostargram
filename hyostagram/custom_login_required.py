from functools import wraps
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.handlers.wsgi import WSGIRequest

def custom_login_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if args:
            request = args[0]
            # Django의 view에서 첫 번째 매개변수는 HttpRequest타입의 변수이며, 이를 확인한다
            # 또한 요청 메서드가 POST인지 확인한다
            if isinstance(request, WSGIRequest) and request.method == 'POST':
                # request 의 user가 있는지 인증되었는지 확인한다
                user = getattr(request, 'user')
                if user and user.is_authenticated:
                    return view_func(*args, **kwargs)
                #인증 되지 않을 경우 HTTP_REFERER의 path를 가져온다
                path = urlparse(request.META['HTTP_REFERER']).path
                return redirect_to_login(path)
        #위에 해당되지 않으면 기존 login_required를 동작한다
        return login_required(view_func)(*args, **kwargs)
    return decorator