from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.message import EmailMessage

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/templates/static')
app.secret_key = 'supersecretkey'

SMTP_HOST = '127.0.0.1'
SMTP_PORT = 8025

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sender = request.form.get('sender')
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        body = request.form.get('body')
        if not sender or not recipient or not subject or not body:
            flash('All fields are required!')
            return redirect(url_for('index'))
        try:
            msg = EmailMessage()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.set_content(body)
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.send_message(msg)
            flash('Email sent successfully!')
        except Exception as e:
            flash(f'Error sending email: {e}')
        return redirect(url_for('index'))
    return render_template('email_server.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)