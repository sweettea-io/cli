Model Training
==============

Once you've `created a dataset`_, training your model on the TensorCI training cluster is easy::

  $ tensorci train

Running the ``train`` command deploys the latest commit of your project's git repo to the TensorCI training cluster.
Once deployed, the following steps are performed, in order:

1. All records in your project's dataset are fetched from its TensorCI datatable.
2. If specified, the ``prepro_data`` function specified in ``.tensorci.yml`` is called if the dataset has changed.
3. The ``train`` function specified in ``.tensorci.yml`` is called.
4. If specified, the ``test`` function specified in ``.tensorci.yml`` is called.
5. The trained model specified in ``.tensorci.yml`` is uploaded to TensorCI model storage.

Watch Training Logs
-------------------
Once a training deploy has succeeded, watching the real-time logs for steps 2-4 above can be initiated with the following
command::

  $ tensorci logs --follow

If the ``--follow`` flag is not provided, a dump of all the logs up to this point for this deploy are returned.

Fetch a Trained Model
---------------------
Once training has finished and the trained model has been uploaded to TensorCI model storage, that model can be pulled
locally by running the following command::

  $ tensorci get model

This saves the model to the path specified in the ``.tensorci.yml`` config file, unless the ``--output`` argument is
provided to specify another path.

Next Steps
----------

* `Host your model's predictions`_

.. _`Host your model's predictions`: /predictions.html
.. _`created a dataset`: /datasets.html

