CowCV
=====

|Build Status| |Coverage Status|

A CV tool for extracting cows from images.

Uses OpenCV and `PIL/Pillow <https://pillow.readthedocs.io/en/3.3.x/>`_. 

Description
-----------

- `Märkning och registrering av nötkreatur <http://www2.jordbruksverket.se/webdav/files/SJV/trycksaker/Jordbruksstod/js31v2.pdf>`_
- `Godkänd märkningsutrustning för nötkreatur <http://www2.jordbruksverket.se/download/18.3a2dd4ec14f19a09a8b52d0a/1439294577516/jsi34_v5.pdf>`_
- `Föreskrifter om ändring i Statens jordbruksverks föreskrifter (SJVFS 2007:12) om märkning och registrering av nötkreatur <http://www.jordbruksverket.se/download/18.33162a40151bcaffe88c1520/1450682394669/2015-044.pdf>`_


Installation
------------

::

    pip install git+https://www.github.com/hbldh/cowcv

Usage
-----


Tests
~~~~~

Tests can be run with `pytest <http://doc.pytest.org/en/latest/>`_:

.. code:: sh

    hbldh@devbox:~/Repos/cowcv py.test tests
    ============================= test session starts ==============================
    platform linux -- Python 3.5.2, pytest-3.0.2, py-1.4.31, pluggy-0.3.1
    rootdir: /home/hbldh/Repos/cowcv, inifile: 
    collected 0 items 

    ========================== 0 passed in 0.0 seconds =============================

References
----------

.. |Build Status| image:: https://travis-ci.org/hbldh/cowcv.svg?branch=master
   :target: https://travis-ci.org/hbldh/cowcv
.. |Coverage Status| image:: https://coveralls.io/repos/github/hbldh/cowcv/badge.svg?branch=master
   :target: https://coveralls.io/github/hbldh/cowcv?branch=master
