===============================
flask-passwordless
===============================

.. image:: https://badge.fury.io/py/flask-passwordless.png
    :target: http://badge.fury.io/py/flask-passwordless
    
.. image:: https://travis-ci.org/kevinjqiu/flask-passwordless.png?branch=master
        :target: https://travis-ci.org/kevinjqiu/flask-passwordless

.. image:: https://pypip.in/d/flask-passwordless/badge.png
        :target: https://crate.io/packages/flask-passwordless?version=latest


Flask extension for implementing passwordless login.

Inspired by `passwordless <https://passwordless.net/>`_

-----
Intro
-----

This simple flask plugin allows you to implement passwordless login using one-time password token authentication.

Passwordless authentication is faster to deploy, easier for your users and better for security.


^^^^^^^^^^
Deployment
^^^^^^^^^^

A single ``userid`` field in your web front-end and that's it.  No need for complicated user login forms.

^^^^^^^^^^^
Convenience
^^^^^^^^^^^

Users don't have to come up with a secure password.

^^^^^^^^
Security
^^^^^^^^

Because using one-time token, you don't need to store users' passwords so you have no passwords to lose to hackers.


-----
Usage
-----

^^^^^^^^^^^^
Installation
^^^^^^^^^^^^

Similar to any modern python libraries, install flask-passwordless with `pip <http://en.wikipedia.org/wiki/Pip_(package_manager)>`_

    pip install flask-passwordless

If you're using `virtualenv <https://github.com/pypa/virtualenv/>`_ (and you really should), activate the virtualenv before doing ``pip install``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Integrate it in your project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Take a look at the examples folder



* Free software: BSD license
* Documentation: http://flask-passwordless.rtfd.org.
