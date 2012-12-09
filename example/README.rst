Example atx_restaurant_ratings Project
======================================
This provides an example project for ``atx_restaurant_ratings``.


Usage
-----
Create your virtualenv, then run:

::

    pip install -r requirements.txt

Next, install the various gems.

::

    bundle install

Finally, start up the demo server using Foreman.

::

    bundle exec foreman start


Testing
-------
Once you've installed the various requirements, you can run the tests for
``atx_restaurant_ratings`` by running ``manage.py`` like this:

::

    python manage.py test example_usage
