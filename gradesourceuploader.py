# gradesourceuploader.py
# Chu Shao
# Dec 22, 2012
# cshao@eng.ucsd.edu

from gradesourcesession import GradesourceSession
from getpass import getpass

# To use: gradesourceuploader.downloadEmail(loginname, courseID)
# Also, these can be hardcoded as global variables
#
# staticLogin = 'moocow'
# staticCourseID = '12345'
def downloadEmail(login, courseID):
    # Alternative:
    # gradesource = GradesourceSession(self.staticLogin, getpass('Password: '), self.staticCourseID)
    gradesource = GradesourceSession(login, getpass('Password: '), courseID)
    gradesource.downloadEmail()

def downloadiClicker(login, courseID):
    gradesource = GradesourceSession(login, getpass('Password: '), courseID)
    gradesource.downloadiClicker()
# To use: gradesourceuploader.updateScores(loginnname, courseID, assignment name, CSVFile, overwrite)
# Can also be replaced with static as well.
#
def updateScoresByEmail(login, courseID, assignmentID, CSVFile, overwrite):
    gradesource = GradesourceSession(login, getpass('Password: '), courseID)
    gradesource.updateEmailScore(assignmentID, CSVFile, overwrite)

def updateScoresByPID(login,courseID, assignmentID, CSVFile, overwrite):
    gradesource = GradesourceSession(login, getpass('Password: '), courseID)
    gradesource.updatePIDScore(assignmentID, CSVFile, overwrite)

# FOR GUI. IF USED MANUALLY THEN PASSWORD IS PLAINTEXT. DO NOT USE THROUGH CLI.
def downloadEmailGUI(login, courseID, password):
    # Alternative:
    # gradesource = GradesourceSession(self.staticLogin, getpass('Password: '), self.staticCourseID)
    gradesource = GradesourceSession(login, password, courseID)
    gradesource.downloadEmail()

def downloadiClickerGUI(login, courseID, password):
    gradesource = GradesourceSession(login, password, courseID)
    gradesource.downloadiClicker()
# To use: gradesourceuploader.updateScores(loginnname, courseID, assignment name, CSVFile)
# Can also be replaced with static as well.
#
def updateScoresByEmailGUI(login, courseID, assignmentID, CSVFile, password, overwrite):
    gradesource = GradesourceSession(login, password, courseID)
    gradesource.updateEmailScore(assignmentID, CSVFile, overwrite)

def updateScoresByPIDGUI(login,courseID, assignmentID, CSVFile, password, overwrite):
    gradesource = GradesourceSession(login, password, courseID)
    gradesource.updatePIDScore(assignmentID, CSVFile, overwrite)
