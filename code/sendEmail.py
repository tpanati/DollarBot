import csv
import re
import helper
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# === Documentation of sendEmail.py ===

def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the sendEmail feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function. It calls helper.py to get the user's
    historical data and based on whether there is data available, it either prints an error message or
    send an email with the csvFile - the user's historical data.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        if user_history is None:
            raise Exception("Sorry! No spending records found!")
        if len(user_history) == 0:
            raise Exception("Sorry! No spending records found!")
        else:
            category = bot.send_message(message.chat.id, "Enter your email id")
            bot.register_next_step_handler(category, acceptEmailId, bot)   

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops! " + str(e))

def acceptEmailId(message, bot):
    email = message.text
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        try:
            chat_id = message.chat.id
            user_history = helper.getUserHistory(chat_id)
            table = [["Date", "Category", "Amount"]]
            if user_history is None:
                raise Exception("Sorry! No spending records found!")
            if len(user_history) == 0:
                raise Exception("Sorry! No spending records found!")

            else:
                for rec in user_history:
                    values = rec.split(',')
                    # Store each value in separate variables
                    date, category, amount = values
                    table.append([date, category, "$ " + amount])

                with open('history.csv', 'w', newline = '', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(table)

                mail_content = '''Hello,
                This email has an attached copy of your expenditure history.
                Thank you!
                '''
                #The mail addresses and password
                sender_address = 'secheaper@gmail.com'
                #sender_pass = 'csc510se'
                sender_pass = 'lrmd uazh dshu xcxi'
                receiver_address = email
                #Setup the MIME
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = 'Spending History document'
                #The subject line
                #The body and the attachments for the mail
                message.attach(MIMEText(mail_content, 'plain'))
                attach_file_name = "history.csv"
                attach_file = open(attach_file_name, 'rb')
                payload = MIMEBase('application', 'octet-stream')
                payload.set_payload((attach_file).read())
                encoders.encode_base64(payload) #encode the attachment
                #add payload header with filename
                payload.add_header('Content-Disposition', f'attachment; filename={attach_file_name}')
                message.attach(payload)
                #Create SMTP session for sending the mail
                session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
                session.starttls() #enable security
                session.login(sender_address, sender_pass) #login with mail_id and password
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)
                session.quit()
                bot.send_message(chat_id, "Mail Sent")

        except Exception as ex:
            logging.error(str(ex), exc_info=True)
            bot.reply_to(message, str(ex))
    else:
        bot.send_message(message.chat.id, 'incorrect email')