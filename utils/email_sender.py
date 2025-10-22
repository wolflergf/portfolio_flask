from flask import current_app
from flask_mail import Message, Mail

mail = Mail()

def send_contact_email(name, email, subject, message):
    """
    Send contact form email to the site owner
    
    Args:
        name (str): Name of the person contacting
        email (str): Email of the person contacting
        subject (str): Subject of the message
        message (str): Message content
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject=f"Portfolio Contact: {subject}",
            recipients=[current_app.config['CONTACT_EMAIL']],
            reply_to=email
        )
        
        msg.body = f"""
New contact form submission from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This email was sent from the contact form at wolflergf.com
"""
        
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #2C3E50;">New Contact Form Submission</h2>
    <p>You have received a new message from your portfolio website:</p>
    
    <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
        <tr>
            <td style="padding: 10px; background-color: #f4f4f4; font-weight: bold; width: 100px;">Name:</td>
            <td style="padding: 10px; background-color: #fff;">{name}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background-color: #f4f4f4; font-weight: bold;">Email:</td>
            <td style="padding: 10px; background-color: #fff;"><a href="mailto:{email}">{email}</a></td>
        </tr>
        <tr>
            <td style="padding: 10px; background-color: #f4f4f4; font-weight: bold;">Subject:</td>
            <td style="padding: 10px; background-color: #fff;">{subject}</td>
        </tr>
    </table>
    
    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #1ABC9C; margin: 20px 0;">
        <h3 style="margin-top: 0; color: #2C3E50;">Message:</h3>
        <p style="white-space: pre-wrap;">{message}</p>
    </div>
    
    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
    <p style="color: #7F8C8D; font-size: 12px;">This email was sent from the contact form at <a href="https://wolflergf.com">wolflergf.com</a></p>
</body>
</html>
"""
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False

