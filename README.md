# Build Instructions.

You can do this with or without a venv but I am gonna try include usage of a venv in the instructions.

* Make sure you have python 3.6 installed.
* `pip3 install virtualenv`
* Extract the project zip I sent you and open up a terminal to the project folder location.
*  `virtualenv collect-venv` This will create a virtual env.
*  `source collect-venv/bin/activate`
*  `pip install -r requirements.txt`
* Download a credentials file from https://developers.google.com/sheets/api/quickstart/python by clicking the button under the Step 1.
Store these credentials file under `/srv/collect/credentials.json`.  This is a quickstart auth system for google sheets and is handy for POC versions of the app.
* Migrate the database using `python manage.py migrate`.

To start a web server run `python manage.py runserver`. A web server will start up at `localhost:8000`.

A POSTMAN API collection is included with for experimentation.
