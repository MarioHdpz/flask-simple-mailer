"""Simple flask email sender"""
import os

from flask import Flask, request

from mail import sender

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["AWS_SES_SENDER"] = os.environ.get("AWS_SES_SENDER")
app.config["AWS_SES_REGION_NAME"] = os.environ.get("AWS_SES_REGION_NAME")
app.config["AWS_ACCESS_KEY_ID"] = os.environ.get("AWS_ACCESS_KEY_ID")
app.config["AWS_SECRET_ACCESS_KEY"] = os.environ.get("AWS_SECRET_ACCESS_KEY")

email_sender = sender.SESMailer(app)

recipients = os.environ.get("RECIPIENTS").split(",")
subject = os.environ.get("SUBJECT", "Form submit")

@app.route('/', methods=['POST'])
def send_mail():
    content = ""
    for key, value in request.form.items():
        content += f"{key}: {value}\n"
    email_sender.send_email(
        recipients,
        subject=subject,
        content=content
    )
    return "", 204
