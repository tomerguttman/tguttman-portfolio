from flask import Flask, render_template, url_for, request, redirect
import smtplib
import csv

app = Flask(__name__)

def write_to_db(data):
    with open('database.txt', mode='a') as db:
        email = data['email']
        name = data['name']
        subject = data['subject']
        message = data['message']
        file = db.write(f'\n{email},{name},{subject},{message}')

def write_to_csv(data):
        with open('database.csv', mode='a',newline='') as csv_db:
            email = data['email']
            name = data['name']
            subject = data['subject']
            message = data['message']
            csv_writer = csv.writer(csv_db, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
            csv_writer.writerow([email,name,subject,message])




def send_mail(i_sender_name, i_sender_email, i_subject, i_message):
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            website_email_address = 'Website email'
            server.login(website_email_address, "Website email password")
            formatted_message = f'From: {i_sender_email}, {i_sender_name}\nSubject: {i_subject}\nMessage: {i_message}'
            server.sendmail(website_email_address, 'Personal email', formatted_message)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name + '.html')

@app.route('/submit_form', methods = ['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            write_to_csv(request.form.to_dict())
            # write_to_db(request.form.to_dict())
            # send_mail(name, email, subject, message) uncomment and edit send_mail function so the website will send you email when people try to contact you.
            return redirect('/thankyou')
        except:
            return 'data was not saved in database'
    else:
        return '<Error: not a post request>'
    
