# this is a rendering program. We are using flask module for our rendering purpose.
# Initial development phase: We have the predict_form where we will take the input
# then pass the input to the function which returns a template along with the  value
# of the inputs for showing the results
# importing our fetal_predict.py to use fetalHealtPredictor function

from datetime import date
from distutils.log import info
from http import client
import shutil
from statistics import mean
from tkinter.messagebox import QUESTION
# from flask.helpers import make_response

from turtle import update
from idna import check_initial_combiner


from requests import session
from sklearn import semi_supervised
import fetal_predict as fp
# importing flask for rendering , render_template to render html file,request to take input values
from flask import Flask, render_template, redirect, url_for, request, make_response, session
from emailSend import sendEmailTouser
import pymongo
import requests
import json
app = Flask(__name__)
app.secret_key = 'mkiytres#@'
value = 0
currInformationHold1 = []
currInformationHold = []
contents = []
newData = []
global updatedata
global medicaldata
updatedata = []
medicaldata = []
global aid
aid = []
global elist
elist = []
global mailid
mailid = []


def setMailId(str):
    del mailid[:]
    mailid.append(str)


def getMailId():
    return mailid


def takeMedicalValues(lst):
    del medicaldata[:]
    for i in lst:
        medicaldata.append(i)


def getMedicalValues():
    return medicaldata


def getMeaning(a):
    if a == 1:
        return "NORMAL"
    elif a == 2:
        return "SUSPECT"
    else:
        return "PATHOLOGICAL"


def takeAnsId(a):
    del aid[:]
    aid.append(a)


def anotherList(lst):
    del elist[:]
    for i in lst:
        elist.append(i)


def returnList():
    return elist


def getAnsid():
    return aid


def takeValues(lst):
    del updatedata[:]  # without this line the end output will have a problem
    for i in lst:
        updatedata.append(i)


def getValues():
    return updatedata


@app.route('/register', methods=['POST'])
def take():

    return render_template('signup1.html')


# global updatedata


@app.route('/home')
def show():
    contents = []
    contents = getValues()
    mailid = getMailId()
    otherDetails = returnList()
    if(not len(otherDetails)):
        curr = str(date.today())
        return render_template('homepage.html', info=contents, details=[' ', curr, ' '])
    return render_template('homepage.html', info=contents, details=otherDetails)


@app.route('/login/home', methods=['POST'])
def takeLogin():
    f = 0
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["PREDICTION"]
    mycol = mydb["USER LOGIN DATA"]
    mycol1 = mydb["PREDICTION DATAS"]
    userInformationCol = mydb["USER PERSONAL DATA"]
    checkInpData = []
    checkInpData.append(request.form.get('maailid'))
    checkInpData.append(request.form.get('pwd'))
    a = mycol.count_documents(
        {"USER MAIL ID": checkInpData[0], "PASSWORD": checkInpData[1]})
    if(a == 1):
        currInformationHold = userInformationCol.find(
            {"USER MAIL ID": checkInpData[0]}, {'_id': 0, 'PHONE NUMBER 1': 0, 'PHONE NUMBER 2': 0, 'USER MAIL ID': 0})
        contents = currInformationHold[0].values()
        contents = list(contents)[:]
        print(contents)
        b = mycol1.find({"USER MAIL ID": checkInpData[0]}).sort(
            "_id", pymongo.DESCENDING).limit(1)
        otherDetails = []
        for a in b:
            print(a)
            currentDate = str(date.today())
            otherDetails.append(a["REPORT DATE"])
            otherDetails.append(currentDate)
            otherDetails.append(a["MEANING OF THE VALUE"])
            anotherList(otherDetails)
        # for x in contents:
        #     print(x)
        # username=contents[0], age=contents[1], docname=contents[2], hosp=contents[3]
        setMailId(checkInpData[0])
        del otherDetails[:]
        del checkInpData[:]
        takeValues(contents)
        otherDetails = returnList()
        return render_template('homepage.html', info=contents, details=otherDetails)
    # data = "INVALID LOGIN CREDENTIALS"
    return render_template('login.html', val="IF THERE IS NO RENDERING PLEASE CHECK PASSWORD AND MAIL ID")


