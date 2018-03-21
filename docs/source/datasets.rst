Datasets
========

In order for the TensorCI training cluster to train a model on your data, it first needs a location where it
can access that data in a fast, reliable manner. To achieve this, datasets uploaded to TensorCI are converted into
tables in a cloud database. This not only makes your data easily accessible from the training cluster, but it also
allows your data to live in one specific location that easily handles updates via an API as new data accumulates over time.

Create a Dataset
------------------

To create a TensorCI dataset for your project, navigate to the root of your project and run the following command::

  $ tensorci create dataset --file path/to/dataset.json

Currently, only JSON files are supported for seeding TensorCI datasets (CSV support coming soon).

Once you've created a dataset, you can verify its creation by checking the **Datasets** tab of the TensorCI dashboard and
selecting your project. The dataset should be listed, along with when it was created, the number of records it currently
has, and a button for previewing its first 5 records. There will also be a dropdown where you can specify your dataset's
**Retrain Step Size** -- the number of new records added to the dataset at which your model will automatically start
retraining.

Next Steps
----------

* :doc:`Train your model<./training>`
* :doc:`Host your model's predictions<./predictions>`