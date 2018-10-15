# Flask-profiling


**version: 0.2** [![Build Status](https://travis-ci.org/huangxiaohen2738/flask-profiling.svg?branch=master)](https://travis-ci.org/huangxiaohen2738/flask-profiling)

##### Flask-profiling: A simple web UI for flask to profile the apis

```python
# your app.py
from flask import Flask
from flask_profiling import Profile
from flask_admin import Admin


app = Flask(__name__)
profile = Profile()
admin = Admin()  # If you use it.

# You need to declare necessary configuration to initialize
# flask-profiling as follows:
app.config["FLASK_PROFILING"] = {
    "db_url": "mysql+pymysql://...",
    "enabled": True,  # must be true if you want to use the flask-profiling
    "auth":{
        "enabled": True,
        "db_url": "mysql+pymysql://root:root@localhost/test",
        "type": "basic",  # ldap
        "username": "admin",  # if you choose the basic
        "password": "admin"  # if you choose the basic
        "ldap_server": "http://dddd",  # for the ldap
        "ldap_port": "336",
        "ldap_base_search_dn": ou=users,dc=baidu,dc=com"
    },
    "ignore": [  # the api which does Not want to profile
        "^/static/.*",
        "/js/.*"
    ]
}
# AND init profile when the ALL API were registed


@app.route('/product/<id>', methods=['GET'])
def getProduct(id):
    return "product id is " + str(id)


profile.init_app(app, logger=logger)

# If you use the flask-admin, flask-profiling can show on it.
# profile.init_app(app, admin)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)



And in your browser, you can visit the "http://localhost:5000/flask-profiling"
Or visit it in your flask-admin.

```

## License
Apache 2.0
