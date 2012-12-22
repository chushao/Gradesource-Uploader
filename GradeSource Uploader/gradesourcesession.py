from bs4 import BeautifulSoup
import re, requests
import sys
import csv
#import utils

class GradesourceSession:
    #Gradesource URLs to be called on for GET and POST
    editScoreURL = "https://www.gradesource.com/editscores.asp?id=%s"
    updateScoreURL = "https://www.gradesource.com/updatescores.asp?id=%s"
    #Initializes cookies and session for method uses
    cookies = None
    s = requests.session()
    savedAccount = {}

    def __init__(self, username, password, courseid):
        # Restores the global session on gradesource
        s = self.s
        # Posts username and password to the website to login
        postData = {'User' : username, 'Password' : password}
        loginPOST = s.post('https://www.gradesource.com/validate.asp', data = postData)
        # Saves current session cookie
        self.cookies = loginPOST.cookies
        # Selects the course
        selectcourseGET = s.get('https://www.gradesource.com/selectcourse.asp?id=%s' % courseid, cookies = self.cookies) 
        # Save the cookies and session for other method use.
        self.cookies = selectcourseGET.cookies
        self.s = s
        # Calls the email function to populate a dictionary of student email + gradesource ID
        self.email()

    # Single Score for all students (Replace One Column)
   # def updateSingleScore(self, field, score):
        # Name format needs to be parsed
        #TODO grab name

    # Updates all the scores for students (Replace All Columns)
   # def updateAllStudentScores(self, score):

    # Grabs and create a dictionary that has email and secret number.
    def email(self):
        # Restores the initialized logged in session
        s = self.s
        #Grabs the webpage
        html = s.get("https://www.gradesource.com/student.asp", cookies = self.cookies).content
        # Parses the HTML with nomnom soup!
        # Also, lol at parsing. http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags
        nomnomsoup = BeautifulSoup(html)
        tbody = nomnomsoup('td', text=re.compile("Secret*"))[0].parent.parent.parent.parent
        # Create a dictionary that has email and student number
        emailDict = {}
        for tr in tbody('tr'):
            try:
                # Grabs the a href of edit students column, to get the student number
                studentNum = tr.contents[9].find('a')['href']
                studentNum = studentNum.replace("editstudent.asp?id=", "")
                # Converts the string into ASCII, as its in unicode by default and that causes problems with csv writer
                studentNum = studentNum.encode('ascii')
                # Grabs the student Email
                studentEmail = tr.contents[7].text.strip()
                studentEmail = studentEmail.encode('ascii')
                # Adds a dictionary value of studentEmail : secretNumber
                emailDict[studentEmail] = secretNum
            except Exception, e:
                continue
        # Sends the dictionary to a global dictionary for other uses
        self.savedAccount = emailDict
        # Saves the session again
        self.s = s


    #Download email and student number and save it into a CSV file
    def downloadEmail(self):
        key = ['Email', 'Gradesource ID']
        writer = csv.writer(open('Roster.csv', 'wb'))
        writer.writerow(key)
        for key, value in self.savedAccount.items():
            writer.writerow([key,value])
        

        
        


