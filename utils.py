import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

mail_id = "singhvikashh003@gmail.com"
mail_pass = "qdedxnyxjddqjqbh"


def get_hashed_pass(plain_pass):
    plain_pass = plain_pass.encode("utf-8")
    hash_salt = bcrypt.gensalt(rounds=12)
    pwd = bcrypt.hashpw(plain_pass, salt=hash_salt)
    return pwd

def verify_pass(plain_pass, hashed_pass):
    plain_pass = plain_pass.encode("utf-8")
    hashed_pass = hashed_pass.encode("utf-8")
    return bcrypt.checkpw(plain_pass,hashed_pass)

def setup_smtp():
    mail_conn = smtplib.SMTP('smtp.gmail.com', 587)
    mail_conn.ehlo()
    mail_conn.starttls()
    mail_conn.ehlo()
    mail_conn.login(mail_id, mail_pass)

    return mail_conn

def send_mail(to, subject, mail_body):
    msg = MIMEMultipart()
    msg['From'] = mail_id
    msg['To'] = to
    msg['Subject'] = subject
    message = mail_body
    msg.attach(MIMEText(message))

    mail_conn = setup_smtp()

    mail_conn.sendmail(mail_id, to, msg.as_string())
    mail_conn.quit()   


def reset_password(to, name):
    all_character = string.ascii_letters + string.digits 
    password = ''.join(random.choices(all_character, k=12))
    mail_body = f"""Welcome {name},

Your pass has been reset, please use your new password to login.
Your temp password is {password}

Please change change your password from profile section.



Happy blogging ahead,
The BlogU Crew 
"""
    send_mail(to, "Password Reset - BlogU", mail_body)
    return get_hashed_pass(password)

