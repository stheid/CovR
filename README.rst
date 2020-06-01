====
CovR
====

|docker-build| |docker-size| |website|

.. |docker-build| image:: https://img.shields.io/docker/cloud/build/stefanheid/covr
   :target: https://hub.docker.com/r/stefanheid/covr/builds    

.. |docker-size| image:: https://img.shields.io/docker/image-size/stefanheid/covr/latest
   :target: https://hub.docker.com/r/stefanheid/covr/

.. |website| image:: https://img.shields.io/website?url=http%3A%2F%2Fcovr.sheid.de
   :target: http://covr.sheid.de


Simple flask project serving a plot of the current Covid19 reproductionrate R in Germany (Data from the RKI)

Execute
-------

::

$ docker pull stefanheid/covr:latest
$ docker run stefanheid/covr:latest
