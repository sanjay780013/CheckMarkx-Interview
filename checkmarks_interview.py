import subprocess
import os, sys
import re
import os
import time
import email, smtplib, ssl, getpass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from pip._internal import main

currentDir = "./"
clocExec = ("./bin/cloc-1.90.exe")
timestr = time.strftime("%Y%m%d%H%M%S")
repoUrl = input("Type the URL for the repository: ") #"https://github.com/sanjay780013/Listed"
def install(package):
	main(['install', package])
try:
	import git
except ImportError:
	print('git is not installed, installing it now!')
	install('GitPython')
	install('Git')
	
def gettingRepoFrmUrl():
    return(repoUrl.strip(".git").split("/")[-1])

def checkRepoValidity():
        if not re.match(r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(\/)?", repoUrl): #https://stackoverflow.com/questions/2514859/regular-expression-for-git-repository
            print(repoUrl + " is not a valid github URL please check your url and re-run again")
            sys.exit() # exit if the url is not valid
        else:
            print(repoUrl +" is a valid URL ")

def cloningRepo(): 
    #repoName = gettingRepoFrmUrl()
    #outputFile = timestr+"_"+repoName+".csv"
    if not os.path.exists(currentDir+repoName):
        print ("Cloning Git Repository.....")
        try:
            git.Git(currentDir).clone(repoUrl) # https://stackoverflow.com/questions/2472552/python-way-to-clone-a-git-repository
        except git.exc.GitError:
            print("Please check if your Repository exisits in github")
            sys.exit() # exit if thrown error likely the repo doesnt exists
    else:
        print ("Pulling latest changes from the repository.....")
        repo = git.Repo(repoName)
        g = git.cmd.Git(repoName) 				#https://stackoverflow.com/questions/15315573/how-can-i-call-git-pull-from-within-python
        g.pull()
        print ("Latest changes from the repository has been pulled.....")

    print ("Getting Cloc report from your Repository " + repoName)
    proc = subprocess.Popen([clocExec,currentDir+repoName, "--csv","--out", outputFile , "--quiet"], stdout=subprocess.PIPE)
    proc.stdout.read()
    print ("Report Generated and outputted on the file " + outputFile)

    
# idea from https://realpython.com/python-send-email/ 

def sendingEmail():
    port = 465 # for SSL encrypted connection
    smtpServer = "smtp.gmail.com"
    sender_email =  input("Type your Sender's email and press enter: ") #"smtpapp22@gmail.com"
    password = getpass.getpass(prompt='Please type in password for your SMTP test email: ', stream=None)
    receiver_email = input("Type the destination email and press enter: ")
    subject = "This is a Cloc report from the test"
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
    message.attach(MIMEText('Sending an attachment', 'plain'))
    with open(outputFile, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename='+ str(outputFile))
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

        # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
            print("Email send to email id: " + receiver_email )
        except SMTPException as e:
            print('There was an error sending an email please check your password or recivers email please make sure its valid email: ', e) 
        
gettingRepoFrmUrl()
repoName = gettingRepoFrmUrl()
outputFile = timestr+"_"+repoName+".csv"
checkRepoValidity()
cloningRepo()
sendingEmail()
    