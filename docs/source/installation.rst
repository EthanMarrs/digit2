Installation
============

Ubuntu Linux
 * Run ``apt-get update`` to update your packages list.
 * Run ``sudo apt-get install rabbitmq-server`` to install RabbitMQ.
 * Run ``sudo apt-get install pip`` to install the Pip package manager.
 * Run ``tar -xvf digit.zip`` to extract the code in the current directory.
 * Navigate to the new directory by running ``cd digit2``.
 * Run ``virtualenv -p python3 env`` to create a Python 3 virtual environment.
 * Run ``pip install -r requirements.txt requirments-dev.txt`` to install the required packages.
 * Once all dependencies have been installed, run ``./manage.py runserver``
