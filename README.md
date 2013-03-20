idreamoftoast
=============

All day long, I dream of toast.

# Setup

Install prerequisites and setup a virtual environment (if needed):

```bash
$ sudo apt-get install python-pip
$ pip install virtualenv
$ virtualenv ~/venv
```

Install toast:

```bash
$ source ~/venv/bin/active
$ git clone git@github.com:whiskeylover/idreamoftoast.git
$ cd idreamoftoast/
$ pip install -r requirements.txt
```

Start the server:

```bash
$ source ~/venv/bin/active
$ python toast/app.py
```
