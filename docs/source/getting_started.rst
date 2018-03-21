Getting Started
===============

This document will show you how to get up and running with TensorCI. You will learn how to create your
TensorCI account, install the CLI, and create your first TensorCI project.

Create an Account
-----------------

Before doing anything else, you will need to create a TensorCI account. Doing this is easy --
just visit the `TensorCI home page`_ and sign up with GitHub.

Once you've signed in, you should be taken to the TensorCI dashboard and prompted to create a basic auth password.
This password is required in order to login to the TensorCI CLI. If you're not automatically prompted to do this on
your first visit to the dashboard, you can use `this link`_ instead.

Install the CLI
---------------

The TensorCI CLI is the easiest way to interact with your TensorCI resources. It provides commands for creating datasets,
deploying your models for training, downloading your trained models, and serving model predictions from your TensorCI API, among
others.

Assuming you have Python_ already, you can install the CLI with ``pip``::

  $ pip install tensorci

Login from the CLI
-------------------

Now that you have the ``tensorci`` command-line tool, you should be able to login to your TensorCI account using your
GitHub username and the basic auth password you just created::

  $ tensorci login

Create a New Project
--------------------

To register your git repo as a TensorCI project, navigate to your project's directory, and run::

  $ tensorci init

This will create a ``.tensorci.yml`` config file in the root of your project with the following contents::

  #
  # Python TensorCI configuration file
  #
  model:         path/to/model/file
  prepro_data:   module1.module2:function
  train:         module1.module2:function
  test:          module1.module2:function
  predict:       module1.module2:function
  reload_model:  module1.module2:function

These config values will need to be modified to fit your project, but not all of them need to be set in order to simply train your
first model. The table below describes these config values in more depth, gives examples for each, and explains when
each value is required (if at all).

.. list-table:: Config Key Descriptions
  :widths: 20 40 20 20
  :header-rows: 1

  * - Key
    - Value
    - Example
    - Required For
  * - ``model``
    - .. line-block::
        Relative path to save model to and read
        model from
    - ``data/model/``
    - Always
  * - ``prepro_data``
    - .. line-block::
        Path to module function used to
        preprocess raw dataset before training
    - ``src.dataset:prepro``
    - Training
  * - ``train``
    - .. line-block::
        Path to module function that trains
        your model
    - ``src.model:train``
    - Training
  * - ``test``
    - .. line-block::
        Path to module function that tests
        your model's accuracy after training
    - ``src.model:test``
    - Optional
  * - ``predict``
    - .. line-block::
        Path to module function used to make
        model predictions from behind an API
    - ``src.model:predict``
    - Predictions
  * - ``reload_model``
    - .. line-block::
        Path to module function used to reload
        latest model into memory when swapping
        out old model
    - ``src.model:reload``
    - Predictions

Once you've modified this config file to integrate with your project, go ahead and push these changes up to GitHub.

**Note:**  Now that you've created your TensorCI project, you can easily navigate to its web dashboard counterpart at any time by
running ``tensorci dash`` from the root of your project.

Congrats! That's all it takes to set up a TensorCI project. The last thing you need to do before you're ready to start
training is :doc:`create a TensorCI Dataset<./datasets>`. Once that's done, you'll be ready to :doc:`train your model<./training>` on
the TensorCI training cluster.

Next Steps
----------

* :doc:`Create a dataset<./datasets>`
* :doc:`Train your model<./training>`
* :doc:`Host your model's predictions<./predictions>`

.. _`Python`: https://www.python.org/
.. _`TensorCI home page`: https://www.tensorci.com
.. _`this link`: https://app.tensorci.com/account/auth