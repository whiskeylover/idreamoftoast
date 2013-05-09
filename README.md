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
$ source ~/venv/bin/active
$ pip install -r requirements.txt
```

Start the server:

```bash
$ source ~/venv/bin/active (if you're not already in the virtual environent)
$ python toast/app.py
```

License
=======

   Copyright 2013 Ashish Kasturia & Dan Riti

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
