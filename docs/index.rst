Documentation
=============

--------------

**This project was generated with:** `fastapi-mvc <https://github.com/fastapi-mvc/fastapi-mvc>`__

--------------

Quickstart
~~~~~~~~~~

If You want to go easy way and use provided virtualized environment You'll need to have installed:

* rsync
* Vagrant `(How to install vagrant) <https://www.vagrantup.com/downloads>`__
* (Optional) Enabled virtualization in BIOS

First run ``vagrant up`` in project root directory and enter virtualized environment using ``vagrant ssh``
Then run following commands to bootstrap local development cluster exposing ``fastapi-mvc`` application.

.. code-block:: bash

    cd /syncd
    make dev-env

.. note::
    This process may take a while on first run.

Once development cluster is up and running you should see summary listing application address:

.. code-block:: bash

    Kubernetes cluster ready

    fastapi-mvc available under: http://example.192.168.49.2.nip.io/

    You can delete dev-env by issuing: minikube delete

.. note::
    Above address may be different for your installation.

    Provided virtualized env doesn't have port forwarding configured which means, that bootstrapped application stack in k8s won't be accessible on Host OS.

Deployed application stack in Kubernetes:

.. code-block:: bash

    vagrant@ubuntu-focal:/syncd$ make dev-env
    ...
    ...
    ...
    Kubernetes cluster ready
    FastAPI available under: http://example.192.168.49.2.nip.io/
    You can delete dev-env by issuing: make clean
    vagrant@ubuntu-focal:/syncd$ kubectl get all -n example
    NAME                                                     READY   STATUS    RESTARTS   AGE
    pod/example-7f4dd8dc7f-p2kr7                1/1     Running   0          55s
    pod/rfr-redisfailover-persistent-keep-0                  1/1     Running   0          3m39s
    pod/rfr-redisfailover-persistent-keep-1                  1/1     Running   0          3m39s
    pod/rfr-redisfailover-persistent-keep-2                  1/1     Running   0          3m39s
    pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-2r7th   1/1     Running   0          3m39s
    pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-6kqv5   1/1     Running   0          3m39s
    pod/rfs-redisfailover-persistent-keep-5d46b5bcf8-sgtvv   1/1     Running   0          3m39s

    NAME                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)     AGE
    service/example                ClusterIP   10.110.42.252   <none>        8000/TCP    56s
    service/rfs-redisfailover-persistent-keep   ClusterIP   10.110.4.24     <none>        26379/TCP   3m39s

    NAME                                                READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/example                1/1     1            1           55s
    deployment.apps/rfs-redisfailover-persistent-keep   3/3     3            3           3m39s

    NAME                                                           DESIRED   CURRENT   READY   AGE
    replicaset.apps/example-7f4dd8dc7f                1         1         1       55s
    replicaset.apps/rfs-redisfailover-persistent-keep-5d46b5bcf8   3         3         3       3m39s

    NAME                                                 READY   AGE
    statefulset.apps/rfr-redisfailover-persistent-keep   3/3     3m39s

    NAME                                                                  AGE
    redisfailover.databases.spotahome.com/redisfailover-persistent-keep   3m39s
    vagrant@ubuntu-focal:/syncd$ curl http://example.192.168.49.2.nip.io/api/ready
    {"status":"ok"}
Documentation
-------------

This part of the documentation guides you through all of the features and usage.

.. toctree::
   :maxdepth: 2

    install
    nix
    usage
    deployment


API Reference
-------------

If you are looking for information on a specific function, class, or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Miscellaneous Pages
-------------------

.. toctree::
   :maxdepth: 2

   license
   CHANGELOG.md
