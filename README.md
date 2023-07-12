###Usage:
In Your Terminal(command line) run:
python tzr.py

###PROJECT HISTORY
26.06.2023 - created flask_version branch and started building flask app

After importing class from tzr_utils.py I got a problem with starting server:
turned out, I had to turn off logging inside that module (with logging module)

Found out about @property in python and used it in sqlalchemy model -
to run a method from a class of tzr_utils.py in order to paste returned result
inside jinja2 code in .html template