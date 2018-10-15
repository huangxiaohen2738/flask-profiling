"""
Flask-Profiling
-------------

Flask Profiling

Links
`````

* `development version <http://github.com/huangxiaohen2738/flask-profiling/>`

"""
from setuptools import setup


tests_require = [
    "Flask-Testing",
]

install_requires = [
    'flask',
    'flask-admin',
    'flask-httpauth',
    'itsdangerous',
    'jinja2',
    'ldap',
    'markupSafe',
    'pymysql',
    'sqlalchemy',
    'werkzeug'
]

setup(
    name='flask_profiling',
    version='0.3',
    url='https://github.com/huangxiaohen2738/flask-profiling',
    license=open('LICENSE').read(),
    author='huangxiaohen2738',
    author_email='huangxiaohen2738@gmail.com',
    description='A simple web UI for flask to profile the apis',
    keywords=[
        'profiler', 'flask', 'performance'
    ],
    long_description=open('README.md').read(),
    packages=['flask_profiling'],
    package_data={
        'flask_profiling': [
            'storage/*',
            'static/dist/fonts/*',
            'static/dist/css/*',
            'static/dist/js/*',
            'static/dist/images/*',
            'static/dist/js/*'
            'static/dist/*',
            'static/dist/index.html',
            ]
        },
    test_suite="tests.suite",
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
