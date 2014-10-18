Python Dependency Injection Container
=====================================

.. image:: https://travis-ci.org/felixcarmona/pydic.png?branch=master
    :target: https://travis-ci.org/felixcarmona/pydic

.. image:: https://coveralls.io/repos/felixcarmona/pydic/badge.png?branch=master
    :target: https://coveralls.io/r/felixcarmona/pydic?branch=master

.. image:: https://pypip.in/d/pydic/badge.png
    :target: https://pypi.python.org/pypi/pydic/
    :alt: Downloads

.. image:: https://pypip.in/v/pydic/badge.png
    :target: https://pypi.python.org/pypi/pydic/
    :alt: Latest Version

Parameters
----------
The ``pydic.Parameters`` class is a simple container for key/value pairs.

The available methods are:

- ``set(key, value)``: Sets a parameter.
- ``get(key, default=None)``: Returns a parameter by name. If the key don't exists, the default parameter will be returned.
- ``has(key)``: Returns *True* if the parameter exists, *False* otherwise.
- ``remove(key)``: Removes a parameter.
- ``add(parameters)``: Adds a dict of parameters
- ``all()``: Returns all set parameters.
- ``count()``: Returns the number of all set parameters.
- ``keys()``: Returns the all set parameter keys.
- ``parse_text(text)``: Resolves a string which can contain parameters (example: 'Hello {{ name }} {{ surname }}!')


.. note::

    You can reference others parameters wrapping it between ``{{`` ``}}`` characters.

    For example: ``'foo': '{{ bar }}', 'bar': 'aaa'``, if you get the ``foo`` parameter, the return value should be ``aaa`` because ``foo -> {{ bar }} -> bar -> aaa``

    You can escape brackets processing with "``\``".

    For example, if you set a parameter with the following value ``Hello \{\{ name \}\}``, if you get it, the return will be ``Hello {{ name }}!``


Services
--------

What is a Service Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~
A Service Container (or *dependency injection container*) is simply a python object that manages the instantiation of services (objects).
For example, suppose you have a simple python class that delivers email messages. Without a service container, you must manually create the object whenever you need it:

.. code-block:: python

    from myapplication.mailer import Mailer

    mailer = Mailer('sendmail')
    mailer.send('felix@example.com', ...)

This is easy enough. The imaginary *Mailer* class allows you to configure the method used to deliver the
email messages (e.g. *sendmail*, *smtp*, etc).

But what if you wanted to use the mailer service somewhere else? You certainly don't want to repeat the mailer
configuration every time you need to use the Mailer object. What if you needed to change the *transport* from *sendmail*
to *smtp* everywhere in the application? You'd need to hunt down every place you create a *Mailer* service and change it.

The Services container allows you to standardize and centralize the way objects are constructed in your application.

Creating/Configuring Services in the Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A better answer is to let the service container create the *Mailer* object for you.
In order for this to work, you must teach the container how to create the *Mailer* service.
This is done via configuration definitions:

.. code-block:: python

    ...
    from pydic import Services

    definitions = {
        'my_mailer': {
            'class':        'myapplication.mailer.Mailer',
            'arguments':    ['sendmail']
        }
    }

    services = Services(definitions)
    ...


When you ask for the *my_mailer* service from the container ``services.get('my_mailer')``, the container constructs the object and returns it.

This is another major advantage of using the service container. Namely, a service is never constructed until it's needed.
If you define a service and never use it, the service is never created. This saves memory and increases
the speed of your application. This also means that there's very little or no performance hit for defining lots
of services. **Services that are never used are never constructed.**

As an added bonus, the *Mailer* service is only created once and the same instance is returned each time you ask for
the service. This is almost always the behavior you'll need (it's more flexible and powerful).

You can pass the arguments as list or dict.

Also you can call functions after object instantiation with:

.. code-block:: python

    ...
    definitions = {
        'my_mailer': {
            'class':        'myapplication.mailer.Mailer',
            'arguments':    ['sendmail'],
            'calls': [
                [ 'set_name', 'Felix Carmona'],
                [ 'inject_something',  [1, 2, 3]],
                [ 'inject_something',  [2, 3]],
                [ 'set_location',  {'city': 'Barcelona', 'country': 'Spain'}]
            ]
        }
    }
    ...


Once the container has been constructed with the definitions, the available methods for the service container object are:

- ``set(key, value)``: Sets a service object by name.
- ``get(key)``: Returns a service object by name.
- ``has(key)``: Returns *True* if the service definition exists or if the service object is instantiated, *False* otherwise.
- ``remove(key)``: Removes a service object and service definition by name.
- ``add(parameters)``: Adds a dict of services objects.
- ``keys()``: Returns the services keys.


Using the Parameters to build Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The creation of new services (objects) via the container is pretty straightforward. Parameters make defining services
more organized and flexible:

.. code-block:: python

    ...
    parameters = Parameters(
        {
            'my_mailer_class':     'myapplication.mailer.Mailer',
            'my_mailer_transport': 'sendmail'
        }
    )

    definitions = {
        'my_mailer': {
            'class':        '{{ my_mailer_class }}',
            'arguments':    ['{{ my_mailer_transport }}']
        }
    }

    services = Services(definitions, parameters)
    ...


The end result is exactly the same as before - the difference is only in how you defined the service.
By surrounding the *my_mailer.class* and *my_mailer.transport* strings in double bracket keys (``{{`` ``}}``) signs, the services container knows to look
for parameters with those names. Parameters can deep reference other parameters that references other parameters, and will
be resolved anyway.

The purpose of parameters is to feed information into services. Of course there was nothing wrong with defining the
service without using any parameters. Parameters, however, have several advantages:

    - separation and organization of all service "options" under a single parameters key
    - parameter values can be used in multiple service definitions

The choice of using or not using parameters is up to you.


Referencing (Injecting) Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can of course also reference services

Start the string with @ to reference a service, example:

.. code-block:: python

    ...
    parameters = Parameters(
        {
            'my_mailer_class':     'myapplication.mailer.Mailer',
            'my_mailer_transport': 'sendmail'
        }
    )

    definitions = {
        'my_mailer': {
            'class':        '{{ my_mailer_class }}',
            'arguments':    ['{{ my_mailer_transport }}']
        },
        'my_mailer_manager': {}
            'class': 'myapplication.mailer.MailerManager',
            'arguments': ['@my_mailer']
        }
    }

    services = Services(definitions, parameters)
    ...


the *my_mailer* service will be injected in the *my_mailer_manager*

.. note::

    Use ``@@`` to escape the ``@`` symbol. ``@@my_mailer`` will be converted into the string "``@my_mailer``" instead of referencing the
    *my_mailer* service.

------------------

*pydic is open-sourced software licensed under the MIT license*