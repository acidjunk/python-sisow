.. Python Sisow documentation master file, created by
   sphinx-quickstart on Sat Jul 16 14:01:31 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Sisow's documentation!
========================================

Contents:

.. toctree::
   :maxdepth: 2

This documentation is work in progress.

Running the demo
----------------

.. note:: When running the project from source you'll need the dependencies listed requirements.txt
    You can install them with `pip install -r requirements.txt'

Make sure there is an `account-sisow.secret` file next to `demo.py`, with on the
first line the `merchantid` and on the second line your secret `merchantkey` e.g.:
123456789
abe6cdba7abe6523bcde87623fa54cd45ade2787etc

You Sisow account needs to be configured to allow simulation mode. If you don't enable simulation
mode you'll receive: `sisow.ErrorResponse: TA3410 simulation forbidden`. Enabling Simulation mode is 
simple: Login to the Sisow dashboard and select the "Gevanceerd" tab. 
Enable: `Testen met behulp van simulator (toestaan)`

Now you can run the demo with:
`python demo.py`

Default the program will run in testmode, ensuring no money will be transferred.
To override this, add --no-test:
`python demo.py --no-test`

You can pick your own bank (issuer) using:
`demo.py --list --no-test`

Available banks
05 ING
09 Triodos Bank

Then choose a issuer with:
`python demo.py --bank 09 --no-test`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

