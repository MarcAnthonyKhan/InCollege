import pytest
import sys
import builtins
from unittest import mock
import sqlite3

from inCollege.manageDB import 	clearJobs, clearApplications, clearUsers, clearMessages, queryNewJobsAndUpdate, clearProfiles
from inCollege.states import deleteJobPosting, jobPost, applyForJob, jobInterface, loginNotifications, newAcct, sendMessageInterface
# from inCollege.testFunc import 

database = sqlite3.connect("inCollege.db")
databaseCursor = database.cursor()


# ==================================================================================
# ==================================================================================





# EPIC #8 Test Cases





# ==================================================================================
# ==================================================================================


def initTestAccounts():
	accounts = [
		('test1', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs', 'plus'),
        ('test2', 'aaaaaaa!A1', 'fname', 'lname', 'usf', 'ce', 'standard'),
        ('test3', 'aaaaaaa!A1', 'f', 'l', 'hcc', 'cs', 'plus'),
        ('test4', 'aaaaaaa!A1', 'fff', 'lll', 'NONE', 'NONE', 'standard'),
        ('test5', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs', 'plus'),
	]
	for account in accounts:
		inputs = iter(account)
		with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
			newAcct()
   
def initJobs():
    jobs = [('ce', 'stuff', 'self', 'FL', '99999'),
            ('ce', 'stuff', 'self', 'FL', '99999'),
            ('ce', 'stuff', 'self', 'FL', '99999'),
            ('ce', 'stuff', 'self', 'FL', '99999')
    ]
    userId = 2
    for job in jobs:
        inputs = iter(job)
        with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
            jobPost(userId)
        userId = userId + 1
        
def initApplications():
    apps = [('01/01/2022', '01/01/2022', 'because', ''),
            ('01/01/2022', '01/01/2022', 'because', ''),
            ('01/01/2022', '01/01/2022', 'because', ''),
            ('01/01/2022', '01/01/2022', 'because', '')
    ]
    userId = 3
    jobId = 1
    for app in apps:
        inputs = iter(app)
        with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
            applyForJob(userId, jobId)
        userId = userId + 1 if userId != 5 else 2
        jobId = jobId + 1
        
def initMessages():
    messages = [('test message'),
                ('test message'),
                ('test message'),
                ('test message')
    ]
    userId = 2
    recipient = 'test3'
    for message in messages:
        inputs = iter(message)
        with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
            sendMessageInterface(userId, recipient)
        userId = userId + 1
        recipient = 'test' + str(userId + 1) if userId != 5 else 'test' + str(2)

def test_setupEnv():
    clearUsers()
    clearJobs()
    clearApplications()
    clearMessages()
    clearProfiles()

    initTestAccounts()
    initJobs()
    initApplications()
    initMessages()
        

        
# Tests notification when entering job section
@pytest.mark.parametrize('userId', [2, 3, 4, 5])
def test_jobInterfaceNotification(capfd, userId):
    notification = "You have applied to 1 jobs"
    inputs = iter(['', '4'])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        output, dataOut = jobInterface(userId)
        out, err = capfd.readouterr()
        assert True if notification in out else False == True
        

# Tests notification when user hasn't applied to job within the last 7 days
@pytest.mark.parametrize('userId', [2, 3, 4, 5])
def test_lastApp7DaysAgo(capfd, userId):
    for i in range(2, 6):
        databaseCursor.execute('UPDATE jobApplications SET appliedTimestamp = 1 WHERE userID = ?', (i, ))
        databaseCursor.execute('UPDATE users SET accountCreatedTimestamp = -999999999 WHERE id = ?', (i, ))
        database.commit()
    notification = "Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs Today!"
    inputs = iter(['', '', '', ''])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        output, dataOut = loginNotifications(userId)
        out, err = capfd.readouterr()
        assert True if notification in out else False == True
        

@pytest.mark.parametrize('userId', [2, 3, 4, 5])
def test_deletedJobNotification(capfd, userId):
    inputs = iter(['1', 'no'])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        deleteJobPosting(userId - 1 if userId != 2 else 5)

    with mock.patch.object(builtins, 'input', lambda _: ''):
        loginNotifications(userId)
        out, err = capfd.readouterr()
        assert "The job ce you applied to has been deleted." in out


# Tests notification to user if user has not created a profile yet
@pytest.mark.parametrize('userId', [2, 3, 4, 5])
def test_createProfileNotification(capfd, userId):
    notification = "Don't forget to create a profile\n"
    inputs = iter(['', '', '', ''])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        output, dataOut = loginNotifications(userId)
        out, err = capfd.readouterr()
        print(out)
        assert True if notification in out else False == True
        

# Tests notification of new messages after the user logs in
@pytest.mark.parametrize('userId', [2, 3, 4, 5])
def test_messageNotification(capfd, userId):
    notification = "You have 1 unread messages in your inbox.\n"
    inputs = iter(['', '', '', ''])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        output, dataOut = loginNotifications(userId)
        out, err = capfd.readouterr()
        assert True if notification in out else False == True



# Tests notification of new users after the user logs in
@pytest.mark.parametrize('userId, expectedNewUsers', [(5, 0), (4, 1), (3, 2), (2, 3), (1, 4)])
def test_newUsersNotification(capfd, userId, expectedNewUsers):
    test_setupEnv()
    if expectedNewUsers == 0:
        notification = " users have joined InCollege"
    else:
        notification = "The following " + str(expectedNewUsers) + " users have joined InCollege"
    with mock.patch.object(builtins, 'input', lambda _: ''):
        output, dataOut = loginNotifications(userId)
        out, err = capfd.readouterr()
        if expectedNewUsers == 0:
            assert notification not in out
        else:
            assert notification in out


def test_newJobsNotification(capfd):
    test_setupEnv()
    with mock.patch.object(builtins, 'input', lambda _: ''):
        loginNotifications(2)
        out, err = capfd.readouterr()
        assert "has been added" in out

def test_queryNewJobs(capfd):
    test_setupEnv()
    assert len(queryNewJobsAndUpdate(2)) == 4
    assert len(queryNewJobsAndUpdate(2)) == 0