# Installation and running

## 1. Local installation


### 1.1. Requirements
*Home Storage* requires [Python 3](https://www.python.org/), [pip](https://pypi.org/), and the modules listed in [requirements.txt](../requirements.txt) installable using *pip*.

Either SQLite or PostgreSQL is required for the database.


### 1.2. Obtaining Home Storage
*Home Storage* can be obtained from the Github [homepage for Home Storage](https://github.com/Peanhua/HomeStorage).

Clone the project, or download the zip file and unpack its contents.


### 1.3. Setup the Python environment
Optionally setup a Python virtual environment using the *venv* Python module:

```Shell Session
$ python3 -m venv venv
```

And take the newly created virtual environment into use:

```Shell Session
$ source venv/bin/activate
```

### 1.4. Install remaining requirements

Install the required Python packages listed in [requirements.txt](../requirements.txt):

```Shell Session
$ pip install -r requirements.txt
```


## 2. Heroku installation
*Home Storage* should run out-of-the-box in Heroku. A [Procfile](../Procfile) is provided, it uses *gunicorn* to run *Home Storage*. PostgreSQL database is recommended, and Heroku should automatically setup the *DATABASE_URL* environment variable. For more information about how to use Heroku, see [Heroku](https://www.heroku.com/) web page.



## 3. Running Home Storage
To run *Home Storage*, use the *run.py* script:

```Shell Session
$ ./run.py
```

The following environment variables are recognized and used if present:
<table>
  <tr><th>Variable     </th><th>Value type</th><th>Default      </th><th>Description</th></tr>
  <tr><td>SECRET_KEY   </td><td>String    </td><td>some random data</td><td>Set the Flask SECRET_KEY used for securely signing the session cookie.</td></tr>
  <tr><td>DATABASE_URL </td><td>String    </td><td>sqlite:///homestorage.db</td><td>The database URL used for SQLAlchemy connection.</td></tr>
  <tr><td>DATABASE_ECHO</td><td>Boolean   </td><td>False        </td><td>Controls the SQLALCHEMY_ECHO configuration. Setting DATABASE_ECHO environment variable to any value, turns on SQLALCHEMY_ECHO.</td></tr>
  <tr><td>DEBUG        </td><td>Boolean   </td><td>False        </td><td>If DEBUG environment variable is defined (to any value), turns on debugging mode.</td></tr>
</table>

The variables are also read from ```.env``` using the *python-dotenv* package.
