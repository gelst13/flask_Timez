from flask import flash, redirect, render_template, request,\
    url_for, Blueprint
from timez import db
from timez.contacts.forms import AddContactForm
from timez.models import Contact


contacts = Blueprint('contacts', __name__)


@contacts.route("/add", methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('add.html', title='Add new contact',
                           legend='Add new  contact', form=form)


@contacts.route("/<int:id>/update", methods=['GET', 'POST'])
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
            return redirect(url_for('main.index'))
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


@contacts.route('/<int:id>/delete')
def delete(id):
    contact_to_delete = Contact.query.get_or_404(id)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        flash('Contact has been deleted!', 'success')
        return redirect(url_for('main.index'))
    except:
        return f'There was a problem deleting contact <{contact_to_delete.content}>'