@app.route('/')  # initial route port 5000
def login():
    # contents = ['giu', '2', 'ws3', '\sss']
    # takeValues(contents)
    return takeLogin()


@app.route('/signup-step1', methods=['POST', 'GET'])  # initial route port 5000
def step1():

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["PREDICTION"]
    mycol = mydb["USER LOGIN DATA"]
    userLoginData = []
    userLoginData.append(request.form['maailid'])
    userLoginData.append(request.form['pwd'])
    userLoginData.append(request.form['cpwd'])
    if(str(userLoginData[1]) != str(userLoginData[2])):
        data = "PASSSWORD NOT MATCHED"
        return render_template('signup1.html', val=data)
    login_dict = {
        "USER MAIL ID": str(userLoginData[0]),
        "PASSWORD": str(userLoginData[1])
    }
    currInformationHold1.append(userLoginData[0])
    if(mycol.find_one({"USER MAIL ID": userLoginData[0]})):
        data = "EMAIL ALREADY EXIST TRY DIFFERENT EMAIL"
        return render_template('signup1.html', val=data)
    mycol.insert_one(login_dict)
    data = "ALMOST THERE"
    del userLoginData[:]
    return render_template('signup2.html')


@app.route('/signup-step2', methods=['POST'])  # initial route port 5000
def step2():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["PREDICTION"]
    mycol = mydb["USER PERSONAL DATA"]
    userLoginData = []
    userLoginData.append(request.form['name'])
    userLoginData.append(request.form['age'])
    userLoginData.append(request.form['phnum1'])
    userLoginData.append(request.form['phnum2'])
    userLoginData.append(request.form['dname'])
    userLoginData.append(request.form['hname'])
    userLoginData.append(request.form['adnum'])
    if(mycol.count_documents({"AADHAR NUMBER": userLoginData[6]}) > 0):
        return render_template('signup2.html', val="AADHAR NUMBER ALREADY EXISTS")
    user_per_dict = {
        "USER MAIL ID": currInformationHold1[0],
        "USER NAME": userLoginData[0],
        "AGE": userLoginData[1],
        "PHONE NUMBER 1": userLoginData[2],
        "PHONE NUMBER 2": userLoginData[3],
        "DOCTOR NAME": userLoginData[4],
        "HOSPITAL NAME": userLoginData[5],
        "AADHAR NUMBER": userLoginData[6],
    }
    mycol.insert_one(user_per_dict)
    del userLoginData[:]
    return render_template('login.html')


@app.route('/home/predict')  # initial route port 5000
def predict():
    return render_template('predictForm.html')


@app.route('/predictData', methods=['POST'])
def predict1():
    contents = getValues()
    # takeValues(contents)
    mailid = getMailId()
    mailid = str(mailid[0])
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    medicalDb = client["PREDICTION"]
    medicalCol = medicalDb["PREDICTION DATAS"]
    predictFormMedicalData = []
    predictFormMedicalData.append(float(request.form['accval']))
    predictFormMedicalData.append(float(request.form['astv_val']))
    predictFormMedicalData.append(float(request.form['mvstval']))
    predictFormMedicalData.append(float(request.form['tastv_val']))
    predictFormMedicalData.append(float(request.form['hme_val']))
    fetalHealthPredictorValue = int(
        fp.fetalHealthPredictor([predictFormMedicalData]))
    reportId = medicalCol.count_documents({})
    reportId = reportId+1
    reportdate = str(date.today())

    meaning = getMeaning(fetalHealthPredictorValue)
    predict_form_input_dict = {
        "USER MAIL ID": mailid,
        "REPORT ID": str(reportId),
        "REPORT DATE": reportdate,
        "ACCELERATION VALUE": predictFormMedicalData[0],
        "ABNORMAL SHORT TERM VARIABILITY VALUE": predictFormMedicalData[1],
        "MEAN VALUE OF SHORT TERM VARIABILITY": predictFormMedicalData[2],
        "TIME % WITH ABNORMAL SHORT TERM VARIABILITY VALUE": predictFormMedicalData[3],
        "HISTOGRAM MEAN VALUE": predictFormMedicalData[4],
        "VALUE OF THE PREDICT": fetalHealthPredictorValue,
        "MEANING OF THE VALUE": meaning,
    }
    predictFormMedicalData.append(fetalHealthPredictorValue)
    predictFormMedicalData.append(meaning)
    takeMedicalValues(predictFormMedicalData)
    userdata = getValues()
    medicalCol.insert_one(predict_form_input_dict)
    return showResultTemplate(predictFormMedicalData, userdata)


