TensorCI API Client
===================

The `TensorCI API Client`_ is the easiest way to fetch predictions from your trained TensorCI models.

Installation
------------

Assuming you have Python_ already, this library can be installed with ``pip``::

  $ pip install tensorci_client

Fetch Model Predictions
-----------------------
Once you've `deployed a trained model`_ to your team's TensorCI API cluster, fetching that model's predictions involves the following
3 steps:

**1.Obtaining API Credentials**

Each TensorCI project comes with its own **Client ID** and **Client Secret** to secure its hosted model predictions.
These credentials can be found on the TensorCI Dashboard at ``https://app.tensorci.com/<TEAM_SLUG>/<PROJECT_SLUG>/settings``.

**2. Setting API Credentials as Environment Variables**

Once you've obtained your API credentials, set the following environment variables in the Python project you wish to fetch
model predictions from:

  * ``TENSORCI_CLIENT_ID``
  * ``TENSORCI_CLIENT_SECRET``
  * ``TENSORCI_TEAM``
  * ``TENSORCI_PROJECT``

**3. Initializing the TensorCI Client**

Once you've set the above environment variables, model predictions can be fetched in the following manner::

  from tensorci import TensorCI

  client = TensorCI()

  unseen_features = {
    'key1': 'val1',
    'key2': 'val2'
  }

  prediction = client.predict(data=unseen_features)

  print('Got Prediction: {}'.format(prediction))

.. _Python: https://www.python.org/
.. _`TensorCI API Client`: https://github.com/tensorci/tensorci-client
.. _`deployed a trained model`: /predictions.html
