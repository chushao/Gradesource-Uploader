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
def test():
    gradesource.downloadEmail()
