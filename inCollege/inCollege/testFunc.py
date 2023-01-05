from operator import truediv
from inCollege.commons import *
from inCollege.manageDB import *
import pytest


def loginStatus(username, password):
  check = checkExistingAccts(username, password)
  if check == -1:
    clear()
    return False
  else:
    clear()
    return True


def stateMainInterface(username, password):
  if loginStatus(username, password) == True:
    return True
  else:
    return False


def listOptions(sel):
  if sel == '1' or sel == '2' or sel == '3':
    return True
  else:
    return False


def accountCount(count):
  count = userCount()
  if count > 5 or count < 0:
    return False
  else:
    return True

def jobCount(count):
  count = jobsCount()
  if count > 10 or count < 0:
    return False
  else:
    return True

def listSkillsOptions(sel):
  if sel == '1' or sel == '2' or sel == '3' or sel == '4' or sel == '5' or sel == '6':
    return True
  else:
    return False


def stateUnderConstruction(sel):
  if sel == '1' or sel == '2' or sel == '4' or sel == '6' or sel == '8' or sel == '10':
    return True
  else: 
    return False


@pytest.fixture
def testTitleCase():
  text = 'test'
  text1 = 'Computer science'
  upper = text.title()
  upper1 = text1.title()
  if upper == 'Test' or upper1 == 'Computer Science':
        return True
  else:
        return False

def getAppliedJobsCount(userId):
  databaseCursor.execute("SELECT Count(*) FROM jobApplications WHERE userId= ?", (userId, ))
  found = databaseCursor.fetchone()
  if found:
    return found[0]

def getSavedJobsCount(userId):
  databaseCursor.execute("SELECT Count(*) FROM jobApplications WHERE userId= ?", (userId, ))
  found = databaseCursor.fetchone()
  if found:
    return found[0]

def getAllJobsCount():
  databaseCursor.execute("SELECT Count(*) FROM jobs")
  found = databaseCursor.fetchone()
  if found:
    return found[0]

def getMessageCount(userId):
  databaseCursor.execute("SELECT Count(*) FROM messages WHERE receiverId= ?", (userId, ))
  found = databaseCursor.fetchone()
  if found:
    return found[0]

def getMembershipStatus(userId):
  user = databaseCursor.execute("SELECT * FROM users WHERE id = ?", (userId,)).fetchone()
  return user[7]
