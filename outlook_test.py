import os
print(os.getcwd())

MailSubject= "Auto test Maili"

#requirements.txt add for py 3 -> pypiwin32

def Emailer(text, subject, recipient):
    import win32com.client as win32

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = recipient
    mail.Subject = subject
    mail.HtmlBody = text
    ###

    attachment1 = os.getcwd() +"\\Model_Names.ini"

    mail.Attachments.Add(attachment1)

    ###
    mail.Display(True)

MailSubject= "Auto test mail"
MailInput="""
<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
<style>
body {
  background-color: black;
  text-align: center;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}
</style>
</head>
<body>

<h1>This is a Heading</h1>
<p>This is a paragraph.</p>
<p>Edit the code in the window to the left, and click "Run" to view the result.</p>

</body>
</html>

"""
MailAdress="person1@gmail.com;person2@corp1.com"

Emailer(MailInput, MailSubject, MailAdress ) #that open a new outlokk mail even outlook closed.