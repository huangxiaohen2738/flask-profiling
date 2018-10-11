from flask_admin.menu import MenuLink
from flask import current_app
from .api import api
from .decorators import wrap_app_endpoints
from .ext import backend, auth, ldap


class Profile(object):
    """ flask-profiling for extension. """

    def __init__(self, app=None, logger=None):
        if app is not None:
            self.init_app(app, logger)

    def init_app(self, app, admin=None, logger=None):
        config = app.config.get("flask_profiling", {})
        if not config.get("enabled", True):
            logger.info("Do not use the profile for Flask")
            return

        backend.init_app(app)
        wrap_app_endpoints(app)
        app.register_blueprint(api)
        if logger is None:
            self.setup_logger()

        if admin is not None:
            admin.add_link(MenuLink("Profile", "/flask-profiling"))

        if config.get("type") == "ldap":
            ldap.init_app(app)

    def setup_logger(self, level="INFO"):
        import logging

        formatter = logging.Formatter(
            "%(asctime)s %(name)s [%(levelname)s] %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)

        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        logger.addHandler(handler)


@auth.verify_password
def verify_auth(username, password):
    config = current_app.config["flask_profiling"]
    if not config["auth"].get("enabled"):
        return True
    if config["type"] == "ldap":
        return ldap.check(username, password)
    else:
        if (
            username == config.get("username")
            and password == config.get("password")
        ):
            return True
    return False
