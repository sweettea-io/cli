Hosting Predictions
===================

Once you've `trained your model`_ on the training cluster, one command is all it takes to host your model's
predictions behind a secure, production-ready websocket::

  $ tensorci serve

Running the ``serve`` command deploys the commit associated with your latest training deploy to your TensorCI team's
dedicated API cluster. Once this deploy succeeds, your trained model is fetched from TensorCI model storage and
the ``predict`` function specified in ``.tensorci.yml`` is registered with the websocket server.

Full Deploys
------------

Rather than deploying to the training cluster and the API cluster in two separate steps (``tensorci train`` + ``tensorci serve``),
these commands have a combined alias::

  $ tensorci push

Next Steps
----------

Now that your model's predictions are being hosted from a websocket server, its predictions can be fetched with the
`TensorCI API Client Library`_.

.. _`trained your model`: /training.html
.. _`TensorCI API Client Library`: /api_client.html
