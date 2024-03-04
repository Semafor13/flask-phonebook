from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from config import Config
from models import db, Contact

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        contact = Contact(name=name, phone_number=phone_number)
        db.session.add(contact)
        db.session.commit()
        flash('Contact added successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('add_contact.html')


@app.route('/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone_number = request.form['phone_number']
        db.session.commit()
        flash('Contact updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_contact.html', contact=contact)


@app.route('/delete/<int:contact_id>')
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = Contact.query.filter(Contact.name.contains(query)).all()
    return render_template('search_results.html', results=results, query=query)


@app.route('/view/<int:contact_id>')
def view_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template('view_contact.html', contact=contact)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
