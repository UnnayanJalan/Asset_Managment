import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import mailtrap as mt

from config import settings

# mail = mt.Mail(
#     sender=mt.Address(email="hello@demomailtrap.co", name="Mailtrap Test"),
#     to=[mt.Address(email="unnayan.jalan@acldigital.com")],
#     subject="You are awesome!",
#     text="Congrats for sending test email with Mailtrap!",
#     category="Integration Test",
# )

# client = mt.MailtrapClient(token="<YOUR_API_TOKEN>")
# response = client.send(mail)

# print(response)

def send_email(to_email: str, password: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.MAIL_USERNAME
        msg["To"] = to_email
        msg["Subject"] = "Your Account Credentials"

        body = f"""
Your account has been created.

Email: {to_email}
Password: {password}

Please login and change your password.
"""

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)

        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email failed:", str(e))

        print("📤 Sending email to:", to_email)