# initial route port 5000
@ app.route('/home/questionPost', methods=['GET', 'POST'])
def qp():
    return render_template('questionsPost.html')
# def qp():
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = client["PREDICTION"]
#     mycol = mydb["POSTED QUESTIONS"]
#     mailid = getMailId()
    # mailid = mailid[0]
    # questionTitle = request.form.get("worry-name")
    # questionDescription = format(request.form.get("describedproblem"))
    # questionId = mycol.count_documents({})+1
    # question_dict = {
    #     "QUESTION ID": questionId,
    #     "POSTED MAIL ID": mailid,
    #     "QUESTION NAME": questionTitle,
    #     "DESCRIBED QUESTION": questionDescription,
    # # }
    # mycol.delete_many({"DESCRIBED QUESTION": "None"})
    # mycol.delete_many({"QUESTION NAME": ""})
    # mycol.insert_one(question_dict)
    # return render_template('questionsPost.html')


# @app.route('/home/search', methods=['GET', 'POST'])
# def search():
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = client["PREDICTION"]
#     # mycol = mydb["POSTED QUESTIONS"]
#     mycol1 = mydb["ANSWERED QUESTIONS"]
#     findwhat = request.form.get('searchit')
#     mycol1.create_index([('ANSWERS', 'text')])
#     a = mycol1.find({"$text": {"$search": findwhat}})
#     temp = []
#     for i in a:
#         temp.append(i['ANSWER'])
#     print(temp)
#     return render_template('questionsPost.html')
@app.route('/home/seeProblemSols')
def showAnswers():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["PREDICTION"]
    mycol1 = mydb["ANSWERED QUESTIONS"]
    a = mycol1.find({}, {'_id': 0, 'POSTED MAIL ID': 0,
                    'ANSWER ID': 0}).limit(10)
    sendAnswers = []
    sendUpcount = []
    sendDowncount = []
    for i in a:
        showingAnswer = 'ONE WORD:' + '#' + \
            i['QUESTION NAME']+'\n\n'+i['DESCRIBED ANSWER']
        sendAnswers.append(showingAnswer)
    return render_template("answerPosts.html", ans=sendAnswers)


@ app.route('/home/PostQA', methods=['GET', 'POST'])
def proans():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["PREDICTION"]
    mycol1 = mydb["ANSWERED QUESTIONS"]
    mailid = getMailId()
    mailid = mailid[0]
    questionTitle = request.form.get("worry-answer-name")
    AnswerDescription = format(request.form.get("answer"))
    answerId = mycol1.count_documents({})+1
    answer_dict = {
        "POSTED MAIL ID": mailid,
        "ANSWER ID": answerId,
        "QUESTION NAME": questionTitle,
        "DESCRIBED ANSWER": AnswerDescription,
    }
    mycol1.insert_one(answer_dict)
    return render_template('questionsPost.html')

