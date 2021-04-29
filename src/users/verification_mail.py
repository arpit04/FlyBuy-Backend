import smtplib, ssl
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from src.database import db_session
import src.models as models
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


ph = PasswordHasher(hash_len=64, salt_len=32)

def send_mail(id, handle, email, email_type):
    try:
        the_token = ph.hash(str(handle))[35:]
        tomorrow = datetime.now() + timedelta(days=1)
        if email_type == "new-user":
            print("set new-user token")
            validation_token = models.ValidationToken(token=the_token, created_at=tomorrow, user_id=id)
            db_session.add(validation_token)
        if email_type == "reset-user":
            print("set reset-user token")
            user = db_session.query(models.ValidationToken).filter(models.ValidationToken.user_id == id).one_or_none()
            user.created_at = tomorrow
            user.token=the_token
        db_session.commit()
    except Exception as e:
        print(e)
        print("[ ERROR ] failed to add validation_token")
        return False

    try:
        print("sending verification email...")
        the_token = the_token.replace("/", "_")
  
        if email_type == "new-user":
           pass

        html = f"""
                <html>
                    <body>
                        <a href="http://127.0.0.1:5000/validate_user/{the_token}">
                            click here
                        </a>
                    </body>
                </html>"""

        html = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <div style="background-color:#eee;padding:10px 20px;">
                <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">FlyBuy Verification</h2>
            </div>
            <div style="padding:20px 0px">
                <a href="http://127.0.0.1:5000/validate_user/{the_token}">
                    click here
                </a>
            </div>
            </div>
        </body>
        </html>
        """

        port = 465  # For SSL
        sender_email = "arpitraval786@gmail.com"
        password = "earth@#0402"

        message = MIMEMultipart("alternative")
        message["Subject"] = "User Account Validation"
        message["From"] = sender_email
        message["To"] = email


        part2 = MIMEText(html, "html")  
        message.attach(part2)

       
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, email, message.as_string())

        if email_type == "reset-user": 
            msg = MIMEText(u'<html><body><a href="127.0.0.1:5000/reset_pass/{the_token}">click here</a></body></html>','html')
            body = f"""Hello, {handle} follow this link to validate your email \n {msg}"""
            subject = "User Account Validation"

    except Exception as e:
        print(e)
        print("[ ERROR ] Sending Mail failed")
        return False
    print("[ SUCCESS ] check your email")
    return True

def validate_email(token):
    try:
        token = token.replace("_", "/")
        token = db_session.query(models.ValidationToken).filter(models.ValidationToken.token == token).one_or_none()
        if token is None:
            return False
    except SQLAlchemyError as e:
        print(e)
        print("token not found")
        return False

    try:
        if datetime.now() > token.created_at:
            print("it has been over a day, try again")
            return False
        else:
            user_id = token.user_id
            user_query = db_session.query(models.User).filter(models.User.id == user_id).one_or_none()
            user_query.email_validated = True
            db_session.commit()
            print("email validated")
            return True
    except SQLAlchemyError as e:
        print(e)
        print('problem retrieving user')
        return False

def update_password(token):
    try:
        token = token.replace("_", "/")
        token = db_session.query(models.ValidationToken).filter(models.ValidationToken.token == token).one_or_none()
        if token is None:
            return False, None
    except SQLAlchemyError as e:
        print(e)
        print("token not found")
        return False, None

    try:
        if datetime.now() > token.created_at:
            print("it has been over a day, try again")
            return False, None
        else:
            print("valid token")
            return True, token.user_id
    except SQLAlchemyError as e:
        print(e)
        print('problem retrieving user')
        return False, None
