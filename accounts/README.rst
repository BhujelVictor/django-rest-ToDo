============
accounts
============

accounts is a django-app to implment authentication using OTP

to install : python -m pip install --user accounts/dist/django-polls-0.1.tar.gz

Quick start
-----------

1. Add "accounts" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "accounts",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("polls/", include("accounts.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.

5. Visit the ``/accounts/`` URL to participate in the poll.