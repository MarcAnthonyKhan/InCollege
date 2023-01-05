import pytest
import sys
import builtins
from unittest import mock
import sqlite3

from inCollege.manageDB import *
from inCollege.testFunc import *
from inCollege.commons import *
from inCollege.states import deleteJobPosting, newAcct, mainInterface, jobInterface, jobViewQuery, jobDetails, applyForJob, jobPost


# ==================================================================================
# ==================================================================================





# EPIC #6 Test Cases





# ==================================================================================
# ==================================================================================

def initTestAccounts():
    accounts = [
        ('test1', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs'),
        ('test2', 'aaaaaaa!A1', 'fname', 'lname', 'usf', 'ce'),
        ('test3', 'aaaaaaa!A1', 'f', 'l', 'hcc', 'cs'),
        ('test4', 'aaaaaaa!A1', 'fff', 'lll', 'NONE', 'NONE'),
        ('test5', 'aaaaaaa!A1', 'firstname', 'lastname', 'usf', 'cse')
	]
    for account in accounts:
        inputs = iter(account)
        with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
            newAcct()


# entered information be stored and associates with job has been applied for 
# so that when list of jobs displayed, applied job will be indicated
def initTestJobs():
	jobs = [
		('SWE', 'Software Engineer', 'Google', 'Tampa, FL', '100000.0', 1),
        ('DevOps', 'Dev Ops', 'Google', 'Tampa, FL', '100000.0', 1),
        ('Frontend', 'Frontend Engineer', 'Google', 'Tampa, FL', '100000.0', 1),
	]
	for job in jobs:
		inputs = iter(job)
		with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
			jobPost(1)

def initAppliedJobs():
    appliedJobs = [
        (1, 1, '01/21/2022', '02/21/2022', 'h'),
        (1, 2, '01/22/2022', '02/22/2022', 'hi'),
        (2, 1, '01/23/2022', '02/23/2022', 'hihi'),
        (2, 2, '01/24/2022', '02/24/2022', 'hihihi'),
        (2, 3, '01/25/2022', '02/25/2022', 'hihihi'),
    ]
    for appliedJob in appliedJobs:
        addJobApplication(appliedJob[0], appliedJob[1], appliedJob[2], appliedJob[3], appliedJob[4])

def initSavedJobs():
    savedJobs = [
        (1, 1), # userId, jobId
        (1, 2),
        (2, 1),
        (2, 2),
        (2, 3)
    ]
    for savedJob in savedJobs:
        toggleSavedJob(savedJob[0], savedJob[1])


# ==================================================================================
# ==================================================================================


# the maximum number of jobs is 10
@pytest.mark.jobCount
def test_jobCount():
    assert jobCount(0) == True 


# view Jobs and Internships option on the mainInterface
# Once the option is selected, show jobInteface state
@pytest.mark.jobStates
@pytest.mark.parametrize('select', [('1')])
def test_viewJobInteface(select):
    state = jobInterface
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = mainInterface(-1)
        assert output == state


# view a list of job that student have applied 
# and have not yet applied for
@pytest.mark.jobApplication
@pytest.mark.parametrize('userId, result', [(1, 2), (2, 3), (3, 0)])
def test_viewAppliedJobs(userId, result):
    clearJobs()
    initTestJobs()
    clearApplications()
    initAppliedJobs()
    output = getAppliedJobsCount(userId)
    assert output == result

@pytest.mark.jobApplication
@pytest.mark.parametrize('userId, result', [(1, 1), (2, 0), (3, 3)])
def test_viewNotAppliedJobs(userId, result):
    clearJobs()
    initTestJobs()
    clearApplications()
    initAppliedJobs()
    appliedJobs = getAppliedJobsCount(userId)
    totalJobs = getAllJobsCount()
    output = totalJobs - appliedJobs
    assert output == result


# once applied for a job, they cannot apply it again.
@pytest.mark.jobApplication
@pytest.mark.parametrize('userId, jobId, result', 
                        [
                            (1, 1, 2), 
                            (2, 1, 3), 
                            (3, 3, 1)
                        ]
)
def test_checkAppliedJobs(userId, jobId, result):
    clearApplications()
    initAppliedJobs()
    applyJobsAgain = [
        (1, 1, '12/21/2022', '12/21/2022', 'h'),
        (2, 1, '12/23/2022', '12/23/2022', 'hihi'),
        (3, 3, '12/25/2022', '12/25/2022', 'hihihi'),
    ]
    for job in applyJobsAgain:
        removeOldApplication(job[0], job[1])
        addJobApplication(job[0], job[1], job[2], job[3], job[4])

    assert getAppliedJobsCount(userId) == result


# view all saved jobs &
# mark a job as "saved" when I am interested in a job 
# so that I can see a list of jobs I marked 
# and I also can unmark a job when I want.
@pytest.mark.jobSaved
@pytest.mark.parametrize('userId, result', [(1, 2), (2, 3), (3, 0)])
def test_viewSavedJobs(userId, result):
    clearApplications()
    initSavedJobs()
    output = getSavedJobsCount(userId)
    assert output == result


# Check if the given string is in the valid date format
@pytest.mark.validString
@pytest.mark.parametrize('inputString, result',
                        [
                            ('01/01/2000', True),
                            ('05/12/2022', True),
                            ('1999/12/0', False),
                            ('////////', False),
                            ('06/15/2022', True),
                            ('05/12/22', False),
                            ('abced32', False)
                        ]
)
def test_validString(inputString, result):
    assert dateValidator(inputString) == result


# select a job so that all of available information for that job displayed
# @pytest.mark.jobStates
# @pytest.mark.parametrize('select, querySel', [(1, 1), (1, 2), (1, 3)])
# def test_viewJob(select, querySel):
#     state = jobDetails
#     queriedJobs = queryAllJobs(-1)
#     inputs = iter(select, queriedJobs[querySel - 1])
#     with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
#         output, dataOut = jobViewQuery(-1)
#         assert output == state


# show the list of saved jobs and applied jobs so that they will be retained and can be displayed next time student logs in


# delete a job I posted so that who applied for that job will have notification for that job removed
@pytest.mark.jobDelete
@pytest.mark.parametrize('jobId, result', [(2, 2), (3, 1)])
def test_deleteJobs(jobId, result):
    deleteJob(jobId)
    assert getAllJobsCount() == result



