|image0|

Python Library and CLI for the Pwned Password v2 API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|Version| |Python Versions|

About
-----

From https://haveibeenpwned.com/API/v2#PwnedPasswords:

    Pwned Passwords are more than half a billion passwords which have
    previously been exposed in data breaches. The service is detailed in
    the `launch blog
    post <https://www.troyhunt.com/introducing-306-million-freely-downloadable-pwned-passwords/>`__
    then `further expanded on with the release of version
    2 <https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2>`__.
    The entire data set is `both downloadable and searchable online via
    the Pwned Passwords page <https://haveibeenpwned.com/Passwords>`__.

``pwnedpasswords`` is a small Python wrapper and command line utility
that exposes the functionality of the Pwned Passwords API.

Installation
------------

pwnedpasswords is available for download through
`PyPi <https://pypi.python.org/pypi/pwnedpasswords>`__. You can install
it right away using pip.

.. code:: bash

    pip install pwnedpasswords

--------------

Usage
-----

.. code:: python

    import pwnedpasswords
    password = pwnedpasswords.Password("testing 123")

    # Return the number of times `testing 123` appears in the Pwned Passwords database.
    password.check()

And that’s it! You’re done.

Notes
^^^^^

pwnedpasswords will automatically check to see if your provided input
looks like a SHA-1 hash. If it looks like plain text, it’ll
automatically hash it before sending it to the Pwned Passwords API.

If you’d like to provide an already-hashed password as input, you don’t
need to do anything special–pwnedpasswords will detect that it looks
like a SHA-1 hash and will not hash it again before providing it as
input to the Pwned Passwords API.

.. code:: python

    password = pwnedpasswords.Password("b8dfb080bc33fb564249e34252bf143d88fc018f")

Likewise, if a password *looks* like a SHA-1 hash, but is actually a
user-provided password, set ``plain_text`` to ``True``, so that the
library knows to hash it before checking it against the database.

.. code:: python

    password = pwnedpasswords.Password("1231231231231231231231231231231231231231", plain_text=True)

``check``
~~~~~~~~~

This is the preferred method to call the Pwned Passwords API. By
default, the ``check`` method uses the
``https://api.pwnedpasswords.com/range/`` endpoint, which is
`k-anonymous <https://en.wikipedia.org/wiki/K-anonymity>`__.

.. code:: python

    password = pwnedpasswords.Password("username")
    password.check()
    # 8340

If you’d like to force pwnedpasswords to use the search endpoint instead
(https://api.pwnedpasswords.com/pwnedpassword/), set the ``anonymous``
parameter to ``False``.

.. code:: python

    password = pwnedpasswords.Password("password")
    password.check(anonymous=False)
    # 3303003

You might want to do this if you’d prefer faster response times, and
aren’t that worried about leaking passwords you’re searching for over
the network.

Lower-level Usage
-----------------

If you’d like direct access to the search and range endpoints, you can
call them directly.

``search``
~~~~~~~~~~

.. code:: python

    password = pwnedpasswords.Password("testing 123")
    password.search()
    # outputs 1

``range``
~~~~~~~~~

.. code:: python

    password = pwnedpasswords.Password("098765")
    password.range()
    # outputs a dictionary mapping SHA-1 hash suffixes to frequency counts

Command Line Utility
--------------------

pwnedpasswords comes bundled with a handy command line utility for
checking passwords against the Pwned Passwords database.

.. code:: bash

    $ pwnedpasswords 123456password
    240

The output is simply the number of entries returned from the Pwned
Passwords database.

If you’d like to use the CLI in a script, pwnedpasswords returns an exit
code equal to the base-10 log of the result count, plus 1. If there are
no matches in the API, the exit status will be ``0``.

If you’d like to take a look under the hood to make sure things are
working as they should, set the ``--verbose`` flag.

.. code:: bash

    $ pwnedpasswords 123456password --verbose
    INFO:pwnedpasswords.pwnedpasswords:https://api.pwnedpasswords.com/range/5052C
    INFO:pwnedpasswords.pwnedpasswords:Entry found
    240

Support/Questions
-----------------

Please file an issue in GitHub if you run into any issues, or would like
to contribute. Thanks!

License
-------

Apache License, Version 2.0. See `LICENSE <LICENSE>`__ for details.

.. |image0| image:: meta/repo-banner.png
.. |Version| image:: https://img.shields.io/pypi/v/pwnedpasswords.svg?style=flat
   :target: https://pypi.python.org/pypi/pwnedpasswords
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/pwnedpasswords.svg?style=flat
   :target: https://pypi.python.org/pypi/pwnedpasswords
