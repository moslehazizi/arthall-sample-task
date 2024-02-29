Arthallco sample task

Setup

The first thing to do is to clone the repository:

    $ git clone https://github.com/moslehazizi/arthall-sample-task.git
    $ cd arthall-sample-task

Then create a virtual environment to install dependencies in and activate it:

    $ python3 -m venv .venv
    $ source .venv/bin/activate

Now You must see the (.venv) in front of the prompt. Then install dependencies:

    (.venv)$ python -m pip install -r requirements.txt

Now:

    (.venv)$ python manage.py runserver

See django admin site with superuser:

    email: arthalladmin@email.com
    password: 123456

You can log in as admin:

    email: testadmin@email.com
    password: test123456

And log in as artist:

    email: testartist1@email.com
    password: test123456

There is a pdf file in document folder in project main directory that I made it to explain what I have done.
