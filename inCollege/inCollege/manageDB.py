from inCollege.commons import *
import inCollege.api as api
import sqlite3
import time
import datetime
from datetime import datetime


database = sqlite3.connect("inCollege.db")
databaseCursor = database.cursor()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS users(
														id INTEGER PRIMARY KEY ASC, 
														username TEXT, 
														password TEXT,
                            firstname TEXT,
                            lastname TEXT,
                            university TEXT,
                            major TEXT,
                            membership TEXT,
                            accountCreatedTimestamp INTEGER,
                            lastSeenUserId INTEGER,
                            lastSeenJobId INTEGER)''')
database.commit()


databaseCursor.execute('''Create TABLE IF NOT EXISTS jobs(
                            jobId INTEGER PRIMARY KEY ASC,
                            title TEXT,
                            description TEXT,
                            employer TEXT,
                            location TEXT,
                            salary REAL,
                            posterId INTEGER,
                            FOREIGN KEY(posterId)
                              REFERENCES users(id))''')
database.commit()


# Table for the relationship between a user and a job (many-to-many relationship)
# Contains data for a job application and also if the job is saved or not.
databaseCursor.execute('''CREATE TABLE IF NOT EXISTS jobApplications(
                            userId INTEGER,
                            jobId INTEGER,
                            gradDate TEXT,
                            workAvailabilityDate TEXT,   
                            qualifications TEXT,
                            saved INTEGER,
                            deleted TEXT,
                            appliedTimestamp INTEGER,
                            FOREIGN KEY(userId)
                              REFERENCES users(id),
                            FOREIGN KEY(jobId)
                              REFERENCES jobs(jobId))''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS userSettings(
                            userId INTEGER,
                            receiveEmail INTEGER,
                            receiveSMS INTEGER,
                            targetedAds INTEGER,
                            language TEXT,
                            FOREIGN KEY(userId)
                                REFERENCES users(id))''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS friendships(
                            acceptRequest INTEGER,
                            senderId INTEGER,
                            receiverId INTEGER,
                            FOREIGN KEY(senderId) REFERENCES users(id),
                            FOREIGN KEY(receiverId) REFERENCES users(id))''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS profiles(
														userId INTEGER,
														title TEXT, 
														major TEXT,
                            university TEXT,
                            about TEXT,
                            school TEXT,
                            degree TEXT,
                            years TEXT)''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS workExperience (
														id INTEGER PRIMARY KEY ASC, 
                            userId INTEGER,
														title TEXT, 
														employer TEXT,
                            dateStarted TEXT,
                            dateEnded TEXT,
                            location TEXT,
                            description TEXT)''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            messageId INTEGER PRIMARY KEY ASC,
                            senderId INTEGER,
                            receiverId INTEGER,
                            content TEXT,
                            sentTimestamp INTEGER,
                            lastReadTimestamp INTEGER,
                            FOREIGN KEY(senderId) REFERENCES users(id),
                            FOREIGN KEY(receiverId) REFERENCES users(id))''')

database.commit()


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def clearUsers():
	databaseCursor.execute('DELETE FROM users')
	database.commit()
 

def clearJobs():
	databaseCursor.execute('DELETE FROM jobs')
	database.commit() 


def clearFriendships():
  databaseCursor.execute('DELETE FROM friendships')
  database.commit()

def clearProfiles():
  databaseCursor.execute('DELETE FROM profiles')
  database.commit()

def removeWorkExperience():
  databaseCursor.execute('DELETE FROM workExperience')
  database.commit()

def clearApplications():
  databaseCursor.execute('DELETE FROM jobApplications')
  database.commit()
  
def clearMessages():
  databaseCursor.execute('DELETE FROM messages')
  database.commit()


def listUsers():
	for row in databaseCursor.execute("SELECT * FROM users ORDER BY id"):
		print(row)


def listFriendships():
  for row in databaseCursor.execute("SELECT * FROM friendships ORDER BY senderId"):
    print(row)


def clearUserSetting(uId):
  databaseCursor.execute("DELETE FROM userSettings WHERE userId = ?", (uId,))
  database.commit()
	

def getUserById(uId):
  lookup = databaseCursor.execute("SELECT * FROM users WHERE id IS ?", (uId,))
  return lookup.fetchone()


def usernameLookup(uId):
  lookup = databaseCursor.execute("SELECT * FROM users WHERE id IS ?", (uId,))
  user = lookup.fetchone()
  return user[1]

def lookupLastJobId():

  query = databaseCursor.execute("SELECT jobId FROM jobs ORDER BY jobId DESC").fetchone()
  if query:
    return query[0]
  
  return -1

def getJobById(asId):
    
    # databaseCursor.execute('''SELECT title FROM jobs INNER JOIN jobApplications ON jobs.jobId = jobApplications.jobId WHERE jobId = ? AND deleted = 1''', (asId,))
    query = databaseCursor.execute('''SELECT title FROM jobs WHERE jobId = ? ''', (asId,)).fetchone()

    if query:
      return query[0]
    
    return -1

def getAppliedJobCount(userId):
   databaseCursor.execute("SELECT Count(*) FROM jobApplications WHERE userId= ?", (userId, ))
   found = databaseCursor.fetchone()
   if found:
    return found[0]
  

def deleteFromPendingList(userId, friendId):
  databaseCursor.execute("DELETE FROM friendships WHERE (acceptRequest = 0 AND senderId = ? AND receiverId = ?)", (friendId, userId))
  database.commit()


def deleteFromFriendList(userId, friendId):
  databaseCursor.execute("DELETE FROM friendships WHERE (acceptRequest = 1 AND senderId = ? AND receiverId = ?) OR (acceptRequest = 1 AND receiverId = ? AND senderId = ?)", (userId, friendId, userId, friendId))
  database.commit()



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

def tableEntriesCount(table):
    '''
    Generates a function that returns the number of rows in a given table

    param table: a case-sensitive string of the name of a table that is to have its rows counted
    return: A lambda f() = number of rows in table
    '''
    return lambda: (databaseCursor.execute("SELECT Count(*) FROM " + table).fetchone()[0]) # Need to look into how much of a vulnerabilty this is


userCount = tableEntriesCount("users") # returns the number of total users in the system
jobsCount = tableEntriesCount("jobs") # returns the number of total jobs in the system
friendshipsCount = tableEntriesCount("friendships")
profilesCount = tableEntriesCount("profiles")


def dbEmpty():
	if (userCount() == 0):
		return True
	else:
		return False


def dbFull():
	if (userCount() == MAX_USERS):
		return True
	else:
		return False


def jobsFull():
    return (jobsCount() == MAX_JOBS)


def vacuouslyTrue(string):
    return True


def unique(username):
    lookup = databaseCursor.execute("SELECT COUNT(*) FROM users where username IS ?", (username,))
    return lookup.fetchone()[0] == 0


def acctSettingsInitilized(userId):
  lookup = databaseCursor.execute("SELECT COUNT(*) FROM userSettings WHERE userId IS ?", (userId,))
  return lookup.fetchone()[0] == 1

def jobAppInitilized(userId, jobId):
  lookup = databaseCursor.execute("SELECT COUNT(*) FROM jobApplications WHERE userId = ? AND jobId = ?", (userId, jobId))
  return lookup.fetchone()[0] == 1

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


def initAcct(username, password, firstname, lastname, uni, major, membership):

  lastJobId = lookupLastJobId()

  databaseCursor.execute("""
                INSERT INTO users (username, password, firstname, lastname, university, major, membership, accountCreatedTimestamp, lastSeenJobId) VALUES
                    (?, ?, ?, ?, ?, ?, ?, (SELECT STRFTIME('%s')), ?)
                """, (username, password, firstname, lastname, uni, major, membership, lastJobId))

  newId = databaseCursor.lastrowid

  databaseCursor.execute("UPDATE users SET lastSeenUserId = ? WHERE id = ?", (newId, newId))

  database.commit()

  return newId

def initJob(title, description, employer, location, salary, posterId):
  databaseCursor.execute("INSERT INTO jobs (title, description, employer, location, salary, posterID) VALUES (?,?,?,?,?,?)", (title, description, employer, location, salary, posterId))

  database.commit()

  return databaseCursor.lastrowid

def initFriendRequest(senderId, receiverId):
  databaseCursor.execute("INSERT INTO friendships (senderId, receiverId, acceptRequest) VALUES (?, ?, 0)", (senderId, receiverId))
  database.commit()

def initEmptyProfile(userId):
    databaseCursor.execute("""
                INSERT INTO profiles (userId, title, major, university, about, school, degree, years) VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?)
                """, (userId, " ", " ", " ", " ", " ", " ", " "))
    database.commit()

def initWorkExperience(userId, title, employer, dateStarted, dateEnded, location, description):

  databaseCursor.execute("""
                INSERT INTO workExperience (userId, title, employer, dateStarted, dateEnded, location, description) VALUES
                    (?, ?, ?, ?, ?, ?, ?)
                """, (userId, title.title(), employer.title(), dateStarted, dateEnded, location.title(), description))
  database.commit()

def initJob(title, description, employer, location, salary, userId):

  databaseCursor.execute("INSERT INTO jobs (title, description, employer, location, salary, posterID) VALUES (?,?,?,?,?,?)",
          (title, description, employer, location, salary, userId))

  database.commit()

def checkExistingAccts(username, password):
  '''
  Looks up an account from a username and password

  param username: the username of the target user
  param password: the password of the target user
  return: the id of the specified user or -1 if the user does not exist
  '''

  databaseCursor.execute("SELECT * FROM users WHERE username= ? and password= ?",
    (username, password))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1


def checkExistingUsername(username):
  databaseCursor.execute("SELECT * FROM users WHERE username= ?",
    (username,))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1


def checkUserGuestControls(userId):
  databaseCursor.execute("SELECT receiveEmail, receiveSMS, targetedAds FROM userSettings WHERE userId = ?", (userId,))
  found = databaseCursor.fetchone()

  if found:
    return found
  else:
    return DEFAULT_GUEST_CONTROLS


def checkUserLanguage(userId):
  databaseCursor.execute("SELECT language FROM userSettings where userId = ?", (userId,))
  found = databaseCursor.fetchone()

  if found:
    return found[0]
  else:
    return DEFAULT_LANGUAGE_SETTINGS


def checkExistingNames(firstname, lastname):
  '''
  Looks up a name from firstname and lastname

  param firstname:
  param lastname:
  return the id of the specified user or -1 if the user does not exist

  '''
  databaseCursor.execute("SELECT * FROM users WHERE firstname= ? and lastname= ?", (firstname, lastname))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1


def checkExistingFriend(userId, friendId):
  databaseCursor.execute("SELECT * FROM friendships WHERE (senderId= ? AND receiverId= ?) OR (senderId= ? AND receiverId= ?)", (userId, friendId, friendId, userId))
  found = databaseCursor.fetchone()
  if found: # return 0 if the request is not accepted or 1 if the request is accepted
    return found[0]
  else:
    return -1

def getUsersWithLastname(name):
    return databaseCursor.execute("SELECT * FROM users WHERE lastname IS ?", (name,)).fetchall()

def getUsersWithUniversity(uni):
    return databaseCursor.execute("SELECT * FROM users WHERE university IS ?", (uni,)).fetchall()

def getUsersWithMajor(major):
    return databaseCursor.execute("SELECT * FROM users WHERE major IS ?", (major,)).fetchall()

def checkUserId(username):
  databaseCursor.execute("SELECT * FROM users WHERE username= ?", (username,))
  found = databaseCursor.fetchone()
  if found: # return user id
    return found[0]
  else:
    return -1

def checkExistingJobTitle(title):
  databaseCursor.execute("SELECT * FROM jobs WHERE title= ?", (title,))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1

def checkUsername(userId):
  return databaseCursor.execute("SELECT username From users WHERE id = ?", (userId,)).fetchone()[0]

def checkExistingPendingRequest(userId):
  '''
  Gets a list of all rows of friendships where the receiver is the given user and they have not accpeted
  
  param userId: id of the receiver the function queries for
  returns: a list of tuples corosponding to rows of the friendships table. Trivially returns an empty list if the user has no incoming friend requests.
  '''
  return databaseCursor.execute("SELECT * FROM friendships WHERE acceptRequest = 0 AND receiverId= ?", (userId,)).fetchall()

def queryAllFriendsOf(userId):
  return databaseCursor.execute("SELECT * FROM friendships WHERE (acceptRequest = 1 AND senderId = ?) OR (acceptRequest = 1 AND receiverId = ?)", (userId, userId)).fetchall()
  
  
def checkProfileExists(userId):
  databaseCursor.execute("SELECT * FROM profiles WHERE userId= ?", (userId,))
  found = databaseCursor.fetchall()
  if found:
    return found
  else:
    return -1
  
def checkUserMembership(userId):
  databaseCursor.execute("SELECT * FROM users WHERE id= ?", (userId,))
  found = databaseCursor.fetchone()
  if found:
    return found[7]
  else:
        return -1

def updateDB(table, field, userId, value):
  databaseCursor.execute("UPDATE " + table +  " SET " + field + " = ? WHERE userId = ?", (value, userId))
  database.commit()
    

def getUserMembership(userId):
  databaseCursor.execute("SELECT * FROM users WHERE id= ?", (userId,))
  found = databaseCursor.fetchone()
  if found: 
    return found[7]
  else:
    return -1



def getExperienceCount(userId):
  databaseCursor.execute("SELECT Count(*) FROM workExperience WHERE userId= ?", (userId, ))
  found = databaseCursor.fetchone()
  if found:
    return found[0]


def getExperience(userId):
  databaseCursor.execute("SELECT * FROM workExperience WHERE userId= ?", (userId, ))
  found = databaseCursor.fetchall()
  if found:
    return found
  else:
    return -1


def getFullname(userId):
  databaseCursor.execute("SELECT * FROM users WHERE id= ?", (userId, ))
  found = databaseCursor.fetchone()
  firstname = found[3].capitalize()
  lastname = found[4].capitalize()
  fullname = firstname + " " + lastname
  if found: 
    return fullname


def getProfile(userId):
  databaseCursor.execute("SELECT * FROM profiles WHERE userId= ?", (userId,))
  found = databaseCursor.fetchone()
  if found:
    return found
  else:
    return -1


def queryAllProfiles():
	databaseCursor.execute("SELECT * FROM profiles")
	return databaseCursor.fetchall()


def queryAllJobs():
  databaseCursor.execute("SELECT * FROM jobs")
  return databaseCursor.fetchall()

def queryAppliedJobs(userId):
  databaseCursor.execute('''SELECT jobs.jobId, title, description, employer, location, salary, posterId
                            FROM jobs
                            INNER JOIN jobApplications
                              ON jobs.jobId = jobApplications.jobId
                            WHERE jobApplications.userId = ? AND jobApplications.gradDate IS NOT NULL AND jobApplications.gradDate != "" ''', (userId,))
  return databaseCursor.fetchall()

def queryNotAppliedJobs(userId):
  databaseCursor.execute('''
                            SELECT jobs.jobId, title, description, employer, location, salary, posterId
                            FROM jobs
                            EXCEPT
                            SELECT jobs.jobId, title, description, employer, location, salary, posterId
                            FROM jobs
                            INNER JOIN jobApplications
                              ON jobs.jobId = jobApplications.jobId
                            WHERE jobApplications.userId = ? AND jobApplications.gradDate IS NOT NULL AND jobApplications.gradDate != "" ''', (userId,))
  return databaseCursor.fetchall()

def querySavedJobs(userId):
  databaseCursor.execute('''SELECT jobs.jobId, title, description, employer, location, salary, posterId
                            FROM jobs
                            INNER JOIN jobApplications
                              ON jobs.jobId = jobApplications.jobId
                            WHERE jobApplications.userId = ? AND jobApplications.saved = 1''', (userId,))
  return databaseCursor.fetchall()

def queryAllSavedJobs():
    databaseCursor.execute("SELECT * FROM jobApplications WHERE saved=? ORDER BY userId", (1, ))
    return databaseCursor.fetchall()

def getApplicationByIds(userId, jobId):
  return databaseCursor.execute("SELECT * FROM jobApplications WHERE userId = ? AND jobId = ?", (userId, jobId)).fetchone()


def toggleSavedJob(userId, jobId):
  if (not jobAppInitilized(userId, jobId)):
    databaseCursor.execute('''INSERT INTO jobApplications(userId, jobId, gradDate, workAvailabilityDate, qualifications, saved, deleted) VALUES (?, ?, '', '', '', 1, '')''', (userId, jobId))
    database.commit()

  else:
    savedState = databaseCursor.execute("SELECT saved FROM jobApplications WHERE userId = ? AND jobId = ?", (userId, jobId)).fetchone()[0]
    savedState = 0 if savedState == 1 else 1

    databaseCursor.execute("UPDATE jobApplications SET saved = ? WHERE userId = ? AND jobId = ?", (savedState, userId, jobId))
    database.commit()

def queryAllApplicationsForJob(jobId):
    databaseCursor.execute("SELECT * FROM jobApplications WHERE jobId= ? AND appliedTimestamp IS NOT NULL", (jobId,))
    return databaseCursor.fetchall()


def addJobApplication(userId, jobId, gradDate, jobAvailabilityDate, qualifications):
  databaseCursor.execute("""INSERT INTO jobApplications(userId, jobId, gradDate, workAvailabilityDate, qualifications, saved, deleted, appliedTimestamp) VALUES (?, ?, ?, ?, ?, 0, '', (SELECT STRFTIME('%s')))""", (userId, jobId, gradDate, jobAvailabilityDate, qualifications))
  database.commit()
  
def removeOldApplication(userId, jobId):
  databaseCursor.execute("DELETE FROM jobApplications WHERE userId = ? AND jobId = ?", (userId, jobId))
  database.commit()
  
def queryMyPostings(userId):
  query = databaseCursor.execute("SELECT * FROM jobs WHERE posterId = ?", (userId,)).fetchall()
  return query if query else -1

def queryNewUsersAndUpdate(userId):
  query = databaseCursor.execute("SELECT * FROM users WHERE id > (SELECT lastSeenUserId FROM users WHERE id = ?) ORDER BY id DESC", (userId,)).fetchall()

  if query:
    newestId = query[0][0] # gets the id of the newest user in the system
    databaseCursor.execute("UPDATE users SET lastSeenUserId = ? WHERE id = ?", (newestId, userId))

    database.commit()


  return query

def queryNewJobsAndUpdate(userId):
  query = databaseCursor.execute("SELECT title FROM jobs WHERE jobId > (SELECT lastSeenJobId FROM users WHERE id = ?) ORDER BY jobId DESC", (userId,)).fetchall()

  if query:
    databaseCursor.execute("UPDATE users SET lastSeenJobId = ? WHERE id = ?", (lookupLastJobId(), userId))
    database.commit()

  return query


def queryDeletions(userId):
  return databaseCursor.execute("SELECT deleted FROM jobApplications WHERE userId = ? AND deleted != ''", (userId,)).fetchall()

def deleteJob(jobId):
  
  title = getJobById(jobId)

  databaseCursor.execute("UPDATE jobApplications SET deleted = ? WHERE jobId = ?", (title, jobId))
  database.commit()
  databaseCursor.execute("DELETE FROM jobs WHERE jobId = ?", (jobId,))
  database.commit()

  api.jobsAPI()


def removeDeletions(userId):
  databaseCursor.execute("DELETE FROM jobApplications WHERE userId = ? AND deleted != ''", (userId,))
  database.commit()


def getFriendsOf(userId):
  standard =  databaseCursor.execute('''SELECT * FROM users WHERE id IN (
    SELECT senderId FROM friendships WHERE receiverId = ? AND acceptRequest = 1
    UNION
    SELECT receiverId FROM friendships WHERE senderId = ? AND acceptRequest = 1
  )''', (userId, userId) ).fetchall() #return friend ID

  return standard



def getAllUsersExcept(userId):
    plus = databaseCursor.execute("SELECT * FROM users WHERE id !=?", (userId,)).fetchall() #return userID
    return plus

def getAllUsers():
    databaseCursor.execute("SELECT * FROM users")
    return databaseCursor.fetchall()

def confirmFriendship(senderId, receiverId):
  
  databaseCursor.execute("UPDATE friendships SET acceptRequest = 1 WHERE senderId = ? AND receiverId = ?", (senderId, receiverId))
  database.commit()


def pushMessage(senderId, receiverId, message):


    databaseCursor.execute("INSERT INTO messages(senderId, receiverId, content, sentTimestamp, lastReadTimestamp) VALUES (?, ?, ?, (SELECT STRFTIME('%s')), 0)",

                           (senderId, receiverId, message))
    database.commit()


def getInbox(receiverId):
    return databaseCursor.execute("SELECT * FROM messages WHERE receiverId = ? ORDER BY lastReadTimestamp ASC, sentTimestamp DESC", (receiverId,)).fetchall()

def readTopMessage(receiverId):

    message = databaseCursor.execute("SELECT * FROM messages WHERE receiverId = ? ORDER BY lastReadTimestamp ASC, sentTimestamp DESC", (receiverId,)).fetchone()

    if message is None:
      return None

    markMessageRead(message[0])
    return message

def getNumUnreadMessages(receiverId):
    return databaseCursor.execute("SELECT COUNT(*) FROM messages WHERE receiverId = ? AND lastReadTimeStamp = 0", (receiverId,)).fetchone()[0]

def deleteMessage(messageId):
    databaseCursor.execute("DELETE FROM messages WHERE messageId = ?", (messageId,))

def markMessageRead(messageId):
    databaseCursor.execute("UPDATE messages SET lastReadTimeStamp = (SELECT STRFTIME('%s')) WHERE messageId = ?", (messageId,))


def getTimeAccountCreated(userId):
    found= databaseCursor.execute("SELECT * FROM users WHERE id = ?", (userId,)).fetchone()
    if found:
      return found[8]
    else:
      return -1
    


def getTimeAppliedJob(userId):
    found = databaseCursor.execute("SELECT appliedTimestamp FROM jobApplications WHERE userId = ? ORDER BY appliedTimestamp DESC", (userId,)).fetchone()
    if found:
      return found[0]
    else:
      return -1

def getAllUsersBaseInfo():
	return databaseCursor.execute("SELECT username, firstname, lastname, password FROM users").fetchall()

def getAllJobsInfo():
  return databaseCursor.execute("SELECT title, description, employer, location, salary FROM jobs").fetchall()

def initOrUpdateUserLanguage(userId, lang):

  if (not acctSettingsInitilized(userId)):
    databaseCursor.execute("INSERT INTO userSettings (userId, receiveEmail, receiveSMS, targetedAds,language) VALUES (?, ?, ?, ?, ?)", (userId, 1, 1, 1, lang))
  else:
    databaseCursor.execute("UPDATE userSettings SET language = ? WHERE userId = ?", (lang, userId))
  
  database.commit()

def initOrUpdateUserControls(userId, email, sms, targetedAds):

  if (not acctSettingsInitilized(userId)):
    databaseCursor.execute("INSERT INTO userSettings (userId, receiveEmail, receiveSMS, targetedAds,language) VALUES (?, ?, ?, ?, ?)", (userId, isYes(email), isYes(sms), isYes(targetedAds), "english"))
    
  else:
    databaseCursor.execute('''UPDATE userSettings SET
                                                    receiveEmail = ?,
                                                    receiveSMS = ?,
                                                    targetedAds = ?
                                                  WHERE
                                                    userId = ?''', (isYes(email), isYes(sms), isYes(targetedAds), userId)) 

  database.commit()