# gradesourcesession.py
# Chu Shao
# Dec 22, 2012
# cshao@eng.ucsd.edu

from bs4 import BeautifulSoup
import re, requests
import csv

class GradesourceSession:
    #'global' cookies and session for method uses
    cookies = None
    s = requests.session()
    savedAccount = {}
    savedPIDAccount = {}
    savedName = {}
    savedNamePID = {}
    def __init__(self, username, password, courseid):
        # Restores the global session on gradesource
        s = self.s
        # Posts username and password to the website to login
        print("Logging in....")
        postData = {'User' : username, 'Password' : password}
        loginPOST = s.post('https://www.gradesource.com/validate.asp', data = postData)
        if loginPOST.status_code != 200:
            print("Login failed... Exiting")
            exit()
        # Saves current session cookie
        self.cookies = loginPOST.cookies
        print("Selecting course %s" % courseid)
        # Selects the course
        selectcourseGET = s.get('https://www.gradesource.com/selectcourse.asp?id=%s' % courseid, cookies = self.cookies) 
        # Save the cookies and session for other method use.
        self.cookies = selectcourseGET.cookies
        self.s = s
        # Calls the email function to populate a dictionary of student email + gradesource ID
        self.email()

    # Updates the score by CSV sheet
    def updateEmailScore(self, field, CSV, overwrite):
        # Restores the initialized logged in session
        s = self.s
        print("Converting CSV into a list...")
        # Import key (email) and value (score) from the CSV 
        reader = csv.reader(open(CSV, 'rU'), delimiter=',')
        try:
            scoreDict = dict(reader)
        except Exception, e:
            print("oops, your file is malformed, please fix it (check for extra lines)")
        print(overwrite)
        if (float(overwrite) == 0):
            for k,v in scoreDict.items():
                if (v == "0"):
                    scoreDict[k] = ""
        print(scoreDict)
        print("CSV Converted")
        self.s = s
        self.updateScores(field, scoreDict)
    # Updates the score by PID from CSV Sheet     
    def updatePIDScore(self, field, CSV, overwrite):
         # Restores the initialized logged in session
        s = self.s
        print("Converting CSV into a list...")
        # Import key (email) and value (score) from the CSV 
        reader = csv.reader(open(CSV, 'rU'), delimiter=',')
        try:
            scoreDict = dict(reader)
        except Exception, e:
            print("oops, your file is malformed, please fix it (check for extra lines)")
        print(scoreDict)
        if (float(overwrite) == 0):
            for k,v in scoreDict.items():
                if (v == "0"):
                    scoreDict[k] = ""
        updateScore = {}
        savedPIDAccount = self.savedPIDAccount
        #InnerJoin (Email, PID) and (PID Score) to (Email, Score)
        for key in savedPIDAccount.keys():
            try:
                updateScore[key] = scoreDict[savedPIDAccount[key]]
            except Exception, e:
                print(savedPIDAccount[key]+ "was unable to be joined and therefore skipped")
                continue
        print(updateScore)
        print("CSV Converted to email")
        self.s = s
        self.updateScores(field, updateScore)

    def updateScores(self, field, scoreDict):
        s = self.s
        print("Updating scores...")
        # Grabs the website
        html = s.get('https://www.gradesource.com/editscores1.asp?id=%s' % field, cookies = self.cookies).content
        # Grabs the max score and runs a check on if any scores are over the maximum
        returnOutput = {}
        totalCount = re.compile('<td nowrap colspan=3 class=BT>&nbsp;&nbsp;Maximum Points: &nbsp;&nbsp;<font color="#336699"><b>(.*)</b></font></td>')
        maximumScore = totalCount.search(html).group(1).strip()
        for k,v in scoreDict.items():
            # Edge case in which the score wasn't inputed
            if (v == ""): 
                value = -1
            else:
                value = float(v)
            maxScore = float(maximumScore) 
            if(value > maxScore):
                # Throw warning, incase someone has a score of 11/10. Therefore they're not recorded
                print(k + " has a score of " + v + " which is larger than the maximum score of " + maximumScore)
                returnOutput[k] = v
                   
        # nomnom soup magic
        nomnomsoup = BeautifulSoup(html)
        updatePOSTDict = {}
        updateIDDict = {}

        for x in nomnomsoup.form('input', id = re.compile("^student")):
            # Grabs the student Number
            studentNumber = re.compile('input id="(.*)" name=')
            studentString = studentNumber.search(str(x))
            studStr = studentString.group(1).strip()
            # Grabs the gradesource Number
            gradesourceNumber = re.compile('type="hidden" value="(.*)">')
            gradesourceString = gradesourceNumber.search(str(x))
            gradStr = gradesourceString.group(1).strip()
            updatePOSTDict[studStr] = gradStr
            # Grabs the id Number
            idNumber = re.compile('input name="id(.*)" type="hidden"')
            idString = idNumber.search(str(x))
            updateIDDict[str("id" + idString.group(1).strip())] = gradStr
        # Some Innerjoin magic? yay for SQL concepts!
        joinedDictA = {}
        saveAccount = self.savedAccount
        #InnerJoin saveAccount (gradesourceNumber, email) and scoreDict (email, score) to (gradesourceNumber, score)
        for key in saveAccount.keys():
            try:
                joinedDictA[key] = scoreDict[saveAccount[key]]
            except Exception, e:
                print(saveAccount[key] + " was found in Gradesource but not in the CSV.")
                continue

        joinedDictB = {}
        #InnerJoin updatePOSTDict(studStr, gradesourceNumber) and joinedDictA(gradesourceNumber, score) to (studStr, score)
        for key in updatePOSTDict.keys():
            try:
                joinedDictB[key] = joinedDictA[updatePOSTDict[key]]
            except Exception, e:
                print(updatePOSTDict[key] + " was unable to be joined and therefore skipped")
                continue
        # Combines (studStr, score), (id, gradesource Number), (assessmentId, assignmentNumber), and (studentCount, count.length) for updatescores1.asp as 
        # thats what it requires
        joinedDictB.update(updateIDDict)
        joinedDictB['assessmentId'] = field
        joinedDictB['studentCount'] = len(saveAccount)
        s.post('https://www.gradesource.com/updatescores1.asp', data = joinedDictB, cookies = self.cookies)
        print("Scores Updated")
        for k,v in returnOutput.items():
            print("WARNING: " + k + " HAS A SCORE OF " + v + " WHICH IS LARGER THAN MAX. SCORE INPUTTED. PLEASE CHECK SITE TO CONFIRM")
    
        
    # Grabs and create a dictionary that has email and secret number.
    def email(self):
        # Restores the initialized logged in session
        s = self.s
        print("Generating list of students")
        #Grabs the webpage
        html = s.get("https://www.gradesource.com/student.asp", cookies = self.cookies).content
        # Parses the HTML with nomnom soup!
        # Also, lol at parsing. http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags
        nomnomsoup = BeautifulSoup(html)
        tbody = nomnomsoup('td', text=re.compile("Secret*"))[0].parent.parent.parent.parent
        # Create a dictionary that has email and student number
        emailDict = {}
        emailPIDDict = {}
        nameDict = {}
        namePIDDict = {}
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
                # Grabs the student PID
                studentPID = tr.contents[3].text.strip()
                studentPID = studentPID.encode('ascii')
                # Grabs the student Name
                studentName = tr.contents[1].text.strip()
                studentName = studentName.encode('ascii')
                if (str(studentEmail) != "Edit") :
                    # Adds a dictionary value of studentEmail : gradesourceID Number
                    emailDict[str(studentNum)] = str(studentEmail)
                    # Add a dictionary value of studentEmail : PID
                    emailPIDDict[str(studentEmail)] = str(studentPID)
                    # Add a dictionary value of studentName: studentEmail for downloading a list?
                    nameDict[str(studentName)] = str(studentEmail)
                    # Add a dictionary value of studentName: studentPID for iClicker management
                    namePIDDict[str(studentName)] = str(studentPID)
            except Exception, e:
                #Catches and ignore the out of range for list, since there will be an extra
                continue
        # Sends the studentNumber/email dictionary to a global dictionary for other uses
        self.savedAccount = emailDict
        print(emailDict)
        print("Students List Generated")
        # Sends the name/email dictonary to a global dictionary for the download function
        self.savedName = nameDict
        # Sends the name/PID dictionary to a global dictionary for the download function
        self.savedNamePID = namePIDDict
        self.savedPIDAccount = emailPIDDict
        # Saves the session again
        self.s = s


    #Download email and student number and save it into a CSV file
    def downloadEmail(self):
        print("Creating CSV")
        writer = csv.writer(open('Roster.csv', 'wb'))
        for key, value in self.savedName.items():
            writer.writerow([key,value])
        print(self.savedName)
        print("CSV Created")

    def downloadiClicker(self):
        print("Creating CSV")
        writer = csv.writer(open('iClickerRoster.csv', 'wb'), escapechar=' ', quoting=csv.QUOTE_NONE)
        for key, value in self.savedNamePID.items():
            writer.writerow([key,value])
        print("CSV Created")

