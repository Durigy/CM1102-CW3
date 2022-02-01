# CM1102-CW3
This is the E-commerce shop that I made in Flask for my CM1102 CW

------------------------------------------------------------------

Python version: 3.6

### Required set up configurations:

It is good practice to create a virtual environment for the project
this can be done in the folder root folder using the following windows (or equivalent) terminal commands

    > py -m venv venv

    > venv\Scripts\activate

    > py -m pip install -r requirements.txt

note: if you do not activate the venv before installing the requirements.txt,
then it will be installed in your main python directory

-----------------------------------------------------

In-order to connect to a database either create a file in ./shop/ called 'db_var.py'
this must contain the folowing variables (shown using mysql):

```python
SECRET_KEY = '<- add secret key here ->' 

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<- DB Password ->@<- DB domain/IP (localhost normally) ->/<- DB Name ->'
```

> SQLALCHEMY_DATABASE_URI: replace the <- -> with the correct info

or

**change the config settings to something more relevant**

app.config['SECRET_KEY'] = *db_var.SECRET_KEY*

app.config['SQLALCHEMY_DATABASE_URI'] = *db_var.SQLALCHEMY_DATABASE_URI*

-----------------------------------------------------

### Secret key generation  
Use the following python commands to generate a secret key:

    > python

    >>> import os

    >>> os.urandom(24).hex()

-----------------------------------------------------

### To add the tables to your local testing database, for example
you can use the following commands:

    > python

    >>> from main import db

    >>> db.create_all()

-----------------------------------------------------
