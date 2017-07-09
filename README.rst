.. image:: http://pybee.org/project/projects/tools/waggle/waggle.png
    :width: 72px
    :target: https://pybee.org/waggle

Waggle
======

.. image:: https://img.shields.io/pypi/pyversions/waggle.svg
    :target: https://pypi.python.org/pypi/waggle

.. image:: https://img.shields.io/pypi/v/waggle.svg
    :target: https://pypi.python.org/pypi/waggle

.. image:: https://img.shields.io/pypi/status/waggle.svg
    :target: https://pypi.python.org/pypi/waggle

.. image:: https://img.shields.io/pypi/l/waggle.svg
    :target: https://github.com/pybee/waggle/blob/master/LICENSE

.. image:: https://travis-ci.org/pybee/waggle.svg?branch=master
    :target: https://travis-ci.org/pybee/waggle

.. image:: https://badges.gitter.im/pybee/general.svg
    :target: https://gitter.im/pybee/general

Prepare and upload Docker images for use by BeeKeeper.

Quickstart
----------

Create a directory, and in that directory place a `Dockerfile` and any
files required by the `Dockerfile` in that directory.

Optionally, you can also put an `ecs.json` file in the directory. The
`ecs.json` file should contains a JSON definition of any ECR container
settings that you want task to have.  For example, if you wanted to specify a
particular memory and CPU usage profile for the task, you would specify::

    {
        memory: 50,
        cpu: 8192
    }

Then, create a file named `.env` in your current working directory that contains
the following content::

    AWS_ECS_REGION_NAME=<Your AWS region (e.g., us-west-2)
    AWS_ACCESS_KEY_ID=<Your AWS access key>
    AWS_SECRET_ACCESS_KEY=<Your AWS secret access key>

Then, run::

    $ waggle <path to docker image directory>

This will:

    * Log into AWS ECR
    * Find (or create) an AWS ECR repository for your image
    * Build the Docker image
    * Tag the image for publication to AWS ECR
    * Push the image to AWS ECR
    * Register (or update) an AWS ECS task that uses the image.

If your Docker image is contained in a directory called `myimage`, your
BeeKeeper configuration will not be able to reference a task image of
`myimage`.

..Documentation
..-------------

..Documentation for Waggle can be found on `Read The Docs`_.

Community
---------

Waggle is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `pybee/general`_ channel on Gitter.

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

Contributing
------------

If you experience problems with Waggle, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: https://waggle.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _pybee/general: https://gitter.im/pybee/general
.. _BeeWare Community Code of Conduct: http://pybee.org/community/behavior/
.. _log them on Github: https://github.com/pybee/waggle/issues
.. _fork the code: https://github.com/pybee/waggle
.. _submit a pull request: https://github.com/pybee/waggle/pulls
