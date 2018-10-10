import functools
from flask import request
from .ext import Process, backend


def measure(f, name, method, context=None):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        processer = Process(name, args, kwargs, method, context)
        try:
            value = f(*args, **kwargs)
        except BaseException as e:
            raise e
        backend.insert(processer())
        return value
    return wrapper


def profile_endpoint(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        context = {
            "url": request.base_url,
            "args": dict(request.args.items()),
            "form": dict(request.form.items()),
            "body": request.data.decode("utf-8", "strict"),
            "headers": dict(request.headers.items()),
            "func": request.endpoint,
            "ip": request.remote_addr
        }
        endpoint_name = str(request.url_rule)
        wrapped = measure(f, endpoint_name, request.method, context)
        return wrapped(*args, **kwargs)

    return wrapper


def wrap_app_endpoints(app):
    # TODO add ignore endpoint in config
    for endpoint, func in app.view_functions.items():
        app.view_functions[endpoint] = profile_endpoint(func)
