import time
from flask_httpauth import HTTPBasicAuth
from ldap3 import Server, Connection
from .backends import Backend
from .models import Measurements  # NOQA


class Process(object):
    DECIMAL_PLACES = 6

    def __init__(self, name, args, kwargs, method, context=None):
        self.context = context
        self.name = name
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.end = 0
        self.elapsed = 0

    def to_dict(self):
        return {
            "name": self.name,
            "args": self.args,
            "kwargs": self.kwargs,
            "method": self.method,
            "startedAt": self.start,
            "endedAt": self.end,
            "elapsed": self.elapsed,
            "context": self.context
        }

    def __call__(self):
        self.end = time.time()
        self.elapsed = round(
            self.end - self.start, self.DECIMAL_PLACES)
        return self.to_dict()


class LDAP(object):
    def __init__(self):
        self._server = None
        self._get_user_dn = None

    def init_app(self, app):
        config = app.config["flask_profiling"]
        server = config.get("auth", {}).get("ldap_server")
        port = config.get("auth", {}).get("ldap_port")
        dn = config.get("auth", {}).get("ldap_base_search_dn")

        assert server is not None
        assert port is not None
        assert dn is not None

        self._server = Server(server, port)
        self._get_user_dn = lambda user: "cn={0},{1}".format(
            user, dn
        )

    def check_password(self, user, password):
        conn = Connection(self._server)
        conn.bind()
        conn.start_tls()
        return conn.rebind(user=self._get_user_dn(user), password=password)


backend = Backend()
auth = HTTPBasicAuth()
ldap = LDAP()
