.. dj-paynow documentation master file

Welcome to dj-paynow's documentation!
=======================================

**dj-paynow** is a comprehensive Django library for integrating paynow payment gateway into your Django applications. It provides a simple, secure, and Pythonic way to accept payments from South African customers.

.. image:: https://img.shields.io/pypi/v/dj-paynow.svg
   :target: https://pypi.org/project/dj-paynow/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/dj-paynow.svg
   :target: https://pypi.org/project/dj-paynow/
   :alt: Python versions

.. image:: https://img.shields.io/pypi/djversions/dj-paynow.svg
   :target: https://pypi.org/project/dj-paynow/
   :alt: Django versions

.. image:: https://img.shields.io/github/license/carrington-dev/dj-paynow.svg
   :target: https://github.com/carrington-dev/dj-paynow/blob/main/LICENSE
   :alt: License

Overview
--------

PayNow is Zimbabwe's leading payment gateway, trusted by thousands of businesses to process online payments securely. **dj-paynow** makes it easy to integrate paynow into your Django projects with minimal configuration.

Key Features
~~~~~~~~~~~~

*  **Secure**: Built-in signature verification and validation
*  **Easy to Use**: Simple API similar to dj-stripe and dj-paypal
*  **Complete**: Models, forms, views, and webhooks included
*  **Test Mode**: Sandbox support for development and testing
*  **Admin Interface**: Full Django admin integration
*  **Webhooks**: Automatic ITN (Instant Transaction Notification) handling
*  **Database Tracking**: Complete payment history and audit trail
*  **Customizable**: Support for custom fields and metadata
*  **Mobile Ready**: Works with paynow's mobile payment options

Quick Example
~~~~~~~~~~~~~

Install using pip:

.. code-block:: bash

   pip install dj-paynow

Add paynow to your main projects:

.. code-block:: bash
   
   INSTALLED_APPS += [
      'paynow'
   ]
   
Add App to Main Projects urls.py:

.. code-block:: bash

   urlpatterns += [
      path('paynow/', include("paynow.urls"))
   ]

Added paynow application ( ``/paynow/payments`` ), perform a post request on, some fields are not required, This is a post request:

.. code-block:: json

   {
      "m_payment_id": "",
      "user": null,
      "amount": null,
      "item_name": "",
      "item_description": "",
      "name_first": "",
      "name_last": "",
      "email_address": "",
      "cell_number": "", // optional field
      "custom_str1": "", // optional field
      "custom_str2": "", // optional field
      "custom_str3": "", // optional field
      "custom_str4": "", // optional field
      "custom_str5": "", // optional field
      "custom_int1": null, // optional field
      "custom_int2": null, // optional field
      "custom_int3": null, // optional field
      "custom_int4": null, // optional field
      "custom_int5": null, // optional field
   }

**Note:** The fields ``cell_number``, ``custom_str1`` through ``custom_str5``, and ``custom_int1`` through ``custom_int5`` are optional.


Expected Response

.. code-block:: json

   {
      "amount": "99.99",
      "item_name": "Premium Subscription",
      "item_description": "1 month premium access",
      "name_first": "",
      "name_last": "",
      "email_address": "your.email@gmail.com",
      "m_payment_id": "3a280ceb-344c-48d1-8e9c-7945f3f1194a",
      "paynow_url": "http://127.0.0.1:2000/paynow/checkout/2"
   }


Using paynow within React or Android
~~~~~~~~~~~~~~~

To use the above Response just redirect to the ``paynow_url`` and pay.


Why dj-paynow?
~~~~~~~~~~~~~~~

**paynow Integration Made Simple**

While paynow provides excellent documentation, integrating it into Django applications requires handling:

- Secure signature generation and verification
- ITN webhook processing and validation
- Payment tracking and database storage
- Admin interface for payment management
- Test and production environment configuration

**dj-paynow** handles all of this for you, letting you focus on building your application instead of dealing with payment gateway integration details.

Requirements
------------

* Python 3.8+
* Django 3.2+
* requests 2.25.0+
* A paynow merchant account (get one at `paynow.co.zw <https://www.paynow.co.zw>`_)

Installation
------------

Install using pip:

.. code-block:: bash

   pip install dj-paynow

Or install from source:

.. code-block:: bash

   git clone https://github.com/carrington-dev/dj-paynow.git
   cd dj-paynow
   pip install -e .

Quick Start
-----------

1. **Add to INSTALLED_APPS**

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'paynow',
      ]

2. **Configure Settings**

   .. code-block:: python

        # paynow Configuration
        PAYNOW_INTEGRATION_ID = 'your_integration_id'
        PAYNOW_INTEGRATION_KEY = 'your_integration_key'
        PAYNOW_TEST_MODE = True  # False for production

3. **Add URLs**

   .. code-block:: python

      urlpatterns = [
          ...
          path('paynow/', include('paynow.urls')),
      ]

4. **Run Migrations**

   .. code-block:: bash

      python manage.py migrate

5. **Start Accepting Payments!**

   See the :doc:`usage` guide for detailed examples.

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   configuration

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   usage
   webhooks
   testing
   security

.. toctree::
   :maxdepth: 2
   :caption: Reference

   api
   models
   forms
   views
   utils
   signals

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   changelog
   contributing
   faq
   troubleshooting
   support

PayNow Resources
-----------------

* `PayNow Website <https://www.paynow.co.zw>`_
* `PayNow API Documentation <https://developers.paynow.co.zw>`_
* `PayNow Integration Guide <https://developers.paynow.co.zw/docs#integration>`_
* `PayNow Sandbox <https://sandbox.paynow.co.zw>`_

Community & Support
-------------------

* **GitHub**: `github.com/carrington-dev/dj-paynow <https://github.com/carrington-dev/dj-paynow>`_
* **Issues**: `GitHub Issue Tracker <https://github.com/carrington-dev/dj-paynow/issues>`_
* **PyPI**: `pypi.org/project/dj-paynow <https://pypi.org/project/dj-paynow>`_
* **Email**: carrington.muleya@outlook.com

Contributing
------------

We welcome contributions! Please see our :doc:`contributing` guide for details on:

* Reporting bugs
* Suggesting features
* Submitting pull requests
* Running tests
* Code style guidelines

License
-------

**dj-paynow** is released under the MIT License. See the LICENSE file for details.

Acknowledgments
---------------

This library is inspired by other excellent Django payment libraries:

* `dj-stripe <https://github.com/dj-stripe/dj-stripe>`_
* `dj-paypal <https://github.com/dj-paypal/dj-paypal>`_
* `django-paypal <https://github.com/spookylukey/django-paypal>`_

Special thanks to PayNow for providing a reliable payment gateway for South African businesses.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`