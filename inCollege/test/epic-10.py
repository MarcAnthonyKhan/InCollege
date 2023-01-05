import pytest
import sys
import builtins
from unittest import mock
import sqlite3
import os.path
import os

from inCollege.manageDB import 	clearJobs, clearApplications, clearUsers, clearMessages, queryNewJobsAndUpdate, getAllJobsInfo, getAllUsersBaseInfo, deleteJob, clearProfiles, removeWorkExperience, toggleSavedJob

from inCollege.states import deleteJobPosting, jobPost, applyForJob, jobInterface, loginNotifications, newAcct, sendMessageInterface, updateProfileSimple, myWorkExperience, myEducation, myProfile
from inCollege.api import usersAPI, studentAccountsAPI, jobsAPI, newJobsAPI, profilesAPI, savedJobsAPI, appliedJobsAPI
# from inCollege.testFunc import 

database = sqlite3.connect("inCollege.db")
databaseCursor = database.cursor()


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
    jobs = [('ce', 'stuff\n\non another line', 'self', 'FL', '99999'),
            ('cs', 'stuff', 'self', 'FL', '99999'),
            ('it', 'stuff', 'self', 'FL', '99999'),
            ('aa', 'stuff', 'self', 'FL', '99999')
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
			#toggleSavedJob(userId, jobId)

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

def initProfiles():
	inputs = iter(['1','1', 'cool guy', 'cs', 'usf', 'i am cool', 'other guy', 'ce', 'usf', 'also cool', 'hard work', 'corpo', '01/01/0001', '11/19/2022', 'space', 'i did cool stuff', 'more work', 'corpo', '11/11/1111', '11/11/1111', 'space', 'i did lame stuff','usf', 'c', '1-1', 'usf','ce','2-2'])
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		myProfile(1)
		myProfile(2)
		for i in range(1,3):
			for j in range(1,5):
				updateProfileSimple(i, j)
		myWorkExperience(1)
		myWorkExperience(1)
		myEducation(1)
		myEducation(2)

def setupEnv():
    clearUsers()
    clearJobs()
    clearApplications()
    clearMessages()

    initTestAccounts()
    initJobs()
    initApplications()
    initMessages()




def test_usersOutAPI():
	clearUsers()
	initTestAccounts()

	apiFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "MyCollege_users.txt")

	if os.path.exists(apiFilePath):
		os.remove(apiFilePath)

	usersAPI()

	expectedLines = ["test1 plus\n", "test2 standard\n", "test3 plus\n", "test4 standard\n", "test5 plus\n"]

	assert os.path.exists(apiFilePath)

	outputFile = open(apiFilePath, "r")

	outputLines = outputFile.readlines()
	outputFile.close()

	assert expectedLines == outputLines


def test_userInAPI():

	clearUsers()
	
	apiInputFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "studentAccounts.txt")

	inputFile = open(apiInputFilePath, "w")

	expectedUsers = [
		("test1", "t1", "t1", "123456A!"),
		("test2", "t2", "t2", "123456A!"),
		("test3", "t3", "t3", "123456A!"),
		("test4", "t4", "t4", "123456A!"),
		("test5", "t5", "t5", "123456A!"),
		("test6", "t6", "t6", "123456A!"),
		("test7", "t7", "t7", "123456A!"),
		("test8", "t8", "t8", "123456A!"),
		("test9", "t9", "t9", "123456A!"),
		("test0", "t0", "t0", "123456A!")
	]

	for user in expectedUsers:
		inputFile.write("{0} {1} {2}\n{3}\n=====\n".format(user[0], user[1], user[2], user[3]))
		
	inputFile.write("testN tN tN\n123456A!\n=====\n")

	inputFile.close()
	
	studentAccountsAPI()

	obtainedUsers = getAllUsersBaseInfo()

	assert obtainedUsers == expectedUsers


def test_jobOutAPIAfterInsertions():

	clearUsers()
	clearJobs()

	initTestAccounts()
	initJobs()

	
	apiFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "MyCollege_jobs.txt")

	if os.path.exists(apiFilePath):
		os.remove(apiFilePath)

	jobsAPI()
	expectedLines = ['ce stuff\n','\n', 'on another line self FL 99999.0\n', 
					 '=====\n', 
					 'cs stuff self FL 99999.0\n', 
					 '=====\n',
					 'it stuff self FL 99999.0\n',
					 '=====\n',
					 'aa stuff self FL 99999.0\n',
					 '=====\n']

	assert os.path.exists(apiFilePath)

	outputFile = open(apiFilePath, "r")

	outputLines = outputFile.readlines()
	outputFile.close()

	assert expectedLines == outputLines


	
