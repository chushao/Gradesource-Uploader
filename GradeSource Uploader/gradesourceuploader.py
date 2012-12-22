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

# To use: gradesourceuploader.updateScores(loginnname, courseID, assignment name, CSVFile)
# Can also be replaced with static as well.
#
def updateScores(login, courseID, assignmentID, CSVFile):
    gradesource = GradesourceSession(login, getpass('Password: '), courseID)
    gradesource.updateScore(assignmentID, CSVFile)

