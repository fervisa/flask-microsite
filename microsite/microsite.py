from flask import Flask, render_template, request
from microsite.db import get_db, query_db
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        db = get_db()
        db.execute('insert into contacts (email, message) values (?, ?)',
                [request.form['email'], request.form['message']])
        db.commit()
        return 'Thanks for reaching out to us, {}'.format(request.form['email'])

@app.cli.command('export_contacts')
def export_contacts():
    contacts = query_db('select * from contacts')
    with open('contacts.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        for contact in contacts:
            writer.writerow([contact['email'], contact['message']])
        print('Contacts have been successfully exported')

@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    if db is not None:
        db.close()
