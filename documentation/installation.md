# Installation and running

## 1. Installation


### 1.1. Requirements
*Home Storage* requires [Python 3](https://www.python.org/), [pip](https://pypi.org/), and the following modules installable using *pip*:
```
bcrypt==3.1.6
cffi==1.12.2
Click==7.0
Flask==1.0.2
Flask-Bcrypt==0.7.1
Flask-Login==0.4.1
Flask-Markdown==0.3
Flask-SQLAlchemy==2.3.2
Flask-WTF==0.14.2
gunicorn==19.9.0
itsdangerous==1.1.0
Jinja2==2.10
Markdown==3.1
MarkupSafe==1.1.1
psycopg2==2.7.7
pycparser==2.19
python-dotenv==0.10.1
six==1.12.0
SQLAlchemy==1.3.1
Werkzeug==0.14.1
WTForms==2.2.1
```


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



## 2. Running Home Storage
To run *Home Storage*, use the *run.py* script:

```Shell Session
$ ./run.py
```

The following environment variables are recognized and used if present:
<table>
  <tr><th>Variable     </th><th>Value type</th><th>Default      </th><th>Description</th></tr>
  <tr><td>SECRET_KEY   </td><td>String    </td><td>*random data*</td><td>Set the Flask SECRET_KEY used for securely signing the session cookie.</td></tr>
  <tr><td>DATABASE_URL </td><td>String    </td><td>sqlite:///homestorage.db</td><td>The database URL used for SQLAlchemy connection.</td></tr>
  <tr><td>DATABASE_ECHO</td><td>Boolean   </td><td>False        </td><td>Controls the SQLALCHEMY_ECHO configuration.</td></tr>
</table>

The variables are also read from ```.env``` using the *python-dotenv* package.