def test_jobOutAPIAfterDeletion():

	clearUsers()
	clearJobs()

	initTestAccounts()
	initJobs()

	
	apiFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "MyCollege_jobs.txt")

	if os.path.exists(apiFilePath):
		os.remove(apiFilePath)

	jobsAPI()

	deleteJob(1) # we expect this to force a refresh of the file
	
	expectedLines = ['cs stuff self FL 99999.0\n', 
					 '=====\n',
					 'it stuff self FL 99999.0\n',
					 '=====\n',
					 'aa stuff self FL 99999.0\n',
					 '=====\n']

	assert os.path.exists(apiFilePath)

	outputFile = open(apiFilePath, "r")

	outputLines = outputFile.readlines()
	outputFile.close()

	assert expectedLines == outputLines

def test_profilesOutAPI():

	clearUsers()
	clearProfiles()
	removeWorkExperience()

	initTestAccounts()
	initProfiles()

	
	
	expectedLines = ['cool guy\n', 
					 'Cs\n',
					 'Usf\n',
					 'i am cool\n',
					 'Hard Work Corpo 01/01/0001 11/19/2022 Space i did cool stuff\n',
					 'More Work Corpo 11/11/1111 11/11/1111 Space i did lame stuff\n',
					 '1-1\n',
					 '=====\n',
					 'other guy\n',
					 'Ce\n',
					 'Usf\n',
					 'also cool\n',
					 '2-2\n',
					 '=====\n']

	apiFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "MyCollege_profiles.txt")

	assert os.path.exists(apiFilePath)

	outputFile = open(apiFilePath, "r")

	outputLines = outputFile.readlines()
	outputFile.close()

	assert expectedLines == outputLines


def test_appliedJobs():
	clearUsers()
	clearJobs()
	clearApplications()
	
	initTestAccounts()
	initJobs()
	initApplications()


	apiFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "MyCollege_appliedJobs.txt")

	if os.path.exists(apiFilePath):
		os.remove(apiFilePath)

	appliedJobsAPI()

	expectedLines = [
		'ce\n',
		'test3 - because\n',
		'=====\n',
		'cs\n',
		'test4 - because\n',
		'=====\n',
		'it\n',
		'test5 - because\n',
		'=====\n',
		'aa\n',
		'test2 - because\n',
		'=====\n'
	]

	assert os.path.exists(apiFilePath)

	outputFile = open(apiFilePath, "r")

	outputLines = outputFile.readlines()
	outputFile.close()

	assert expectedLines == outputLines


def test_savedJobs():
	clearUsers()
	clearJobs()
	clearApplications()

	initTestAccounts()
	initJobs()
	initApplications()


	apiFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "MyCollege_savedJobs.txt")

	if os.path.exists(apiFilePath):
		os.remove(apiFilePath)

	toggleSavedJob(3,1)
	toggleSavedJob(4,2)
	toggleSavedJob(5,3)
	toggleSavedJob(2,4)

	savedJobsAPI()

	expectedLines = [
		'aa test2\n',
		'=====\n',
		'ce test3\n',
		'=====\n',
		'cs test4\n',
		'=====\n',
		'it test5\n',
		'=====\n',
	]

	assert os.path.exists(apiFilePath)

	outputFile = open(apiFilePath, "r")

	outputLines = outputFile.readlines()
	outputFile.close()

	assert expectedLines == outputLines


def test_newJobAPI():

	clearJobs()

	apiInputFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "inCollege", "api", "newJobs.txt")

	inputFile = open(apiInputFilePath, "w")
	
	initialJobs = [
		("title1", "description1 &&&", "test1", "employerName1", "location1", 11111.0),
		("title2", "description2 &&&", "test2", "employerName2", "location2", 22222.0),
		("title3", "description3 &&&", "test3", "employerName3", "location3", 33333.0),
		("title4", "description4 &&&", "test4", "employerName4", "location4", 44444.0),
		("title5", "description5 &&&", "test5", "employerName5", "location5", 55555.0)
	]

	expectedJobs = [
		("title1", "description1 ", "employerName1", "location1", 11111.0),
		("title2", "description2 ", "employerName2", "location2", 22222.0),
		("title3", "description3 ", "employerName3", "location3", 33333.0),
		("title4", "description4 ", "employerName4", "location4", 44444.0),
		("title5", "description5 ", "employerName5", "location5", 55555.0)
	]
	

	for job in initialJobs:
		inputFile.write("{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n=====\n".format(job[0], job[1], job[2], job[3], job[4], job[5]))
	
	inputFile.close()

	newJobsAPI()

	obtainedJobs = getAllJobsInfo()

	assert obtainedJobs == expectedJobs
