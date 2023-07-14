from flask import flash, redirect, render_template, request, url_for, abort
from timez import app, db
from timez.forms import AddContactForm, UpdateContactForm
from timez.models import Contact
from timez.tzr_utils import TimeKeeper


new_contact = dict()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = list(map(int, request.form.get('time_data').split(':')))
        result = TimeKeeper.time_operation_0(data)
        return "In {} hours {} minutes it'll be: {}".format(data[0], data[1], result)
    else:
        contacts = Contact.query.order_by(Contact.contact_name).all()
        return render_template('index.html', contacts=contacts)


@app.route('/time_operations', methods=['POST', 'GET'])
def time_operations():
    if request.method == 'POST':
        if request.form.get('time_data_1'):
            data = request.form.get('time_data_1')
            print(data)
            result = TimeKeeper().get_current_time(data)
            return f'current time in {data} time zone: {result}'
        elif request.form.get('time_data_2'):  # format "EST;00:00"
            data = request.form.get('time_data_2').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'y')
            return result
        elif request.form.get('time_data_3'):  # format "EST;00:00"
            data = request.form.get('time_data_3').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'n')
            return result

    return render_template('time_operations.html')


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddContactForm()
    if form.validate_on_submit():
        contact = Contact(contact_name=form.contact_name.data, 
                          platform=form.platform.data, 
                          comment=form.comment.data, 
                          location=form.location.data, 
                          zone_name=form.zone_name.data, 
                          utc_offset=form.utc_offset.data)
        print(contact)
        db.session.add(contact)
        db.session.commit()
        flash(f"New contact has been added!", 'success')
        return redirect(url_for('index'))
    return render_template('add.html', title='Add new contact',
                           legend='Add new  contact', form=form)


@app.route("/<int:id>/update", methods=['GET', 'POST'])
def update(id):
    contact = Contact.query.get_or_404(id)
    form = AddContactForm()
    if form.validate_on_submit():
        contact.contact_name = form.contact_name.data
        contact.platform = form.platform.data
        contact.comment = form.comment.data
        contact.location = form.location.data
        contact.zone_name = form.zone_name.data
        if form.utc_offset.data == '':
            contact.utc_offset = None
        else:
            contact.utc_offset = form.utc_offset.data
        contact.utc_offset = form.utc_offset.data
        try:
            db.session.commit()
            flash('Your contact has been updated!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            return f'There was an issue updating contact {contact.contact_name}'
    elif request.method == 'GET':
        form.contact_name.data = contact.contact_name
        form.platform.data = contact.platform
        form.comment.data = contact.comment
        form.location.data = contact.location
        form.zone_name.data = contact.zone_name
        form.utc_offset.data = contact.utc_offset
    return render_template('add.html', title='Update Contact',
                           form=form, legend='Update Contact')


@app.route('/<int:id>/delete')
def delete(id):
    contact_to_delete = Contact.query.get_or_404(id)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        flash('Contact has been deleted!', 'success')
        return redirect(url_for('index'))
    except:
        return f'There was a problem deleting contact <{contact_to_delete.content}>'


