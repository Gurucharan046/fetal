# this is an email sending automation codde designed for mailing the attatchment to the customer if required.
# this program is constructed using the simple mail transfer protocol library.
# the email library is used to get or create the email template.
# the to address will be directky fetched from the user loginn credential which will be passed as an arguments.
# the pdf is generated in the app.py file itself and the pdf will be saved in  directory fetal>res.pdf
# the res.pdf file has only one copy in this device whenever a user asks the pdf file we will rewrite the same file with the new data thereby
# storing the data in only one pdf
# we have used smpt library because it is very more user friendly and gmail works flawlessly
# we are using port number 465
# first we read the contents of the file and place it in the sender file using add attachnment
# finally the message is sent to user it takes minimum 10-12 secs to send a fileS
import smtplib
from email.message import EmailMessage


def sendEmailTouser(mailid):

    msgContent = EmailMessage()
    msgContent['Subject'] = 'FETAL HEALTH  PREDICTION REPORT'
    msgContent['From'] = 'MR PREDICTOR'
    msgContent['To'] = mailid
    with open("res.pdf", "rb") as f:
        fileContent = f.read()
        file_name = f.name
        msgContent.add_attachment(
            fileContent, maintype="application", subtype="pdf", filename=file_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("give your mail id here", "give your gmail app code here")
        server.send_message(msgContent)
