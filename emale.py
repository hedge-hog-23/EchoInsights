import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Login to the server using the app password
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email

# Example usage:
sender_email = "xero.prints231@gmail.com"
sender_password = "gzdj nogr mofu pbzs"  # Use the app password here
receiver_email = "210701241@rajalakshmi.edu.in"
subject = "Test Subject"
message = "CFC BAIII !!"

send_email(sender_email, sender_password, receiver_email, subject, message)
