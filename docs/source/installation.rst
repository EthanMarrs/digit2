Installation
============

Ubuntu Linux
 * Run ``apt-get update`` to update your packages list.
 * Run ``sudo apt-get install rabbitmq-server`` to install RabbitMQ.
 * Run ``sudo apt-get install imagemagick`` to install imagemagick
 * Run ``sudo apt-get install pip`` to install the Pip package manager.
 * Run ``tar -xvf digit.zip`` to extract the code in the current directory.
 * Navigate to the new directory by running ``cd digit2``.
 * Run ``virtualenv -p python3 env`` to create a Python 3 virtual environment.
 * Run ``source env/bin/activate`` to activate the virtual environment
 * Run ``pip install -r requirements.txt requirments-dev.txt`` to install the required packages.
 * Once all dependencies have been installed, run ``./manage.py runserver``

macOS (assumes brew is installed)
 * Run ``brew update`` to update your packages list.
 * Run ``brew install rabbitmq`` to install RabbitMQ.
 * Run ``sudo easy_install pip`` to install the Pip package manager.
 * Run ``tar -xvf digit.zip`` to extract the code in the current directory.
 * Navigate to the new directory by running ``cd digit2``.
 * Run ``virtualenv -p python3 env`` to create a Python 3 virtual environment.
 * Run ``source env/bin/activate`` to activate the virtual environment
 * Run ``pip install -r requirements.txt requirments-dev.txt`` to install the required packages.
 * Once all dependencies have been installed, run ``./manage.py runserver`` to start the development server
 * If you want scheduled tasks to execute, run ``celery -A digit beat -l info -S django`` in one terminal window,
   and ``celery --app=digit.celery  worker --loglevel=info`` in another