# @app.route('/home/getEmailcopy')
# def sendEmail():
#     mail_content = '''Hello,
# This is an auto generated mail.
# In this mail we are sending some attachments regarding our prediction result.
# Please take care of your health regardless of the results.
# Thank You
# '''
#     sender_address = 'dkgurucharan@gmail.com'
#     sender_pass = '9731151567'
#     receiver_address = 'dkgurucharan@gmail.com'
# # Setup the MIME
#     message = MIMEMultipart()
#     message['From'] = sender_address
#     message['To'] = receiver_address
#     message['Subject'] = 'A test mail sent by Python. It has an attachment.'
# # The subject line
# # The body and the attachments for the mail
#     message.attach(MIMEText(mail_content, 'plain'))
#     attach_file_name = 'res.pdf'
#     attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
#     payload = MIMEBase('application', 'octate-stream')
#     payload.set_payload((attach_file).read())
#     encoders.encode_base64(payload)  # encode the attachment
# # add payload header with filename
#     payload.add_header('Content-Decomposition',
#                        'attachment', filename=attach_file_name)
#     message.attach(payload)
# # Create SMTP session for sending the mail
#     session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
#     session.starttls()  # enable security
#     # login with mail_id and password
#     session.login(sender_address, sender_pass)
#     text = message.as_string()
#     session.sendmail(sender_address, receiver_address, text)
#     session.quit()


@app.route('/home/showResult')
def showResultTemplate(list, ulist):
    # source_path_html = r"C:\Users\91900\OneDrive\Desktop\fetal\templates\result.html"
    # destination_path_html = r"C:\Users\91900\OneDrive\Desktop\fetal\result.html"
    # shutil.copy(source_path_html, destination_path_html)
    return render_template('result.html', userName=ulist[0], userAge=ulist[1], userdocname=ulist[2], userHospName=ulist[3], acc=float(list[0]), astv=float(list[1]), mvst=float(list[2]), tast=float(list[3]), hme=float(list[4]),
                           pred=float(list[5]), result=list[6])

    # @app.route('/home/showResult')
    # def showResultTemplate(mailid, repid):
    #     client = pymongo.MongoClient("mongodb://localhost:27017/")
    #     db = client["PREDICTION"]
    #     userInfoCol = db["USER PERSONAL DATA"]
    #     reportContentsCol = db["PREDICTION DATAS"]
    #     Info = []
    #     medInfo = []
    #     b = reportContentsCol.find({"USER MAIL ID": mailid, "REPORT ID": repid}, {
    #                                '_id': 0, 'USER MAIL ID': 0, 'REPORT ID': 0})
    #     a = userInfoCol.find({"USER MAIL ID": mailid}, {
    #         '_id': 0, 'PHONE NUMBER 1': 0, 'PHONE NUMBER 2': 0, 'USER MAIL ID': 0})
    #     medInfo.append(b['ACCELERATION VALUE'])
    #     medInfo.append(b['ABNORMAL SHORT TERM VARIABILITY VALUE'])
    #     medInfo.append(b['MEAN VALUE OF SHORT TERM VARIABILITY'])
    #     medInfo.append(b['TIME % WITH ABNORMAL SHORT TERM VARIABILITY VALUE'])
    #     medInfo.append(b['HISTOGRAM MEAN VALUE'])
    #     medInfo.append(b['VALUE OF THE PREDICT'])
    #     medInfo.append(b['MEANING OF THE VALUE'])

    #     Info.append(a['USER NAME'])
    #     Info.append(a['AGE'])
    #     Info.append(a['DOCTOR NAME'])
    #     Info.append(a['HOSPITAL NAME'])
    #     return render_template('result.html', userName=Info[0], userAge=Info[1], userdocname=Info[2], userHospName=Info[3], acc=medInfo[0], astv=medInfo[1], mvstv=medInfo[2], tastv=medInfo[3], hme=medInfo[4],
    #                            predRes=medInfo[5], result=medInfo[6])


