from flask import flash, redirect, render_template, request,\
    url_for, Blueprint
from timez.models import Contact


main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass  # to clean!
        # data = list(map(int, request.form.get('time_data').split(':')))
        # result = TimeKeeper.time_operation_0(data)
        # return "In {} hours {} minutes it'll be: {}".format(data[0], data[1], result)
    else:
        contacts = Contact.query.order_by(Contact.contact_name).all()
        return render_template('index.html', contacts=contacts)