@app.route('/download')
def downloadReport():
    ulist = getValues()
    list = getMedicalValues()
    config = pdfkit.configuration(
        wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    renderedReport = render_template('finalShow.html', userName=ulist[0], userAge=ulist[1], userdocname=ulist[2], userHospName=ulist[3], acc=float(list[0]), astv=float(list[1]), mvst=float(list[2]), tast=float(list[3]), hme=float(list[4]),
                                     pred=float(list[5]), result=list[6])
    pdf = pdfkit.from_string(renderedReport, 'res.pdf', configuration=config)
    Mailid = getMailId()
    sendEmailTouser(mailid=Mailid)
    return redirect('/home')


@app.route('/home/result')
def showHistory():
    MailId = getMailId()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["PREDICTION"]
    mycol = mydb["PREDICTION DATAS"]
    a = mycol.find({"USER MAIL ID": MailId[0]}, {"_id": 0, "USER MAIL ID": 0, "ACCELERATION VALUE": 0, "ABNORMAL SHORT TERM VARIABILITY VALUE": 0,
                                                 "MEAN VALUE OF SHORT TERM VARIABILITY": 0,  "TIME % WITH ABNORMAL SHORT TERM VARIABILITY VALUE": 0,
                                                 "HISTOGRAM MEAN VALUE": 0,        "VALUE OF THE PREDICT": 0})
    atags = []
    reps = []
    datetags = []
    meaning = []
    for cur in a:
        anchors = '/home/result/'+cur['REPORT ID']
        reportId = cur['REPORT ID']
        datetags.append(cur['REPORT DATE'])
        means = cur['MEANING OF THE VALUE']
        reps.append(reportId)
        meaning.append(means)
        atags.append(anchors)
    resp = render_template('history.html', lst=atags,
                           report_list=reps, dateofreports=datetags, value_means=meaning, zip=zip)
    del reps[:]
    del atags[:]
    del meaning[:]
    return resp


@app.route('/home/result/<int:value>')
def getresult(value):
    repid = str(value)
    mailid = getMailId()
    ulist = getValues()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["PREDICTION"]
    mycol = mydb["PREDICTION DATAS"]
    a = mycol.find_one({"REPORT ID": repid, "USER MAIL ID": mailid[0]}, {
                       "_id": 0, "USER MAIL ID": 0, "REPORT ID": 0})
    sendingData = []
    sendingData.append(a["ACCELERATION VALUE"])
    sendingData.append(a["ABNORMAL SHORT TERM VARIABILITY VALUE"])
    sendingData.append(a["MEAN VALUE OF SHORT TERM VARIABILITY"])
    sendingData.append(a["TIME % WITH ABNORMAL SHORT TERM VARIABILITY VALUE"])
    sendingData.append(a["HISTOGRAM MEAN VALUE"])
    sendingData.append(a["VALUE OF THE PREDICT"])
    sendingData.append(a["MEANING OF THE VALUE"])
    takeMedicalValues(sendingData)
    return showResultTemplate(list=sendingData, ulist=ulist)


@app.route('/signout')
def logout():
    umail = getMailId()
    session.pop(umail[0], None)
    return redirect('/')


@app.route('/home/answerPost', methods=['POST'])  # initial route port 5000
def ap():

    return render_template('answerPosts.html')

# @app.route('/getinfo', methods=['POST'])  # when the form is made submit
# def pred():
#     data = []
#     data.append(request.form['accval'])
#     data.append(request.form['astv_val'])
#     data.append(request.form['mvstval'])
#     data.append(request.form['tastv_val'])
#     data.append(request.form['hme_val'])
#     value = fp.fetalHealthPredictor([data])
#     # if(value == 1.0):
#     #     return "<h1> THE BABY HEALTH IS NORMAL</h1>"
#     # elif(value == 2.0):
#     #     return "<h1>THE BABY IS PATHOLOGICAL</h1>"
#     # else:
#     #     return "<h1>THE BABY IS SUSPECT</h1>"
#     return render_template('result_shower.html', pred=value, acc=float(data[0]), astv=float(data[1]), mvst=float(data[2]), tast=float(data[3]), hme=float(data[4]))


if __name__ == '__main__':
    
    app.run(debug=True)
